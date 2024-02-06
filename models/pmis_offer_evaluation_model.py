from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import datetime, date


class PMISOffer(models.Model):
    _name = 'pmis.offer'
    _inherit = ['mail.thread']
    _description = "PMIS  Offer evaluation  Records"
    _rec_name = "details_offer_id"

    details_offer_id = fields.Many2one('pmis.offer_submission', required=True, string="Offer",
                                       domain="[('id', 'in', available_offer_ids),('state', '=', 'offer_details')]"
                                       )

    offers_evaluation_id = fields.Many2one('pmis.offers.evaluation', string='Offer Evaluation', readonly=True)


    available_offer_ids = fields.Many2many(
        comodel_name='pmis.offer_submission',
        compute='_compute_available_offers_ids'
    )

    @api.depends('offers_evaluation_id')
    def _compute_available_offers_ids(self):
        for rec in self:
            rec.available_offer_ids = rec.offers_evaluation_id.offer_details_id.offer_ghoshai_project_id.offers_submission_ids

    # @api.onchange('offers_evaluation_id')
    # def onchange_offers_evaluation_id(self):
    #     if self.offers_evaluation_id:
    #         domain = [('submission_project_id', '=',
    #                    self.offers_evaluation_id.offer_details_id.offer_ghoshai_project_id.offer_submission_project_id.id)]
    #         domain.append(('state', '=', 'offer_details'))
    #         return {'domain': {'details_offer_id': domain}}
    #     else:
    #         return {'domain': {'details_offer_id': []}}

    # company = fields.Char(string='Company')
    company = fields.Many2one('pmis.vendors', string='Vendor', related="details_offer_id.vendor_id")

    offer_lang = fields.Selection([
        ('pashto', 'Pashto'),
        ('dari', 'Dari'),
        ('english', 'English')],
        string='Offer Language', default="pashto",
        tracking=True)
    offer_currency = fields.Selection([
        ('AF', 'Afghan Afghani (AF)'),
        ('USD', 'US Dollar (USD)'),
        ('EUR', 'Euro (EUR)')],
        string='Offer Currency', default="AF",
        tracking=True)
    offer_total_price = fields.Float(string='Total Offer Price')
    offer_discount = fields.Float(string='Offer Discount')

    ref = fields.Char(string='Reference', default=lambda self: _('New'))

    # Establishing relationships
    vendor_ids = fields.One2many('exchange.currency.rate', 'offer_id', string='Vendors')
    internal_preference_ids = fields.One2many('internal.preference', 'offer_id', string='Internal Preferences')
    financial_evaluation_ids = fields.One2many('standard.form.financial.evaluation', 'offer_id',
                                               string='Financial Evaluations')
    technical_evaluation_ids = fields.One2many('technical.evaluation.standard.form', 'offer_id',
                                               string='Technical Evaluations')

    @api.onchange('details_offer_id')
    def onchange_details_offer_id(self):
        self.offer_state = self.details_offer_id.id

    offer_state = fields.Integer(string='Offer state')

    @api.model
    def create(self, vals):
        self.env['pmis.offer_submission'].browse(vals['offer_state']).write({'state': 'offer_evaluation'})
        print("Creation triggered", vals['offer_state'])
        return super(PMISOffer, self).create(vals)

    def unlink(self):
        # print("Delete triggered", self.project_id.id)
        self.env['pmis.offer_submission'].browse(self.offer_state).write({'state': 'offer_details'})
        print(self.offer_state)
        return super(PMISOffer, self).unlink()


# offers_evaluation_id = fields.Many2one('pmis.offers.evaluation', string='Offer Evaluation')


class PmisExchangeCurrencyRate(models.Model):
    _name = "exchange.currency.rate"
    _inherit = ['mail.thread']
    _description = "Exchange Currency Rate"

    offer_amount = fields.Float(string="Offer Amount", required=True)
    shartnama_amount = fields.Float(string="Shartnama Amount", required=True)
    exchange_rate = fields.Float(string="Exchange Rate", required=True)
    note = fields.Text(string="Note")

    # Relationship
    offer_id = fields.Many2one('pmis.offer', string='Offer')


class InternalPreference(models.Model):
    _name = "internal.preference"
    _inherit = ['mail.thread']
    _description = "Internal Preference Calculation"

    number = fields.Char(string="Number")
    agent_name = fields.Char(string="Company Agent Name")
    assessed_price = fields.Float(string="Assessed Price of Offer")
    product_name = fields.Char(string="Product Name")
    product_price = fields.Float(string="Product Price")
    preference_percentage = fields.Float(string="Preference Percentage")
    preference_value = fields.Float(string="Preference Value")
    price_after_preferences = fields.Float(string="Price After Preferences")
    note = fields.Text(string="Note")

    offer_id = fields.Many2one('pmis.offer', string='Offer')


class StandardFormFinancialEvaluation(models.Model):
    _name = "standard.form.financial.evaluation"
    _inherit = ['mail.thread']
    _description = "Standard Form of Financial Evaluation Offer"

    opening_day_amount = fields.Float(string="Amount Read on Opening Day (in Contract Currency)")
    calculation_errors = fields.Float(string="Calculation Errors")
    professional_sum = fields.Float(string="Professional Sum")
    revised_offer_price = fields.Float(string="Revised Offer Price")
    discount_percentage = fields.Float(string="Discount Percentage")
    discount_amount = fields.Float(string="Discount Amount")
    assessed_price = fields.Float(string="Assessed Price")
    internal_preference_amount = fields.Float(string="Internal Preference Amount")
    offer_grading = fields.Char(string="Offer Grading")
    note = fields.Text(string="Note")

    # Relationship
    offer_id = fields.Many2one('pmis.offer', string='Offer')


class TechnicalEvaluationStandardForm(models.Model):
    _name = "technical.evaluation.standard.form"
    _inherit = ['mail.thread']
    _description = "Technical Evaluation Standard Form"

    criteria = fields.Selection([
        ('similar_experience', 'Similar Experience'),
        ('annual_transaction_volume', 'Annual Transaction Volume'),
        ('financial_capability', 'Financial Capability')],
        string="Criteria", required=True)

    amount = fields.Float(string="Amount")
    offer_amount = fields.Float(string="Offer Amount")

    completed_criteria = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No')],
        string="Completed Criteria", required=True)

    nature_of_documents = fields.Char(string="Nature of Documents Provided by the Candidate")
    explanation_of_evaluation_board = fields.Char(string="Explanation of Evaluation Board")
    note = fields.Text(string="Note")

    # Relationship
    offer_id = fields.Many2one('pmis.offer', string='Offer')
