from odoo import models, fields, api


class PmisWinnerCandidatesProjects(models.Model):
    _name = 'pmis.winners.candidates.project'
    _description = 'Winner Project'
    _rec_name = "interview_project_id"

    interview_project_id = fields.Many2one('pmis.consult.interview.project', string='Project', required=True,
                                           domain="[('evaluation_id.offerghoshai_project_id.offer_shortlist_project_id.shortlist_id.shortlist_project_id.job_title_id.planned_project_id.project_id.state', '=', 'consult_winners')]")

    winner_ids = fields.One2many('pmis.winner.candidates', 'candidate_project_id', string='Winner')

    @api.onchange('interview_project_id')
    def onchange_interview_project_id(self):
        self.project_name = self.interview_project_id.evaluation_id.offerghoshai_project_id.offer_shortlist_project_id.shortlist_id.shortlist_project_id.job_title_id.planned_project_id.project_id.id

    project_name = fields.Integer(string='Project Id')

    @api.model
    def create(self, vals):
        self.env['pmis.project'].browse(vals['project_name']).write({'state': 'consult_candidate_won'})
        print("Creation triggered", vals['project_name'])
        return super(PmisWinnerCandidatesProjects, self).create(vals)

    def unlink(self):
        # print("Delete triggered", self.project_id.id)
        self.env['pmis.project'].browse(self.project_name).write({'state': 'consult_winners'})
        print(self.project_name)
        return super(PmisWinnerCandidatesProjects, self).unlink()





class PmisWinnerCandidates(models.Model):
    _name = 'pmis.winner.candidates'
    _description = 'Winner Candidates'
    _rec_name = 'candidate_id'

    candidate_project_id = fields.Many2one('pmis.winners.candidates.project', string='Candidate Project')
    candidate_id = fields.Many2one('pmis.consult.interview', string='Candidate', required=True,
                                   domain="[('id', 'in', available_offer_ids),('is_selected', '=', True), ('candidate_id.candidate_id.state', '=', 'interviewed')]")
    # domain="[('is_selected', '=', True)]")
    start_date = fields.Date(string='Interview Round')
    contract_date = fields.Date(string='Winner')
    note = fields.Text(string='Note')

    candidate_name = fields.Integer(string='Candidate Id')

    @api.onchange('candidate_id')
    def onchange_candidate_id(self):
        self.candidate_name = self.candidate_id.candidate_id.candidate_id.id
        # print(self.candidate_name)

    @api.model
    def create(self, vals):
        self.env['pmis.job.application'].browse(vals['candidate_name']).write({'state': 'winner'})
        # print("Creation triggered", vals['candidate_name'])
        return super(PmisWinnerCandidates, self).create(vals)

    def unlink(self):
        # print("Delete triggered", self.project_id.id)
        self.env['pmis.job.application'].browse(self.candidate_name).write({'state': 'interviewed'})
        # print(self.candidate_name)
        return super(PmisWinnerCandidates, self).unlink()

    # @api.onchange('candidate_project_id')
    # def onchange_candidate_project_id(self):
    #     domain = []
    #     if self.candidate_project_id:
    #         domain = [('consult_interview_id', '=', self.candidate_project_id.interview_project_id.id),
    #                   ('is_selected', '=', True), ('candidate_id.candidate_id.state', '=', 'interviewed')]
    #     return {'domain': {'candidate_id': domain}}

    available_offer_ids = fields.Many2many(
        comodel_name='pmis.consult.interview',
        compute='_compute_available_ids'
    )

    @api.depends('candidate_project_id')
    def _compute_available_ids(self):
        for rec in self:
            print(rec)
            rec.available_offer_ids = rec.candidate_project_id.interview_project_id.consult_interview_ids
