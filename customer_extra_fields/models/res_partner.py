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

    responsible_name = fields.Char()
    identification_no = fields.Char()
    responsible_phone = fields.Char()
    activity_start_date = fields.Date()
    activity_year = fields.Char()

    legal_form = fields.Selection([
        ('sel_1', 'تضامن'),
        ('sel_2', 'توصية بسيطة'),
        ('sel_3', 'ذات مسئولية محدودة'),
        ('sel_4', 'مساهمة مغلقة '),
        ('sel_5', 'مساهمة مفتوحة '),
        ('sel_6', 'شركة شخص واحد'),
    ],
        default='sel_1',
    )
    company_law_id = fields.Many2one(
        'company.law'
    )
    industry_code = fields.Char(
        related='industry_id.code',
        store=1,
        readonly=1,
        string='Industry Code'
    )

    firm_tax_ids = fields.One2many(
        'firm.tax',
        'partner_id'
    )
    is_eta = fields.Boolean()
    token_end_date = fields.Date()

    firm_document_ids = fields.One2many(
        'firm.document',
        'partner_id'
    )