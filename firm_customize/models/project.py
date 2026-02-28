""" Initialize Project """

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError


class ProjectProject(models.Model):
    """
        Inherit Project Project:
         -
    """
    _inherit = 'project.project'

    firm_contract_id = fields.Many2one(
        'firm.contract'
    )

    service_type_ids = fields.Many2many(
        'service.type'
    )

    @api.constrains('reinvoiced_sale_order_id')
    def _check_reinvoiced_sale_order_id(self):
        """ Validate reinvoiced_sale_order_id """
        for rec in self:
            if rec.reinvoiced_sale_order_id and rec.reinvoiced_sale_order_id.firm_contract_id:
                rec.firm_contract_id = rec.reinvoiced_sale_order_id.firm_contract_id
                rec.account_id = rec.reinvoiced_sale_order_id.firm_contract_id.analytic_account_id


class ProjectTask(models.Model):
    """
        Inherit Project Task:
         -
    """
    _inherit = 'project.task'

    firm_contract_id = fields.Many2one(
        'firm.contract',
        related='project_id.firm_contract_id',
        store=1
    )

    @api.constrains('sale_line_id')
    def _check_sale_line_id(self):
        """ Validate sale_line_id """
        for rec in self:
            if rec.sale_line_id and rec.sale_line_id.order_id.firm_contract_id:
                rec.project_id.firm_contract_id = rec.sale_line_id.order_id.firm_contract_id
                if rec.firm_contract_id:
                    service = rec.firm_contract_id.firm_services_ids.filtered(lambda x: x.product_id == rec.sale_line_id.product_id)
                    if service:
                        rec.project_id.service_type_ids = service.firm_contract_id.service_type_ids.ids
                        rec.project_id.description = service.scope
                        rec.project_id.user_id = service.project_manager_id.id
                        rec.user_ids = service.assignee_ids.ids
