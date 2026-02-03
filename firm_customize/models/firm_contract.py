""" Initialize Firm Contract """

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError


class FirmContract(models.Model):
    """
        Initialize Firm Contract:
         -
    """
    _name = 'firm.contract'
    _description = 'Firm Contract'

    name = fields.Char(
        required=True,
        translate=True,
        string='Contract No'
    )
    active = fields.Boolean(
        default=True
    )
    partner_id = fields.Many2one(
        'res.partner'
    )
    parent_id = fields.Many2one(
        'res.partner',
        related='partner_id.parent_id',
        store=1,
    )
    start_date = fields.Date()
    end_date = fields.Date()
    company_type = fields.Selection(
        related='partner_id.company_type',
        store=1,
        readonly=0,
    )
    person_legal_form = fields.Selection(
        [('person', 'شركة فردية')],
        default='person',
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
    )
    description = fields.Html()
    state = fields.Selection(
        [('draft', 'Draft'),
         ('approve', 'Approved'),
         ('cancel', 'Cancelled')],
        default='draft',
        string='Status'
    )
    firm_document_ids = fields.One2many(
        'firm.document',
        'firm_contract_id'
    )
    firm_services_ids = fields.One2many(
        'firm.services',
        'firm_contract_id'
    )
    firm_tax_ids = fields.One2many(
        'firm.tax',
        'firm_contract_id'
    )


class FirmDocument(models.Model):
    """
        Initialize Firm Document:
         -
    """
    _name = 'firm.document'
    _description = 'Firm Document'

    name = fields.Char(
        required=True,
        string='Document No',
    )
    document_type_id = fields.Many2one(
        'firm.document.type'
    )
    issuing_office_id = fields.Many2one(
        'issuing.office'
    )
    state = fields.Selection(
        [('active', 'Active'),
         ('not', 'Not Active')],
        default='active',
        string='Status'
    )
    last_update_date = fields.Date()
    alert_days = fields.Integer()
    alert_users_ids = fields.Many2many(
        'res.users'
    )
    folder_path = fields.Char()
    firm_contract_id = fields.Many2one(
        'firm.contract'
    )


class FirmServices(models.Model):
    """
        Initialize Firm Services:
         -
    """
    _name = 'firm.services'
    _description = 'Firm Services'

    category_id = fields.Many2one(
        'product.category'
    )
    product_id = fields.Many2one(
        'product.product',
        domain="[('categ_id', '=', category_id)]"
    )
    uom_id = fields.Many2one(
        'uom.uom',
        string='Unit Of Measure'
    )
    quantity = fields.Float()
    price = fields.Float()
    total = fields.Float(
        compute='_compute_total'
    )
    firm_contract_id = fields.Many2one(
        'firm.contract'
    )

    @api.depends('quantity', 'price')
    def _compute_total(self):
        """ Compute total value """
        for rec in self:
            rec.total = rec.quantity * rec.price


class FirmTax(models.Model):
    """
        Initialize Firm Tax:
         -
    """
    _name = 'firm.tax'
    _description = 'Firm Tax'

    gate_link = fields.Char(
        required=True,
    )
    user_name = fields.Char()
    password = fields.Char()
    firm_contract_id = fields.Many2one(
        'firm.contract'
    )