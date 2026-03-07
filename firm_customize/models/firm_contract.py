""" Initialize Firm Contract """

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError
from datetime import timedelta


class FirmContract(models.Model):
    """
        Initialize Firm Contract:
         -
    """
    _name = 'firm.contract'
    _description = 'Firm Contract'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(
        required=False,
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

    services_type = fields.Selection(
        [('accounting', 'Accounting'),
         ('audit', 'Audit'),
         ('tax', 'Tax'),
         ('incorporation', 'Incorporation'),
         ('consulting', 'Consulting'),
         ('legal', 'Legal')],
        default='accounting',
    )
    service_type_ids = fields.Many2many(
        'service.type'
    )
    company_law_id = fields.Many2one(
        'company.law'
    )
    country_id = fields.Many2one(
        related='partner_id.country_id',
        store=1,
        readonly=0,
    )
    industry_id = fields.Many2one(
        related='partner_id.industry_id',
        store=1,
        readonly=0,
    )
    industry_code = fields.Char(
        related='industry_id.code',
        store=1,
        readonly=1,
        string='Industry Code'
    )
    responsible_name = fields.Char()
    identification_no = fields.Char()
    responsible_phone = fields.Char()
    start_date = fields.Date()
    end_date = fields.Date()
    activity_start_date = fields.Date()
    activity_year = fields.Char()
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
    contract_doc = fields.Binary()
    description = fields.Html()
    state = fields.Selection(
        [('draft', 'Draft'),
         ('approve', 'Approved'),
         ('done', 'Done'),
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
        'firm_contract_id',
        copy=True
    )
    firm_tax_ids = fields.One2many(
        'firm.tax',
        'firm_contract_id'
    )
    is_eta = fields.Boolean()
    token_end_date = fields.Date()
    analytic_account_id = fields.Many2one(
        'account.analytic.account'
    )

    service_tag_ids = fields.Many2many(
        'product.tag',
        # compute='_compute_service_tag_ids'
    )

    # @api.onchange('service_type_ids')
    # def _check_service_type_ids(self):
    #     """ Validate service_type_ids """
    #     for rec in self:
    #         if rec.service_type_ids:
    #             rec._compute_service_tag_ids()

    def _compute_service_tag_ids(self):
        """ Compute service_tag_ids value """
        for rec in self:
            rec.service_tag_ids = None
            products = self.env['product.category'].search([
                ('service_type_id', 'in', rec.service_type_ids.ids)
            ])
            if products:
                rec.service_tag_ids = products.mapped('service_tag_ids')

    @api.model
    def create(self, vals_list):
        """
            Override create method
             - sequence name
        """
        res = super(FirmContract, self).create(vals_list)
        sequence = self.env['ir.sequence'].next_by_code('firm.contract')
        res['name'] = sequence
        return res

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

    def action_view_firm_calender(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Firm Contract'),
            'res_model': 'firm.contract',
            'view_mode': 'calendar',
            'domain': [('id', '=', self.id)],
        }

    def action_view_firm_activity(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Firm Contract'),
            'res_model': 'firm.contract',
            'view_mode': 'activity',
            'domain': [('id', '=', self.id)],
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

    def action_view_payment(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Payments'),
            'res_model': 'account.payment',
            'view_mode': 'list,form',
            'domain': [('firm_contract_id', '=', self.id)],
            'context': {
                'default_firm_contract_id': self.id,
                'default_payment_type': 'inbound',
                'default_partner_type': 'customer'
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

    def action_done(self):
        """ Action Approve """
        for rec in self:
            rec.state = 'done'

    def action_draft(self):
        """ Action Approve """
        for rec in self:
            rec.state = 'draft'

    def action_approve(self):
        """ Action Approve """
        for rec in self:
            rec.state = 'approve'
            analytic_account_id = False
            if rec.name:
                rec.analytic_account_id = self.env['account.analytic.account'].create({
                    'name': rec.name,
                    'plan_id': 1
                })
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
                        'analytic_distribution': {rec.analytic_account_id.id: 100}
                    })
                sale.action_confirm()


class FirmDocument(models.Model):
    """
        Initialize Firm Document:
         -
    """
    _name = 'firm.document'
    _description = 'Firm Document'
    _inherit = ['mail.thread', 'mail.activity.mixin']

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
    activity_type_id = fields.Many2one(
        'mail.activity.type'
    )

    def action_send_activity(self):
        """ Action Send Activity """
        for rec in self:
            if rec.alert_users_ids:
                summary = 'Renew Document For ' + rec.partner_id.name + ' - ' + rec.name
                for user in rec.alert_users_ids:
                    rec.activity_schedule(
                        activity_type_id=rec.activity_type_id.id,
                        user_id=user.id,
                        summary=summary,
                        note=summary,
                        date_deadline=fields.Date.today()
                    )
    def action_schedule_document(self):
        """ Action Schedule Document """
        records = self.env['firm.document'].search([
            ('last_update_date', '!=', False)
        ])
        today = fields.Date.today()
        if records:
            for record in records:
                if record.last_update_date + timedelta(days=record.alert_days) >= today:
                    record.action_send_activity()


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
    quantity = fields.Float(
        default=1
    )
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