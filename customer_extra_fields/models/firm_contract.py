""" Initialize Firm Contract """

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError


class FirmContract(models.Model):
    """
        Inherit Firm Contract:
         -
    """
    _inherit = 'firm.contract'

    responsible_name = fields.Char(
        related='partner_id.responsible_name',
        store=1,
        readonly=1,
    )
    identification_no = fields.Char(
        related='partner_id.identification_no',
        store=1,
        readonly=1,
    )
    responsible_phone = fields.Char(
        related='partner_id.responsible_phone',
        store=1,
        readonly=1,
    )
    activity_start_date = fields.Date(
        related='partner_id.activity_start_date',
        store=1,
        readonly=1,
    )
    activity_year = fields.Char(
        related='partner_id.activity_year',
        store=1,
        readonly=1,
    )

    legal_form = fields.Selection([
        ('sel_1', 'تضامن'),
        ('sel_2', 'توصية بسيطة'),
        ('sel_3', 'ذات مسئولية محدودة'),
        ('sel_4', 'مساهمة مغلقة '),
        ('sel_5', 'مساهمة مفتوحة '),
        ('sel_6', 'شركة شخص واحد'),
    ],
        default='sel_1',
        related='partner_id.legal_form',
        store=1,
        readonly=1,
    )
    company_law_id = fields.Many2one(
        'company.law',
        related='partner_id.company_law_id',
        store=1,
        readonly=1,
    )
    industry_id = fields.Many2one(
        related='partner_id.industry_id',
        store=1,
        readonly=0,
    )
    industry_code = fields.Char(
        related='partner_id.industry_code',
        store=1,
        readonly=1,
        string='Industry Code'
    )


class FirmTax(models.Model):
    """
        Inherit Firm Tax:
         -
    """
    _inherit = 'firm.tax'
    _rec_name = 'gate_name'

    partner_id = fields.Many2one(
        'res.partner'
    )
    gate_name = fields.Char()


class FirmDocument(models.Model):
    """
        Inherit Firm Document:
         -
    """
    _inherit = 'firm.document'

    partner_id = fields.Many2one(
        'res.partner'
    )