Cancel HR Expense
=================

Standard Odoo 19 refuses an expense only while it is **Submitted** or
**Approved**, and ``_do_refuse`` raises outright once a journal entry is
posted. This module lets an authorised user cancel an expense at any stage,
including **Paid**.

Configuration
-------------

*Settings → Expenses → Expense Cancel Feature*. Tick it, then choose:

* **Cancel Only** — the expense becomes Refused.
* **Cancel and Reset to Draft** — the expense returns to Draft for correction.
* **Cancel and Delete** — the expense record is removed.

Assign **Cancel Expenses** (Human Resources → Expense Cancellation privilege)
to the users allowed to do this. Expense Managers get it automatically.

Usage
-----

A **Cancel** button appears in the expense form header once the feature is on
and the expense is past Draft. The expense list has a **Cancel Expenses**
header button for acting on a selection.

Accounting behaviour
--------------------

Posted journal entries are **reversed**, never deleted; draft entries are
removed. This mirrors what core ``action_reset`` does and keeps the books
auditable.

Under **Cancel and Delete** the expense record goes but the original entry
and its reversal remain. That is deliberate: deleting posted accounting
entries is not something a module should do.

If the expense was already **Paid**, its ``account.payment`` is cancelled
(never deleted) before the journal entry is reversed, for the same reason.
This covers both payment modes: for *own account* reimbursements the
payment is a separate entry reconciled against the expense's payable
line; for *company account* expenses the payment's move **is** the
expense's own entry, so cancelling it cancels that entry directly instead
of reversing it. Draft payments, which have nothing posted to preserve,
are removed.

Note on Odoo 19
---------------

``hr.expense.sheet`` was removed in Odoo 19, so there are no expense reports
to cancel — expenses are standalone and carry their own approval and payment
states. ``hr.expense.state`` is a stored compute that gives priority to
``account_move_id``: an expense keeps reporting *Paid* until the move is
detached, whatever is written to ``approval_state``. Reversing and detaching
the move is therefore required for the cancellation to be visible at all,
not merely good accounting hygiene.
