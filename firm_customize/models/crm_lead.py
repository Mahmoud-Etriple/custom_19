""" Initialize Crm Lead """

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError


class CrmLead(models.Model):
    """
        Inherit Crm Lead:
         -
    """
    _inherit = 'crm.lead'

    firm_contract_id = fields.Many2one(
        'firm.contract'
    )