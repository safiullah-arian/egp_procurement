from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import datetime, date


class PmisDocuments(models.Model):
    _name = "pmis.documents"
    _description = "PMIS Directorates"
    _rec_name = 'number'

    number = fields.Char(string=' Number', required=True)
    subject = fields.Char(string='Subject', required=True)
    type_id = fields.Many2one(
        comodel_name="pmis.document.type",
        string="Document Type",
        readonly=False,
        copy=True,
        tracking=True,
    )
    note = fields.Text(string='Description', required=True)
    attachment = fields.Binary(
        string='Attachment'
    )

    directorates_id = fields.Many2one(
        comodel_name="pmis.directorates",
        string="Document Sender",
        readonly=False,
        copy=True,
        tracking=True,
    )

    # project_id3 = fields.Many2one(
    #     comodel_name="pmis.offerentry",
    #     string="Offer Entry",
    #     readonly=False,
    #     copy=True,
    #     tracking=True,
    # )
    submission_id = fields.Many2one(
        comodel_name="pmis.offersubmission",
        string="Submission Documents",
        readonly=False,
        copy=True,
        tracking=True,
    )

    project_id = fields.Many2one(
        comodel_name="pmis.project",
        string="Project",
        readonly=False,
        copy=True,
        tracking=True,
    )
    purchase_project_id = fields.Many2one(
        comodel_name="pmis.purchase.project",
        string="Purchase",
        readonly=False,
        copy=True,
        tracking=True,
    )
    vendor_id = fields.Many2one(
        comodel_name="pmis.vendors",
        string="Vendor",
        readonly=False,
        copy=True,
        tracking=True,
    )

    delivery_doc_id = fields.Many2one('pmis.delivery.description', string="Delivery Document")
    purchase_quotation_id = fields.Many2one('pmis.quotation', string="Purchase Quotation")
    purchase_id = fields.Many2one('pmis.purchase.kharidari', string="Purchase")
    purchase_quotation_line_id = fields.Many2one(
        comodel_name="pmis.purchase.quotation",
        string='Quotation Line',
        readonly=False,
        copy=True,
    )

    delivery_doc_id = fields.Many2one('pmis.delivery.description', string="Delivery Document")

    contract_management_doc_id = fields.Many2one('pmis.contract.management', string="Contract Management Document")


class DocumentType(models.Model):
    _name = "pmis.document.type"
    _description = "Document Type "

    name = fields.Char(string='Type Name', required=True)
