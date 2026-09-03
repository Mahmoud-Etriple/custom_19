""" Initialize Firm Automatic Invoice Plan """

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class FirmInvoiceConfig(models.Model):
    """
        Initialize Firm Automatic Invoice Plan:
         - Names an automatic invoicing scheme and the model it applies to.
         - The invoicing figures themselves live on its plans.
    """
    _name = 'firm.invoice.config'
    _description = 'Automatic Invoice Plan'
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


class FirmPaymentPlan(models.Model):
    """
        Initialize Firm Plan:
         - Carries the invoicing figures of an automatic invoice plan:
           payment term and number of invoices.
    """
    _name = 'firm.payment.plan'
    _description = 'Plan'
    _order = 'invoice_config_id, name'

    name = fields.Char(
        required=True,
        translate=True,
    )
    active = fields.Boolean(
        default=True
    )
    invoice_config_id = fields.Many2one(
        'firm.invoice.config',
        string='Automatic Invoice Plan',
        required=True,
        ondelete='cascade',
    )
    payment_term_id = fields.Many2one(
        'account.payment.term',
    )
    no_of_invoices = fields.Integer(
        string='No. Of Invoices',
        default=1,
        required=True,
    )

    _sql_constraints = [
        ('firm_payment_plan_name_uniq',
         'unique(invoice_config_id, name)',
         'The plan name must be unique inside an automatic invoice plan.'),
    ]

    @api.constrains('no_of_invoices')
    def _check_no_of_invoices(self):
        """ The number of invoices must be a positive amount """
        for rec in self:
            if rec.no_of_invoices < 1:
                raise ValidationError(
                    _('The number of invoices must be at least 1.')
                )
