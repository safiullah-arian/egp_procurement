from odoo import api, fields, models, _, tools
from datetime import datetime, date
from odoo.exceptions import ValidationError


class GuaranteeForBank(models.Model):
    _name = 'guaranteefor.bank'
    _description = 'Guarantee for Bank'

    guarantee_type = fields.Selection([
        ('guarantee_bank', 'Offer Guarantee'),
        ('guarantee_good_execution', 'Guarantee of Good Execution'),
        ('prepaymen_guarantee', 'Prepayment Guarantee')],
        string='Type of Guarantee',
        required=True
    )
    guarantee_amount_type = fields.Selection(
        [('cash', 'Cash'),
         ('bank', 'Bank')],
        default='bank', string='Guarantee Amount Type')

    date_entry = fields.Date(string='Date Entry')
    start_date = fields.Date(string='Start Date')
    expiry_date = fields.Date(string='Expiry Date')
    guarantee_no = fields.Char(string='Guarantee No')
    project_name = fields.Many2one('pmis.offerghoshai', string='Project Name')
    project_number = fields.Char(string='Project Number', related='project_name.project_number')
    amount = fields.Float(string='Amount', digits=(12, 2))
    bank_id = fields.Many2one('pmis.bank', string='Bank')
    bank_agent =  fields.Many2one('pmis.vendor.agent',string='Bank Agent Name')
    attachment_id = fields.Binary(string='Attachment')

    basic_evaluation_guarantee_id = fields.Many2one('basic.evaluation', string="basic Evaluation Guarantee")
    guarantee_submission_id = fields.Many2one('pmis.offersubmission', string='Project Guarantee')
    guarantee_winner_id = fields.Many2one('bidding.winner', string='Winner Guarantee')
    consult_basic_evaluation_guarantee_id = fields.Many2one('pmis.consultative.basic.evaluation',
                                                            string="Consultative Basic Evaluation Guarantee")


# class PmisBankGuarantee(models.Model):
#     _name = "pmis.bank.guarantee"
#     _description = "Bank guarantee for the project"
#
#     bank_name = fields.Char(string='Name Bank')
#     bank_representative = fields.Char(string='Bank Representative')
#     representative_job = fields.Char(string='Representative Job')
#     amount = fields.Float(string='Amount', digits=(12, 2))
#     guarantee_bank_id = fields.Many2one('guaranteefor.bank', 'Guarantee for Bank')
