from odoo import api, fields, models, _, tools
from datetime import datetime, date
from odoo.exceptions import ValidationError





class PmisContractManagement(models.Model):
    _name = 'pmis.contract.management'
    _description = 'Contract information for Contract Management'
    _rec_name = "winner_id"

    winner_id = fields.Many2one('bidding.winner', string='Project',
                                domain=[(
                                    'evaluated_project_id.evaluation_Project_id.offer_details_id.offer_ghoshai_project_id.offer_submission_project_id.announced_project_id.planned_project_id.project_id.state',
                                    '=',
                                    'offer_winning')], required=True)

    winner_project_name = fields.Many2one(string="Project Name", related="winner_id")
    contract_number = fields.Char(string="Contract Number",
                                  related="winner_id.project_id")


    vendor_id = fields.Many2one('pmis.vendors', string="Vendor",
                                related="winner_id.winning_offer_id.vendor_id")

    currency_unit = fields.Selection([
        ('AF', 'Afghan Afghani (AF)'),
        ('USD', 'US Dollar (USD)'),
        ('EUR', 'Euro (EUR)')
    ], string='Currency Unit'
        , related="winner_id.evaluated_project_id.evaluation_Project_id.offer_evaluation_ids.offer_currency")


    contract_price = fields.Float(string='Contract Price', tracking=True,
                                  related="winner_id.offer_acceptance_ids.contact_price")

    procurement_type = fields.Many2one(string="Procurement Type",
                                   related="winner_id.evaluated_project_id.evaluation_Project_id.offer_details_id.offer_ghoshai_project_id.offer_submission_project_id.announced_project_id.planned_project_id.project_id.category_id")

    budget_code = fields.Selection([('0', '220'), ('1', '222'), ('2', '225')], string='Budget Code',
                                   related="winner_id.evaluated_project_id.evaluation_Project_id.offer_details_id.offer_ghoshai_project_id.offer_submission_project_id.announced_project_id.planned_project_id.project_id.budget_code")

    contract_type = fields.Selection([
        ('sum_lum', 'Contract Sum Lum'),
        ('unit_price', 'Contract Unit Price'),
        ('framework', 'Framework'),
        ('percentage', 'Contract Base Percentage'),
        ('supply_chain', ' Erection and  Supply, Design for Contract'),
        ('industrial', 'Plant Industrial For Contract Turnke'),
        ('build_design', 'Contracts Build & Design'),
        ('pos_payment', 'Post Payment'),
        ('other', 'Other')
    ],
        string='Contract Type',
        related="winner_id.evaluated_project_id.evaluation_Project_id.offer_details_id.offer_ghoshai_project_id.offer_submission_project_id.announced_project_id.planned_project_id.contract_type")


    procurement_method = fields.Selection([('normal', 'Normal'), ('developing', 'Developing'), ],
                                          string='Procurement Method',
                                          related="winner_id.evaluated_project_id.evaluation_Project_id.offer_details_id.offer_ghoshai_project_id.offer_submission_project_id.announced_project_id.planned_project_id.budget_type")

    contract_date = fields.Date(string="Contract Date", related="winner_id.contract_signed_date")
    start_date = fields.Date(string="Start Date", related="winner_id.contract_agreement_ids.contract_start_date",limit=1,store=True)
    end_date = fields.Date(string="End Date", related="winner_id.contract_agreement_ids.contract_expiry_date",limit=1, store=True)
    remaining_duration = fields.Char(string='Remaining Duration', compute='_compute_remaining_duration')

    # @api.depends('end_date')
    @api.depends('end_date')
    def _compute_remaining_duration(self):
        for record in self:
            if record.end_date:
                current_date = fields.Date.today()
                end_date = fields.Date.from_string(record.end_date)
                remaining_days = (end_date - current_date).days
                record.remaining_duration = remaining_days


            else:

                record.remaining_duration = 0

    payment_Percentage = fields.Float(string="payment Percentage")
    vendor_name = fields.Many2one('pmis.vendors', string="Vendor Name")
    contract_states = fields.Selection([
        ('draft', 'Draft'),
        ('pending_approval', 'Pending Approval'),
        ('approved', 'Approved'),
        ('terminated', 'Terminated'),
        ('completed', 'Completed'),
    ], defualt="draft", string="Contract States")
    note = fields.Text(string="Comment")
    is_tadil = fields.Boolean(string="Is Tadil")
    tadil = fields.Selection([
        ('price', 'Price Tadil'),
        ('time', 'Time Tadil'),
        ('quantity', 'Quantity Tadil'),
    ], string="Tadil")

    documents_ids = fields.One2many('pmis.documents', 'contract_management_doc_id', string="Documents")

    # date method to check the strat date and end date
    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        for record in self:
            if record.start_date and record.end_date \
                    and record.start_date > record.end_date:
                raise ValidationError("Start date cannot be later than the end date!")

    @api.onchange('winner_id')
    def onchange_winner_id(self):
        self.project_name = self.winner_id.evaluated_project_id.evaluation_Project_id.offer_details_id.offer_ghoshai_project_id.offer_submission_project_id.announced_project_id.planned_project_id.project_id.id
        print("test", self.project_name)

    project_name = fields.Integer(string='Project Id')

    @api.model
    def create(self, vals):
        self.env['pmis.project'].browse(vals['project_name']).write({'state': 'contract'})
        print("Creation triggered", vals['project_name'])
        return super(PmisContractManagement, self).create(vals)

    def unlink(self):
        # print("Delete triggered", self.project_id.id)
        self.env['pmis.project'].browse(self.project_name).write({'state': 'offer_winning'})
        print("Offer deletion", self.project_name)
        return super(PmisContractManagement, self).unlink()
