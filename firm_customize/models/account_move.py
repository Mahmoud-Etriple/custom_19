""" Initialize Account Move """

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError


class AccountMove(models.Model):
    """
        Inherit Account Move:
         -
    """
    _inherit = 'account.move'

    firm_contract_id = fields.Many2one(
        'firm.contract'
    )