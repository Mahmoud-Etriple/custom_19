""" Initialize Hr Expense """

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError


class HrExpense(models.Model):
    """
        Inherit Hr Expense:
         -
    """
    _inherit = 'hr.expense'

    firm_contract_id = fields.Many2one(
        'firm.contract'
    )