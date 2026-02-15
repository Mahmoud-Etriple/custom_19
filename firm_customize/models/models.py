""" Initialize Models """

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError


class FirmDocumentType(models.Model):
    """
        Initialize Firm Document Type:
         - 
    """
    _name = 'firm.document.type'
    _description = 'Firm Document Type'

    name = fields.Char(
        required=True,
        translate=True,
    )


class CompanyLaw(models.Model):
    """
        Initialize Firm Document Type:
         -
    """
    _name = 'company.law'
    _description = 'Company Law'

    name = fields.Char(
        required=True,
        translate=True,
    )


class ServiceType(models.Model):
    """
        Initialize Firm Document Type:
         -
    """
    _name = 'service.type'
    _description = 'Service Type'

    name = fields.Char(
        required=True,
        translate=True,
    )


class FirmDocumentTag(models.Model):
    """
        Initialize Firm Document Type:
         -
    """
    _name = 'firm.document.tag'
    _description = 'Firm Document Tag'

    name = fields.Char(
        required=True,
        translate=True,
    )


class IssuingOffice(models.Model):
    """
        Initialize Issuing Office:
         -
    """
    _name = 'issuing.office'
    _description = 'Issuing Office'

    name = fields.Char(
        required=True,
        translate=True,
    )
