from odoo import models, fields, api


class PmisBiddingWinningAnnouncement(models.Model):
    _name = 'pmis.bidding.winning.announcement'
    _description = 'Bidding Winning Announcement'
    _rec_name = "evaluation_Project_id"

    evaluation_Project_id = fields.Many2one('pmis.offers.evaluation', string='Project',
                                            domain=[(
                                                'offer_details_id.offer_ghoshai_project_id.offer_submission_project_id.announced_project_id.planned_project_id.project_id.state',
                                                '=',
                                                'offer_testing')],
                                            )
    evaluation_offer_id = fields.Many2one('pmis.offer_submission', string='Winner Offer',
                                          domain="[('id', 'in', available_offer_ids),('state', '=', 'offer_evaluation')]"
                                          )
    winner_announc_start_date = fields.Date(string='Announcement Start Date')
    winner_announc_end_date = fields.Date(string='Announcement End Date')
    attachment = fields.Binary(string='Attachment')

    evaluat_project_id = fields.Many2one(string='Project Name',
                                         related='evaluation_Project_id')

    is_complaints = fields.Boolean(string='Has Complaint', default=False)

    complaint_winner_ids = fields.One2many('pmis.complaint.vendors', 'complaint_winner_id',
                                           string='Complaint_id')

    complaint_processing_agents_ids = fields.One2many('pmis.vendor.agent', 'complaint_winner_id',
                                                      string='Complaint Processing Bord')

    available_offer_ids = fields.Many2many(
        comodel_name='pmis.offer_submission',
        compute='_compute_available_offers_ids'
    )

    @api.depends('evaluation_Project_id')
    def _compute_available_offers_ids(self):
        for rec in self:
            rec.available_offer_ids = rec.evaluation_Project_id.offer_details_id.offer_ghoshai_project_id.offers_submission_ids
    # @api.onchange('evaluat_project_id')
    # def onchange_evaluat_project_id(self):
    #     if self.evaluat_project_id:
    #         domain = [('submission_project_id', '=',
    #                    self.evaluation_Project_id.offer_details_id.offer_ghoshai_project_id.offer_submission_project_id.id)]
    #         domain.append(('state', '=', 'offer_evaluation'))
    #         return {'domain': {'evaluation_offer_id': domain}}
    #     else:
    #         return {'domain': {'evaluation_offer_id': []}}

    @api.onchange('evaluation_Project_id')
    def onchange_evaluation_Project_id(self):
        self.project_name = self.evaluation_Project_id.offer_details_id.offer_ghoshai_project_id.offer_submission_project_id.announced_project_id.planned_project_id.project_id.id
        print("test", self.project_name)
        print("this is onchange project")

    project_name = fields.Integer(string='Project Id')

    @api.onchange('evaluation_offer_id')
    def onchange_evaluation_offer_id(self):
        self.offer_state = self.evaluation_offer_id.id

    offer_state = fields.Integer(string='Offer state')

    @api.model
    def create(self, vals):
        self.env['pmis.project'].browse(vals['project_name']).write({'state': 'winner_announcement'})
        self.env['pmis.offer_submission'].browse(vals['offer_state']).write({'state': 'announced_winner'})
        print("Creation triggered", vals['project_name'])
        return super(PmisBiddingWinningAnnouncement, self).create(vals)

    def unlink(self):
        # print("Delete triggered", self.project_id.id)
        self.env['pmis.project'].browse(self.project_name).write({'state': 'offer_testing'})
        self.env['pmis.offer_submission'].browse(self.offer_state).write({'state': 'offer_evaluation'})
        print("Offer deletion", self.project_name)
        return super(PmisBiddingWinningAnnouncement, self).unlink()


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
    complaint_winner_id = fields.Many2one(
        comodel_name="pmis.bidding.winning.announcement", string="Compliant Board"
    )
