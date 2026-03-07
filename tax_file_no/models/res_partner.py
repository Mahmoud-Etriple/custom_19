""" Initialize Sale Order """

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError


class ResPartner(models.Model):
    """
        Inherit Sale Order:
         -
    """
    _inherit = 'res.partner'

    tax_file_no = fields.Char()
    person_legal_form = fields.Selection(
        [('person', 'شركة فردية')],
        default='person',
    )