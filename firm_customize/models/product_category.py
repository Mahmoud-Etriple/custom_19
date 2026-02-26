""" Initialize Product Category """

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError


class ProductCategory(models.Model):
    """
        Inherit Product Category:
         -
    """
    _inherit = 'product.category'

    services_type = fields.Selection(
        [('accounting', 'Accounting'),
         ('audit', 'Audit'),
         ('tax', 'Tax'),
         ('incorporation', 'Incorporation'),
         ('consulting', 'Consulting'),
         ('legal', 'Legal')],
        default='accounting',
    )

    service_type_id = fields.Many2one(
        'service.type'
    )

    service_tag_ids = fields.Many2many(
        'product.tag',
        compute='_compute_service_tag_ids'
    )

    def _compute_service_tag_ids(self):
        """ Compute service_tag_ids value """
        for rec in self:
            rec.service_tag_ids = None
            products = self.env['product.template'].search([
                ('categ_id', '=', rec.id)
            ])
            if products:
                rec.service_tag_ids = products.mapped('product_tag_ids')
