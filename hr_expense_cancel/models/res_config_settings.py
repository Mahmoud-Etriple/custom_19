from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    expense_cancel_enabled = fields.Boolean(
        related="company_id.expense_cancel_enabled",
        string="Expense Cancel Feature",
        readonly=False,
    )
    expense_cancel_mode = fields.Selection(
        related="company_id.expense_cancel_mode",
        string="On Cancel",
        readonly=False,
    )
