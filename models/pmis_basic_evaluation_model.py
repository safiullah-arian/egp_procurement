from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import datetime, date


class BasicEvaluation(models.Model):
    _name = 'basic.evaluation'
    _description = 'Basic Evaluation'
    _rec_name = "received_offers_id"

    basic_evaluation_id = fields.Many2one('pmis.offerghoshai', string='Basic Evaluation')
    received_offers_id = fields.Many2one(
        'pmis.offer_submission',
        string="Received Offers",
        required=True,
        domain="[('id', 'in', available_offer_ids),('state', '=', 'received')]"
    )


    available_offer_ids = fields.Many2many(
        comodel_name='pmis.offer_submission',
        compute='_compute_available_journal_ids'
    )

    @api.depends('basic_evaluation_id')
    def _compute_available_journal_ids(self):
        for rec in self:
            rec.available_offer_ids = rec.basic_evaluation_id.offers_submission_ids
#
# <<<<<<< HEAD
# =======
#
# >>>>>>> d32340c96f165280a0130fc82d1aa166a559f848
    vendor_id = fields.Many2one(related="received_offers_id.vendor_id", string="Vendor")

    criteria = fields.Selection([
        ('bank_asset', 'Assets in Bank'),
        ('experience_years', 'Years of Experience'),
        ('number_of_transactions', 'Number of Transactions'),
    ], string='Criteria for Selection', )

    note = fields.Text(string='Note')



    Agent_ids = fields.One2many('pmis.vendor.agent', 'Agent_id', string='Vendor Agent')
    basic_evaluation_checkbox_ids = fields.One2many(
        'basic.evaluation.checkbox',
        'evaluation_checkbox_id',
        string="Basic Evaluation CheckBox"
    )

    guarantee_ids = fields.One2many('guaranteefor.bank', 'basic_evaluation_guarantee_id', string="Offer Guarantee")
    is_information_form_signed = fields.Boolean(string='Is Vendor Information Form Signed',default=True)

   
    vendor_transaction_ids = fields.One2many(
        'pmis.vendor.transactions',
        'basic_evaluation_transaction_id',
        string="Vendor Transaction"
    )

    vendor_experience_ids = fields.One2many(
        'pmis.vendor.experience',
        'basic_evaluation_experience_id',
        string="Vendor Experience"
    )

    vendor_assets_ids = fields.One2many(
        'pmis.vendor.assets',
        'basic_evaluation_assets_id',
        string="Vendor Assets"
    )

    @api.onchange('received_offers_id')
    def onchange_received_offers_id(self):
        self.offer_state = self.received_offers_id.id

    offer_state = fields.Integer(string='Offer state')

    @api.model
    def create(self, vals):
        self.env['pmis.offer_submission'].browse(vals['offer_state']).write({'state': 'offer_ghoshai'})
        print("Creation triggered", vals['offer_state'])
        return super(BasicEvaluation, self).create(vals)

    def unlink(self):
        # print("Delete triggered", self.project_id.id)
        self.env['pmis.offer_submission'].browse(self.offer_state).write({'state': 'received'})
        print(self.offer_state)
        return super(BasicEvaluation, self).unlink()
