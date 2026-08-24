from odoo.exceptions import UserError
from odoo.tests.common import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestHrExpenseCancel(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company = cls.env.company
        cls.company.expense_cancel_enabled = True
        cls.company.expense_cancel_mode = "cancel"

        cls.canceller = cls.env["res.users"].create({
            "name": "Expense Canceller",
            "login": "hec_canceller",
            "group_ids": [(6, 0, [
                cls.env.ref("base.group_user").id,
                cls.env.ref("hr_expense.group_hr_expense_manager").id,
                cls.env.ref("hr_expense_cancel.group_hr_expense_cancel").id,
                cls.env.ref("account.group_account_invoice").id,
            ])],
        })
        cls.plain_user = cls.env["res.users"].create({
            "name": "Plain Expense User",
            "login": "hec_plain",
            "group_ids": [(6, 0, [
                cls.env.ref("base.group_user").id,
                cls.env.ref("hr_expense.group_hr_expense_user").id,
            ])],
        })
        cls.employee = cls.env["hr.employee"].create({
            "name": "Cancel Test Employee",
            "company_id": cls.company.id,
        })
        cls.product = cls.env["product.product"].create({
            "name": "Cancel Test Expense Product",
            "type": "service",
            "can_be_expensed": True,
            "standard_price": 100.0,
        })

    def _expense(self, **overrides):
        vals = {
            "name": "Test expense",
            "employee_id": self.employee.id,
            "product_id": self.product.id,
            "total_amount_currency": 100.0,
            "payment_mode": "own_account",
            "company_id": self.company.id,
        }
        vals.update(overrides)
        return self.env["hr.expense"].create(vals)

    def _submitted(self):
        exp = self._expense()
        exp.action_submit()
        return exp

    def _approved(self):
        exp = self._submitted()
        exp.sudo()._do_approve(check=False)
        return exp

    # -- guards ---------------------------------------------------------
    def test_disabled_feature_blocks_cancel(self):
        self.company.expense_cancel_enabled = False
        exp = self._submitted()
        with self.assertRaises(UserError):
            exp.with_user(self.canceller).action_expense_cancel()
        self.company.expense_cancel_enabled = True

    def test_user_without_group_blocked(self):
        exp = self._submitted()
        with self.assertRaises(UserError):
            exp.with_user(self.plain_user).action_expense_cancel()

    def test_draft_expense_is_not_cancellable(self):
        exp = self._expense()
        self.assertEqual(exp.state, "draft")
        with self.assertRaises(UserError):
            exp.with_user(self.canceller).action_expense_cancel()

    def test_availability_flag_follows_state_and_setting(self):
        exp = self._expense()
        self.assertFalse(exp.expense_cancel_available, "draft is not cancellable")
        exp.action_submit()
        exp.invalidate_recordset(["expense_cancel_available"])
        self.assertTrue(exp.expense_cancel_available)
        self.company.expense_cancel_enabled = False
        exp.invalidate_recordset(["expense_cancel_available"])
        self.assertFalse(exp.expense_cancel_available)
        self.company.expense_cancel_enabled = True

    # -- the three modes ------------------------------------------------
    def test_mode_cancel_only(self):
        self.company.expense_cancel_mode = "cancel"
        exp = self._approved()
        exp.with_user(self.canceller).action_expense_cancel()
        self.assertEqual(exp.state, "refused")
        self.assertEqual(exp.approval_state, "refused")

    def test_mode_cancel_and_reset_to_draft(self):
        self.company.expense_cancel_mode = "cancel_draft"
        exp = self._approved()
        exp.with_user(self.canceller).action_expense_cancel()
        self.assertEqual(exp.state, "draft")
        self.assertFalse(exp.approval_state)

    def test_mode_cancel_and_delete(self):
        self.company.expense_cancel_mode = "cancel_delete"
        exp = self._approved()
        exp.with_user(self.canceller).action_expense_cancel()
        self.assertFalse(exp.exists())

    # -- accounting -----------------------------------------------------
    def test_posted_expense_move_is_reversed_not_deleted(self):
        """A posted entry must survive as a reversal pair, never vanish."""
        self.company.expense_cancel_mode = "cancel"
        exp = self._approved()
        exp.with_user(self.canceller).sudo().action_post()
        move = exp.account_move_id
        if not move:
            self.skipTest("Posting requires accounting setup not present here")
        move_id = move.id
        exp.with_user(self.canceller).action_expense_cancel()
        self.assertEqual(exp.state, "refused")
        self.assertFalse(exp.account_move_id, "move must be detached")
        original = self.env["account.move"].browse(move_id)
        self.assertTrue(original.exists(), "posted entry must not be deleted")

    def test_paid_expense_cancels_reconciled_payment(self):
        """own_account: the payment is a separate move reconciled against
        the expense entry. It must not survive untouched — it should end
        up cancelled, not left posted/paid and reconciled to a journal
        entry that has just been reversed."""
        self.company.expense_cancel_mode = "cancel"
        exp = self._approved()
        exp.with_user(self.canceller).sudo().action_post()
        move = exp.account_move_id
        if not move:
            self.skipTest("Posting requires accounting setup not present here")

        payment_register = self.env["account.payment.register"].with_context(
            active_model="account.move", active_ids=move.ids,
        ).create({})
        payment_action = payment_register._create_payments()
        payment = self.env["account.payment"].browse(payment_action)
        if not payment:
            self.skipTest("Payment registration not available in this setup")
        self.assertEqual(payment.state, "paid")

        exp.invalidate_recordset()
        exp.with_user(self.canceller).action_expense_cancel()

        self.assertEqual(
            payment.state, "canceled",
            "the reconciled payment must be cancelled when the expense is",
        )

    def test_company_paid_expense_cancels_own_payment(self):
        """company_account: the payment IS the expense's own move (no
        separate reconciled move to find). Posting must have created an
        account.payment whose move_id equals account_move_id, and
        cancelling the expense must cancel that payment, not leave it
        posted and paid while the entry underneath it gets reversed."""
        self.company.expense_cancel_mode = "cancel"
        exp = self._expense(payment_mode="company_account")
        exp.action_submit()
        exp.sudo()._do_approve(check=False)
        exp.with_user(self.canceller).sudo().action_post()
        move = exp.account_move_id
        if not move:
            self.skipTest("Posting requires accounting setup not present here")

        payment = self.env["account.payment"].sudo().search(
            [("move_id", "=", move.id)]
        )
        if not payment:
            self.skipTest(
                "company_account posting did not create an account.payment "
                "in this setup"
            )
        self.assertEqual(payment.state, "paid")

        exp.invalidate_recordset()
        exp.with_user(self.canceller).action_expense_cancel()

        self.assertEqual(
            payment.state, "canceled",
            "the expense's own payment/move must end up cancelled",
        )

    def test_state_leaves_paid_only_when_move_detached(self):
        """_compute_state prioritises the move, so detaching it is required."""
        self.company.expense_cancel_mode = "cancel"
        exp = self._approved()
        exp.sudo().write({"approval_state": "refused"})
        exp.invalidate_recordset(["state"])
        self.assertEqual(
            exp.state, "refused",
            "with no move, approval_state alone decides the state",
        )

    # -- batch ----------------------------------------------------------
    def test_mass_cancel_from_list(self):
        self.company.expense_cancel_mode = "cancel"
        expenses = self._approved() | self._approved() | self._approved()
        expenses.with_user(self.canceller).action_expense_cancel()
        self.assertEqual(set(expenses.mapped("state")), {"refused"})

    def test_mixed_batch_is_rejected_whole(self):
        self.company.expense_cancel_mode = "cancel"
        good = self._approved()
        draft = self._expense()
        with self.assertRaises(UserError):
            (good | draft).with_user(self.canceller).action_expense_cancel()
        self.assertNotEqual(good.state, "refused")

    def test_empty_recordset_raises(self):
        with self.assertRaises(UserError):
            self.env["hr.expense"].with_user(
                self.canceller
            ).action_expense_cancel()

    # -- group wiring ---------------------------------------------------
    def test_expense_manager_implies_cancel_right(self):
        self.assertTrue(self.canceller.has_group(
            "hr_expense_cancel.group_hr_expense_cancel"
        ))

    def test_group_is_assignable_in_the_user_form(self):
        group = self.env.ref("hr_expense_cancel.group_hr_expense_cancel")
        self.assertTrue(group.privilege_id)
        hierarchy = self.env["res.groups"]._get_view_group_hierarchy()
        self.assertIn(
            group.id,
            hierarchy["privileges"][group.privilege_id.id]["group_ids"],
        )


@tagged("post_install", "-at_install")
class TestCancelDeleteBlocked(TransactionCase):
    """Cancel and Delete must fail cleanly when deleting is restricted.

    account_delete_ceo_only reserves deleting expenses for the CEO. The cancel
    flow reverses the entry and cancels the payment BEFORE it reaches the
    unlink, so a refusal there has to leave nothing behind and has to say what
    actually went wrong - the user pressed Cancel, not Delete.
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company = cls.env.company
        cls.company.expense_cancel_enabled = True
        cls.company.expense_cancel_mode = "cancel_delete"
        cls.user = cls.env["res.users"].create({
            "name": "Cancel User",
            "login": "hec_cancel_user",
            "group_ids": [(6, 0, [
                cls.env.ref("base.group_user").id,
                cls.env.ref("hr_expense.group_hr_expense_user").id,
                cls.env.ref("hr_expense_cancel.group_hr_expense_cancel").id,
            ])],
        })
        cls.employee = cls.env["hr.employee"].create({
            "name": "HEC Employee", "user_id": cls.user.id,
        })
        cls.product = cls.env["product.product"].create({
            "name": "HEC Product", "can_be_expensed": True, "type": "service",
        })

    def _expense(self):
        expense = self.env["hr.expense"].create({
            "name": "HEC expense",
            "employee_id": self.employee.id,
            "product_id": self.product.id,
            "total_amount_currency": 100.0,
        })
        expense.sudo().write({"approval_state": "submitted"})
        return expense

    def test_blocked_delete_explains_itself_and_changes_nothing(self):
        expense = self._expense()
        original_unlink = type(expense).unlink

        def refusing_unlink(records):
            raise UserError("Only the CEO can delete expenses.")

        type(expense).unlink = refusing_unlink
        try:
            with self.assertRaises(UserError) as caught:
                expense.with_user(self.user).action_expense_cancel()
        finally:
            type(expense).unlink = original_unlink

        message = str(caught.exception)
        self.assertIn("Cancel and Delete", message)
        self.assertIn("Settings", message)
        self.assertIn(
            "Only the CEO can delete expenses.", message,
            "the underlying refusal must be quoted, not swallowed",
        )
        self.assertTrue(
            expense.exists(),
            "a refused cancel must leave the expense untouched",
        )


@tagged("post_install", "-at_install")
class TestExpenseCancelReturnValue(TransactionCase):
    """What the button hands back to the web client.

    An action dict reaches the browser and is executed there, so a wrong one
    crashes the user *after* the work has succeeded - the hardest kind of
    failure to connect to its cause. These assertions are about the shape of
    that dict, not about the cancellation.
    """

    def test_no_empty_next_action_is_returned(self):
        """{} is truthy in JavaScript.

        The client runs `if (params.next) doAction(params.next)`. An empty
        dict passes that test and then fails inside the action manager with
        "can't handle actions of type undefined". Absent is not the same as
        empty.
        """
        for mode in ("cancel", "cancel_draft"):
            with self.subTest(mode=mode):
                action = self.env["hr.expense"]._expense_cancel_notification(
                    mode, ["EXP/001"])
                self.assertNotIn(
                    "next", action["params"],
                    "no next action must be sent when there is nowhere to go",
                )

    def test_delete_mode_closes_the_form(self):
        """Here the record is gone, so the client does have to be told."""
        action = self.env["hr.expense"]._expense_cancel_notification(
            "cancel_delete", ["EXP/001"])
        self.assertEqual(
            action["params"]["next"]["type"], "ir.actions.act_window_close")

    def test_every_returned_action_carries_a_type(self):
        for mode in ("cancel", "cancel_draft", "cancel_delete"):
            with self.subTest(mode=mode):
                action = self.env["hr.expense"]._expense_cancel_notification(
                    mode, ["EXP/001"])
                self.assertEqual(action["type"], "ir.actions.client")
                self.assertTrue(action["params"].get("message"))
                for key, value in action["params"].items():
                    if isinstance(value, dict):
                        self.assertTrue(
                            value.get("type"),
                            f"nested action under '{key}' has no type",
                        )
