from odoo import fields, models


class M7(models.Model):
    _name = 'pmis.m_seven'
    _description = 'info of M7'

    No = fields.Integer(string='M 7 Number')
    date = fields.Date(string='Date')
    office = fields.Char(string='Office')
    address = fields.Text(string='delivery Address')
    company = fields.Char(string='Vendor', related="delivery_id.vendor_id.name")
    order_no = fields.Char(string='Order Number')
    total_price = fields.Float(string='Total Price', related="delivery_id.invoice_ids.invoice_amount")
    trustee = fields.Char(string='Trustee')

    delivery_id = fields.Many2one('pmis.delivery.description', string='Delivery')

