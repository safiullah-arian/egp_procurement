from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import datetime, date


class BiddingWinner(models.Model):
    _name = 'bidding.winner'
    _description = 'Bidding Winner Information'
    _rec_name = 'evaluated_project_id'

    evaluated_project_id = fields.Many2one('pmis.bidding.winning.announcement', string='Evaluated Project',
                                           domain=[(
                                               'evaluation_Project_id.offer_details_id.offer_ghoshai_project_id.offer_submission_project_id.announced_project_id.planned_project_id.project_id.state',
                                               '=',
                                               'winner_announcement')], required=True,
                                           )
    project_name_id = fields.Many2one(string='Project Name',
                                      related='evaluated_project_id')
    winning_offer_id = fields.Many2one(
        'pmis.offer_submission',
        string='Winning Offer',
        domain="[('id', 'in', available_offer_ids),('state', '=', 'announced_winner')]"
    )

    available_offer_ids = fields.Many2many(
        comodel_name='pmis.offer_submission',
        compute='_compute_available_offers_ids'
    )

    @api.depends('evaluated_project_id')
    def _compute_available_offers_ids(self):
        for rec in self:
            rec.available_offer_ids = rec.evaluated_project_id.evaluation_Project_id.offer_details_id.offer_ghoshai_project_id.offers_submission_ids

    # @api.onchange('project_name_id')
    # def onchange_project_name_id(self):
    #     print('he')
    #     if self.project_name_id:
    #         domain = [('submission_project_id', '=',
    #                    self.evaluated_project_id.evaluation_Project_id.offer_details_id.offer_ghoshai_project_id.offer_submission_project_id.id)]
    #         domain.append(('state', '=', 'announced_winner'))
    #         domain.append(('state', '=', 'announced_winner'))
    #         return {'domain': {'winning_offer_id': domain}}
    #     else:
    #         return {'domain': {'winning_offer_id': []}}

    project_id = fields.Char(string='Project Number',
                             related='evaluated_project_id.evaluation_Project_id.offer_details_id.offer_ghoshai_project_id.offer_submission_project_id.announced_project_id.planned_project_id.project_id.project_number')

    is_contract_signed = fields.Boolean(string='Contract Signed', default=False)
    contract_signed_date = fields.Date(string='Contract Signed Date', default=fields.Date.context_today)


    offer_acceptance_ids = fields.One2many('pmis.offeracceptance', 'winner_bidding_id', string='Offer Acceptance')
    contract_agreement_ids = fields.One2many('pmis.contractagreement', 'winner_bidding_agreement_id',
                                             string='Contract Agreement')
    winner_guarantee_ids = fields.One2many('guaranteefor.bank', 'guarantee_winner_id', string='Offer Guarantee')

    is_complaints = fields.Boolean(string='Has Complaint', default=False)

    complaint_vendor_ids = fields.One2many('pmis.complaint.vendors', 'complaint_vendor_winner_id',
                                           string='Complaint_id')
    project_name = fields.Integer(string='Project Id')

    @api.onchange('evaluated_project_id')
    def onchange_evaluated_project_id(self):
        self.project_name = self.evaluated_project_id.evaluation_Project_id.offer_details_id.offer_ghoshai_project_id.offer_submission_project_id.announced_project_id.planned_project_id.project_id.id
        print("test", self.project_name)


    @api.onchange('winning_offer_id')
    def onchange_winning_offer_id(self):
        self.offer_state = self.winning_offer_id.id


    offer_state = fields.Integer(string='Offer state')

    @api.model
    def create(self, vals):
        self.env['pmis.project'].browse(vals['project_name']).write({'state': 'offer_winning'})
        self.env['pmis.offer_submission'].browse(vals['offer_state']).write({'state': 'offer_winner'})
        print("Creation triggered", vals['project_name'])
        return super(BiddingWinner, self).create(vals)

    def unlink(self):
        # print("Delete triggered", self.project_id.id)
        self.env['pmis.project'].browse(self.project_name).write({'state': 'winner_announcement'})
        self.env['pmis.offer_submission'].browse(self.offer_state).write({'state': 'announced_winner'})

        return super(BiddingWinner, self).unlink()


class Pmis_complaint_Vendors(models.Model):
    _name = 'pmis.complaint.vendors'
    _description = 'Procurement Complaint vendor'
    _rec_name = 'vendor'

    complaint_no = fields.Char(string='Complaint No', required=True)
    vendor = fields.Many2one('pmis.vendors', string='Vendor')
    date = fields.Date(string='Complaint Date')
    details = fields.Html(string='Details')
    attachments = fields.Binary(string='Attachments')

    complaint_vendor_winner_id = fields.Many2one('bidding.winner', string='Complaint Vendor Winner')

