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
    _inherit = ['mail.thread', 'mail.activity.mixin']

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
    vat = fields.Char(
        related='partner_id.vat',
        store=1,
        readonly=0,
    )
    street = fields.Char(
        related='partner_id.street',
        store=1,
        readonly=0,
    )

    street2 = fields.Char(
        related='partner_id.street2',
        store=1,
        readonly=0,
    )

    city = fields.Char(
        related='partner_id.city',
        store=1,
        readonly=0,
    )

    state_id = fields.Many2one(
        related='partner_id.state_id',
        store=1,
        readonly=0,
    )

    zip = fields.Char(
        related='partner_id.zip',
        store=1,
        readonly=0,
    )

    country_id = fields.Many2one(
        related='partner_id.country_id',
        store=1,
        readonly=0,
    )
    responsible_name = fields.Char()
    responsible_phone = fields.Char()
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

    def action_view_crm(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Opportunity'),
            'res_model': 'crm.lead',
            'view_mode': 'list,form',
            'domain': [('firm_contract_id', '=', self.id)],
            'context': {
                'default_firm_contract_id': self.id,
            },
        }

    def action_view_expense(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Expenses'),
            'res_model': 'hr.expense',
            'view_mode': 'list,form',
            'domain': [('firm_contract_id', '=', self.id)],
            'context': {
                'default_firm_contract_id': self.id,
            },
        }

    def action_view_sale(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Sales Orders'),
            'res_model': 'sale.order',
            'view_mode': 'list,form',
            'domain': [('firm_contract_id', '=', self.id)],
            'context': {
                'default_firm_contract_id': self.id,
            },
        }

    def action_view_project(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Projects'),
            'res_model': 'project.project',
            'view_mode': 'list,form',
            'domain': [('firm_contract_id', '=', self.id)],
            'context': {
                'default_firm_contract_id': self.id,
            },
        }


    def action_view_task(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Tasks'),
            'res_model': 'project.task',
            'view_mode': 'list,form',
            'domain': [('firm_contract_id', '=', self.id)],
            'context': {
                'default_firm_contract_id': self.id,
            },
        }


    def action_view_bill(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Vendor Bills'),
            'res_model': 'account.move',
            'view_mode': 'list,form',
            'domain': [('firm_contract_id', '=', self.id),('move_type', '=', 'in_invoice')],
            'context': {
                'default_partner_id': self.id,
                'default_firm_contract_id': self.id,
                'default_move_type': 'in_invoice',
            },
        }

    def action_view_invoice(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Customer Invoice'),
            'res_model': 'account.move',
            'view_mode': 'list,form',
            'domain': [('firm_contract_id', '=', self.id),('move_type', '=', 'out_invoice')],
            'context': {
                'default_partner_id': self.id,
                'default_firm_contract_id': self.id,
                'default_move_type': 'out_invoice',
            },
        }

    def action_cancel(self):
        """ Action Approve """
        for rec in self:
            rec.state = 'cancel'

    def action_draft(self):
        """ Action Approve """
        for rec in self:
            rec.state = 'draft'

    def action_approve(self):
        """ Action Approve """
        for rec in self:
            rec.state = 'approve'
            if rec.firm_services_ids:
                sale = self.env['sale.order'].create({
                    'partner_id': rec.partner_id.id,
                    'firm_contract_id': rec.id
                })
                for line in rec.firm_services_ids:
                    self.env['sale.order.line'].create({
                        'product_id': line.product_id.id,
                        'product_uom_qty': line.quantity,
                        'product_uom_id': line.product_id.uom_id.id,
                        'price_unit': line.price,
                        'order_id': sale.id,
                    })


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
    tag_ids = fields.Many2many(
        'firm.document.tag'
    )
    attachment_ids = fields.Many2many(
        'ir.attachment'
    )



class FirmServices(models.Model):
    """
        Initialize Firm Services:
         -
    """
    _name = 'firm.services'
    _description = 'Firm Services'
    
    scope = fields.Char()
    project_manager_id = fields.Many2one(
        'res.users'
    )
    assignee_ids = fields.Many2many(
        'res.users'
    )
    category_id = fields.Many2one(
        'product.category'
    )
    product_id = fields.Many2one(
        'product.product',
        domain="[('categ_id', '=', category_id)]"
    )
    uom_id = fields.Many2one(
        'uom.uom',
        string='Unit Of Measure',
        related='product_id.uom_id'
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