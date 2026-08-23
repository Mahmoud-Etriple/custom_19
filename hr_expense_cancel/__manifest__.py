{
    "name": "Cancel HR Expense",
    "version": "19.0.1.2.0",
    "category": "Human Resources/Expenses",
    "summary": "Cancel submitted, approved, posted or paid expenses",
    "description": """
Cancel HR Expense
=================
Standard Odoo refuses an expense only while it is Submitted or Approved, and
blocks it outright once a journal entry is posted. This module lets an
authorised user cancel an expense at any stage, including Paid.

Three configurable behaviours:

* **Cancel Only** - the expense becomes Refused.
* **Cancel and Reset to Draft** - the expense returns to Draft for correction.
* **Cancel and Delete** - the expense record is removed.

Works on a single expense from the form and on a selection from the list.

Accounting
----------
Draft journal entries are removed. What happens to a **posted** entry is a
company setting, *Posted Journal Entries*:

* **Reverse the entry** (default) - the original stays and a reversal is
  posted against it. Both remain in the books. This is what core does when
  resetting an expense, and it is the answer an auditor expects.
* **Cancel the entry** - the entry is reset to draft, its reconciliation is
  removed and it is set to Cancelled. It stops affecting the accounts and
  there is no counter-entry. Odoo still refuses this for locked/hashed,
  tax cash basis and exchange difference entries.

Payments are cancelled in both modes, never unlinked, unless they were still
draft - a draft payment is removed.
    """,
    "author": "Etriple Soft",
    "website": "https://www.etriplesoft.com",
    "license": "LGPL-3",
    "depends": ["hr_expense", "account"],
    "data": [
        "security/hr_expense_cancel_groups.xml",
        "views/hr_expense_views.xml",
        "views/res_config_settings_views.xml",
    ],
    "installable": True,
}
