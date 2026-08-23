from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    expense_cancel_enabled = fields.Boolean(
        string="Expense Cancel Feature",
        help="Allow authorised users to cancel expenses that have already "
             "been submitted, approved, posted or paid.",
    )
    expense_cancel_mode = fields.Selection(
        selection=[
            ("cancel", "Cancel Only"),
            ("cancel_draft", "Cancel and Reset to Draft"),
            ("cancel_delete", "Cancel and Delete"),
        ],
        string="On Cancel",
        default="cancel",
        required=True,
        help="Cancel Only: the expense is refused.\n"
             "Cancel and Reset to Draft: the expense returns to draft so it "
             "can be corrected and resubmitted.\n"
             "Cancel and Delete: the expense record is removed. Journal "
             "entries are handled per the setting below.",
    )
