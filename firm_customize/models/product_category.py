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