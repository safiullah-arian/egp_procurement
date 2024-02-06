from odoo import models, fields, api


class PmisCandidateProposal(models.Model):
    _name = 'pmis.candidate.proposal'
    _description = 'Candidate Proposal'
    _rec_name = "shortlist_id"

    shortlist_id = fields.Many2one('pmis.first.shortlist', string='Shortlist', requred=True,
                                   domain="[('shortlist_project_id.job_title_id.planned_project_id.project_id.state', '=', 'shortlist')]")

    category_id = fields.Many2one(related="shortlist_id.procurement_type", string='Category')
    note = fields.Text(string='Note')
    candidate_application_ids = fields.One2many('pmis.candidate.application', 'candidate_shortlist_id',
                                                string='Candidate')

    @api.onchange('shortlist_id')
    def onchange_shortlist_id(self):
        self.project_name = self.shortlist_id.shortlist_project_id.job_title_id.planned_project_id.project_id.id

    project_name = fields.Integer(string='Project Id')

    @api.model
    def create(self, vals):
        self.env['pmis.project'].browse(vals['project_name']).write({'state': 'consult_offers_received'})
        print("Creation triggered", vals['project_name'])
        return super(PmisCandidateProposal, self).create(vals)

    def unlink(self):
        # print("Delete triggered", self.project_id.id)
        self.env['pmis.project'].browse(self.project_name).write({'state': 'shortlist'})
        print(self.project_name)
        return super(PmisCandidateProposal, self).unlink()


class PmisCandidateApplication(models.Model):
    _name = 'pmis.candidate.application'
    _description = 'Candidate Application'
    _rec_name = "candidate_shortlist_id"

    candidate_shortlist_id = fields.Many2one('pmis.candidate.proposal', string='Shortlist project')

    candidate_id = fields.Many2one('pmis.first.shortlist.application', string='Candidate', required=True,
                                   domain="[('id', 'in', available_offer_ids),('candidate_id.state', '=', 'submitted')]")
    is_applcated = fields.Boolean(string='Is Applied')
    proposal = fields.Binary(string='Proposal')
    proposal_text = fields.Text(string='Proposal')

    @api.onchange('candidate_id')
    def onchange_candidate_id(self):
        self.candidate_name = self.candidate_id.candidate_id.id

    candidate_name = fields.Integer(string='Candidate Id')

    @api.model
    def create(self, vals):
        self.env['pmis.job.application'].browse(vals['candidate_name']).write({'state': 'shortlisted'})
        print("Creation triggered", vals['candidate_name'])
        return super(PmisCandidateApplication, self).create(vals)

    def unlink(self):
        # print("Delete triggered", self.project_id.id)
        self.env['pmis.job.application'].browse(self.candidate_name).write({'state': 'submitted'})
        print(self.candidate_name)
        return super(PmisCandidateApplication, self).unlink()

    # @api.onchange('candidate_shortlist_id')
    # def onchange_candidate_shortlist_id(self):
    #     if self.candidate_shortlist_id:
    #         print("Shortlist Candidate ID:",
    #               self.candidate_shortlist_id.shortlist_id.id)
    #         domain = [
    #             ('first_shortlist_id', '=',
    #              self.candidate_shortlist_id.shortlist_id.id),('candidate_id.state', '=', 'submitted')
    #         ]
    #         return {'domain': {'candidate_id': domain}}

    available_offer_ids = fields.Many2many(
        comodel_name='pmis.first.shortlist.application',
        compute='_compute_available_ids'
    )

    @api.depends('candidate_shortlist_id')
    def _compute_available_ids(self):
        for rec in self:
            print(rec)
            rec.available_offer_ids = rec.candidate_shortlist_id.shortlist_id.shortlist_application_offer_ids
