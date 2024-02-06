from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import date, datetime


class PMISOfferAcceptance(models.Model):
    _name = "pmis.offeracceptance"
    _inherit = ['mail.thread']
    _description = "bidding affer Acceptance letter  Records"

    # this is to use bidding offer acceptance  information

    offer_acceptance_no = fields.Char(string='Acceptance No', required=True, tracking=True)
    offer_acceptance_date = fields.Date(string='Acceptance Date', tracking=True , default=fields.Date.today)
    contact_price = fields.Float(string='Contract Price', tracking=True)
    contact_time = fields.Float(string='Contract Time (in hours)', tracking=True)
    contact_place = fields.Char(string='Contract Place', tracking=True,  default='MCIT 13 Floor Procurement Office')
    ref = fields.Char(string='Reference', default=lambda self: _('New'))
    notes = fields.Text(string='Notes')

    winner_bidding_id = fields.Many2one('bidding.winner', string="Winner Bidding")
