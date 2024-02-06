from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import datetime, date


class ImpliedServices(models.Model):
    _name = "implied.services"
    _inherit = ['mail.thread']
    _description = "Implied Services"


    product_description_id = fields.Many2one(
        comodel_name="pmis.products.description",
        string="Products ",
        readonly=False,
    )
    service_description = fields.Char(string="Service Description", required=True, default="Not Applicable")
    delivery_date = fields.Date(string="Delivery Date")
    implied_services_id = fields.Many2one('pmis.offersubmission', string="Note")
    source_country = fields.Many2one('pmis.country', string="Source Country" , default=1)

    name = fields.Char(
        string='Name',
    )

    qty = fields.Integer(string='Quantity')
    price = fields.Float(string='Price', required=True)
    sub_total = fields.Float(string='Sub Total', compute="_compute_sub_total")

    @api.onchange('qty', 'price')
    def _compute_sub_total(self):
        for rec in self:
            if rec.price:
                rec.sub_total = rec.price * rec.qty

            else:
                rec.sub_total = 0.0
