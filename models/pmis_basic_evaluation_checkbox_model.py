from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import datetime, date


class BasicEvaluationCheckbox(models.Model):
    _name = 'basic.evaluation.checkbox'
    _description = 'Basic Evaluation Checkbox'


    is_packet_stamped = fields.Boolean(string='Packet Stamped ?', default=False)
    is_license_valid = fields.Boolean(string='Valid License ?', default=False)
    is_offer_filled_completely = fields.Boolean(string='Filled Completely ?', default=False)
    is_agent_letter_signed = fields.Boolean(string='Agent Letter Signed?', default=False)
    tadel_changes = fields.Boolean(string='Tadel & Changes')
    discount = fields.Boolean(string='Discount Or Tadil')
    is_offer_stamped = fields.Boolean(string='Offer Stamped ?', default=False)
    offer_currency_type = fields.Selection(
        [('afg','Afg'),
         ('usd','USD Dollar')],
        default='afg',string='Offer Currency')

    is_sample_submitted = fields.Boolean(string='Sample Submitted ?', default=False)
    total_price = fields.Float(string="Offer Amount")

    evaluation_checkbox_id = fields.Many2one('basic.evaluation', string="Evaluation Checkbox")

    consult_evaluation_checkbox_id = fields.Many2one('pmis.consultative.basic.evaluation',
                                                     string="Consultative Evaluation Checkbox")

