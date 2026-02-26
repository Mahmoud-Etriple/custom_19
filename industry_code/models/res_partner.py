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

    industry_code = fields.Char()
    
    
class ResPartnerIndustry(models.Model):
    """
        Inherit Res Partner Industry:
         - 
    """
    _inherit = 'res.partner.industry'
    
    code = fields.Char()