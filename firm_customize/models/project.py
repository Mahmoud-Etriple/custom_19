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
