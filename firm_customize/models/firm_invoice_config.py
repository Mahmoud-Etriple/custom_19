""" Initialize Firm Invoice Configuration """

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class FirmPaymentPlan(models.Model):
    """
        Initialize Firm Payment Plan:
         - Configuration list of payment plans referenced by the invoice
           configuration and by the firm contract.
    """
    _name = 'firm.payment.plan'
    _description = 'Firm Payment Plan'
    _order = 'name'

    name = fields.Char(
        required=True,
        translate=True,
    )
    active = fields.Boolean(
        default=True
    )

    _sql_constraints = [
        ('firm_payment_plan_name_uniq',
         'unique(name)',
         'The payment plan name must be unique.'),
    ]


class FirmInvoiceConfig(models.Model):
    """
        Initialize Firm Invoice Configuration:
         - Holds, per target model, how many invoices are generated and which
           payment term / payment plan applies.
    """
    _name = 'firm.invoice.config'
    _description = 'Firm Invoice Configuration'
    _order = 'name'

    name = fields.Char(
        required=True,
        translate=True,
    )
    active = fields.Boolean(
        default=True
    )
    model_id = fields.Many2one(
        'ir.model',
        required=True,
        ondelete='cascade',
    )
    model_name = fields.Char(
        related='model_id.model',
        store=True,
        readonly=True,
        string='Model Technical Name',
    )
    no_of_invoices = fields.Integer(
        string='No. Of Invoices',
        default=1,
        required=True,
    )
    payment_term_id = fields.Many2one(
        'account.payment.term',
    )
    payment_plan_id = fields.Many2one(
        'firm.payment.plan',
    )

    @api.constrains('no_of_invoices')
    def _check_no_of_invoices(self):
        """ The number of invoices must be a positive amount """
        for rec in self:
            if rec.no_of_invoices < 1:
                raise ValidationError(
                    _('The number of invoices must be at least 1.')
                )
