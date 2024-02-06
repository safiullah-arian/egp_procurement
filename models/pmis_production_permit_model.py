from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import datetime, date


class ProductionPermit(models.Model):
    _name = "production.permit"
    _inherit = ['mail.thread']
    _description = "Production Permit"

    product_description_id = fields.Many2one(
        comodel_name="pmis.products.description",
        string="Products ",
        readonly=False,
    )
    date = fields.Date(string="Date", default=fields.Date.context_today)
    note = fields.Text(string="Note")
    product_permit_id = fields.Many2one('pmis.offersubmission', string='offer submission')
    production_company_id = fields.Many2one('pmis.production.company', string='Producer Name')


class PmisProductionCompany(models.Model):
    _name = "pmis.production.company"
    _description = "Production company"
    _rec_name = "name"

    name = fields.Char(string="Producer's Name")
    address = fields.Text(string="Manufacturer's Address")
    representative = fields.Char(string="Manufacturer's Representative")
    representative_job = fields.Char(string="Job of Representative")
