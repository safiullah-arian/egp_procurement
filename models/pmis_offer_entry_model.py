from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import datetime, date


class PmisOfferEntry(models.Model):
    _name = 'pmis.offerentry'
    _inherit = ['mail.thread']
    _description = 'Pmis Offer Entry to the system after the office got the Offer from Clints'

    project_id = fields.Many2one('pmis.project', string='Project')
    receved_offer = fields.Many2one('pmis.offersubmission', string='Receved Offer')
    project_number = fields.Char(string='Project Number')
    project_name = fields.Char(string='Project Name')
    date = fields.Date(string='Date')
    # company_name = fields.Many2one('pmis.company', string='Company Name')
    company_name = fields.Char(string='Company Name')
    ref = fields.Char(string='Ref')
    note = fields.Text(string='Note')

    # Products related to the project
    products_ids = fields.One2many('pmis.products', 'project_id2', string='Products')

    # Documents related to the project
    documents_ids = fields.One2many('pmis.documents', 'project_id3', string='Documents')
    product_ids = fields.One2many('pmis.product.price', 'productprice_id', string='product price')
    implied_services_ids = fields.One2many('implied.services', 'implied_services_id', string='Implied services')

