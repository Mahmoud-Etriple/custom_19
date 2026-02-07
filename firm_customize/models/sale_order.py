""" Initialize Sale Order """

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError


class SaleOrder(models.Model):
    """
        Inherit Sale Order:
         -
    """
    _inherit = 'sale.order'

    firm_contract_id = fields.Many2one(
        'firm.contract'
    )