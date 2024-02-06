from odoo import api, fields, models
from datetime import datetime,date


class Invoice(models.Model):
    _name = 'pmis.invoice'
    _description = 'Invoice Information'
    _rec_name = "invoice_number"

    invoice_number = fields.Char(string='Invoice Number', required=True)
    invoice_date = fields.Date(string='Invoice Date', default=date.today())
    invoice_amount = fields.Float(string='Invoice Amount')
    payment_terms = fields.Char(string='Payment Terms')
    invoice_scan = fields.Binary(string='Invoice Scan')

    delivery_id = fields.Many2one('pmis.delivery.description', string='Delivery')
