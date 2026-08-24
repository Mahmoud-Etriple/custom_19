from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools import clean_context

CANCEL_GROUP = "hr_expense_cancel.group_hr_expense_cancel"

# States worth cancelling. 'draft' has nothing to undo and 'refused' is
# already the destination.
CANCELLABLE_STATES = ("submitted", "approved", "posted", "in_payment", "paid")


class HrExpense(models.Model):
    _inherit = "hr.expense"

    expense_cancel_available = fields.Boolean(
        string="Can Be Cancelled",
        compute="_compute_expense_cancel_available",
        help="Technical field driving the visibility of the Cancel button.",
    )

    @api.depends("state", "company_id", "company_id.expense_cancel_enabled")
    def _compute_expense_cancel_available(self):
        for expense in self:
            company = expense.company_id or self.env.company
            expense.expense_cancel_available = bool(
                company.expense_cancel_enabled
                and expense.state in CANCELLABLE_STATES
            )

    def _expense_cancel_settings(self):
        company = self.company_id or self.env.company
        return company[:1].expense_cancel_enabled, company[:1].expense_cancel_mode

    def _check_can_cancel(self):
        enabled, _mode = self._expense_cancel_settings()
        if not enabled:
            raise UserError(self.env._(
                "The expense cancel feature is disabled. Enable it under "
                "Settings > Expenses before cancelling."
            ))
        if not self.env.user.has_group(CANCEL_GROUP):
            raise UserError(self.env._(
                "You are not allowed to cancel expenses. Ask an "
                "administrator for the 'Cancel Expenses' access right."
            ))
        blocked = self.filtered(lambda e: e.state not in CANCELLABLE_STATES)
        if blocked:
            raise UserError(self.env._(
                "These expenses are not in a state that can be cancelled: %s",
                ", ".join(blocked.mapped("display_name")),
            ))

    def _cancel_related_payments(self, moves_sudo):
        """Cancel the payments tied to ``moves_sudo`` and return them.

        A 'Paid' expense carries a payment in one of two different shapes
        depending on ``payment_mode``, and both have to be caught:

        - ``own_account`` (employee reimbursement): the payment is a
          *separate* ``account.move``, reconciled against the expense
          entry's payable line. Found via the matched counterpart lines.
        - ``company_account`` (paid directly from a company journal):
          ``account.payment`` delegates to ``account.move`` via
          ``move_id``, and here that move *is* the expense's own
          ``account_move_id`` — there's no separate move to reconcile
          against, so the reconciliation search finds nothing. Found via
          ``line_ids.payment_id`` directly on the expense's own move.

        Missing either shape is what leaves a payment posted, still
        marked paid, after the expense entry has been reversed or
        cancelled out from under it. Payments are cancelled, never
        unlinked, for the same audit-trail reason posted moves are
        reversed rather than deleted.
        """
        if not moves_sudo:
            return moves_sudo.env["account.payment"]
        reconciled_lines_sudo = (
            moves_sudo.line_ids.matched_credit_ids.credit_move_id
            | moves_sudo.line_ids.matched_debit_ids.debit_move_id
        )
        payments_sudo = moves_sudo.line_ids.payment_id | reconciled_lines_sudo.payment_id
        if not payments_sudo:
            return payments_sudo
        draft_payments_sudo = payments_sudo.filtered(lambda p: p.state == "draft")
        other_payments_sudo = payments_sudo - draft_payments_sudo
        draft_payments_sudo.unlink()
        for payment_sudo in other_payments_sudo:
            if payment_sudo.state == "canceled":
                continue
            if hasattr(payment_sudo, "action_cancel"):
                payment_sudo.action_cancel()
        return payments_sudo - draft_payments_sudo

    def _cancel_related_moves(self):
        """Undo the accounting behind the expense.

        Mirrors what core ``action_reset`` does: a draft entry can simply go,
        a posted one must be reversed rather than deleted. This is also what
        makes the cancellation visible at all — ``_compute_state`` gives
        priority to ``account_move_id``, so an expense keeps reporting
        'paid' until the move is detached, no matter what is written to
        ``approval_state``.

        Any payment tied to the entry is cancelled *before* the entry
        itself is touched. For ``company_account`` expenses this cancels
        the expense's own move as a side effect (payment and move are the
        same record), so that move is excluded from the reversal/unlink
        step below to avoid operating on an already-cancelled move. For
        ``own_account`` expenses, cancelling the payment only frees the
        reconciliation on a *different* move, leaving the expense's own
        move to be reversed as before.
        """
        moves_sudo = self.sudo().account_move_id
        if not moves_sudo:
            return
        cancelled_payments_sudo = self._cancel_related_payments(moves_sudo)
        payment_owned_moves_sudo = cancelled_payments_sudo.move_id & moves_sudo
        remaining_moves_sudo = moves_sudo - payment_owned_moves_sudo

        draft_moves_sudo = remaining_moves_sudo.filtered(lambda m: m.state == "draft")
        posted_moves_sudo = remaining_moves_sudo - draft_moves_sudo
        if posted_moves_sudo:
            posted_moves_sudo._reverse_moves(
                default_values_list=[
                    {"invoice_date": fields.Date.context_today(move_sudo)}
                    for move_sudo in posted_moves_sudo
                ],
                cancel=True,
            )
        draft_moves_sudo.unlink()

    def action_expense_cancel(self):
        """Cancel the selected expenses using the configured mode.

        Works from the form header and from the list view on a selection.
        """
        if not self:
            raise UserError(self.env._("Select at least one expense to cancel."))
        self._check_can_cancel()
        _enabled, mode = self._expense_cancel_settings()

        records = self.with_context(clean_context(self.env.context))
        records._cancel_related_moves()

        names = records.mapped("display_name")

        if mode == "cancel_draft":
            records._do_reset_approval()
            for expense in records:
                expense.message_post(body=self.env._(
                    "Expense cancelled and reset to draft."
                ))
        else:
            records.sudo().write({
                "approval_state": "refused",
                "approval_date": False,
                "account_move_id": False,
            })
            records.update_activities_and_mails()
            if mode == "cancel_delete":
                for expense in records:
                    expense.message_post(body=self.env._(
                        "Expense cancelled and deleted."
                    ))
                try:
                    records.unlink()
                except UserError as error:
                    # The delete is attempted as the acting user, on purpose:
                    # whatever restricts deleting expenses on this database
                    # should apply here too, rather than being bypassed by a
                    # sudo() buried in a cancel button.
                    #
                    # account_delete_ceo_only is the usual objector - it
                    # reserves deleting expenses for the CEO. The whole call
                    # is one transaction, so the reversal and the payment
                    # cancellation above are rolled back with it and nothing
                    # is left half-done. Without this the user saw a refusal
                    # about deletion after pressing Cancel, with no hint that
                    # the two were connected.
                    raise UserError(self.env._(
                        "The expenses could not be cancelled. This company is "
                        "set to \"Cancel and Delete\", and you are not allowed "
                        "to delete expenses:\n\n%(reason)s\n\n"
                        "Nothing has been changed. Either ask someone who may "
                        "delete expenses to do it, or switch On Cancel to "
                        "\"Cancel Only\" or \"Cancel and Reset to Draft\" under "
                        "Settings > Expenses.",
                        reason=error.args[0] if error.args else "",
                    )) from error
            else:
                for expense in records:
                    expense.message_post(body=self.env._("Expense cancelled."))

        return self._expense_cancel_notification(mode, names)

    def _expense_cancel_notification(self, mode, names):
        messages = {
            "cancel": self.env._("%s expense(s) cancelled.", len(names)),
            "cancel_draft": self.env._(
                "%s expense(s) cancelled and reset to draft.", len(names)
            ),
            "cancel_delete": self.env._(
                "%s expense(s) cancelled and deleted.", len(names)
            ),
        }
        params = {
            "type": "success",
            "message": messages.get(mode, messages["cancel"]),
        }
        # 'next' is only present when there is somewhere to go.
        #
        # It used to be set to {} on the other two modes, on the assumption
        # that an empty action is the same as no action. It is not: the web
        # client tests `params.next` for truthiness, and {} is truthy in
        # JavaScript, so it handed the empty dict to doAction and the action
        # manager refused an action whose type is undefined - "The
        # ActionManager service can't handle actions of type undefined",
        # raised after the cancellation had already succeeded and its
        # notification had already been shown. The work was done and the user
        # was looking at a crash dialog.
        #
        # Only 'cancel_delete' needs a next action, because the record the
        # form is sitting on no longer exists and the client has to be told to
        # leave. In the other two modes the record is still there and the
        # client reloads it by itself.
        if mode == "cancel_delete":
            params["next"] = {"type": "ir.actions.act_window_close"}
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": params,
        }
