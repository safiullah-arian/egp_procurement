from odoo import models, fields, api


class PmisConsultInterview(models.Model):
    _name = 'pmis.consult.interview'
    _description = 'candidate_id'
    _rec_name = "candidate_id"

    consult_interview_id = fields.Many2one('pmis.consult.interview.project', string='Evaluation')
    candidate_id = fields.Many2one('pmis.first.shortlist.application', string='Candidate',
                                   domain="[('id', 'in', available_offer_ids),('candidate_id.state', '=', 'evaluated')]")

    # candidate_total_marks = fields.Integer(related='consult_interview_id.evaluation_id.evaluation_condidate_ids.total_marks',string='Total Marks')
    interview_date = fields.Date(string='Interview Date')
    interview_notes = fields.Text(string='Interview Notes')
    is_selected = fields.Boolean(string='Is Selected')
# related='consult_interview_id.evaluation_id.total_marks'

    candidate_name = fields.Integer(string='Candidate Id')

    @api.onchange('candidate_id')
    def onchange_candidate_id(self):
        self.candidate_name = self.candidate_id.candidate_id.id
        # print(self.candidate_name)

    @api.model
    def create(self, vals):
        self.env['pmis.job.application'].browse(vals['candidate_name']).write({'state': 'interviewed'})
        # print("Creation triggered", vals['candidate_name'])
        return super(PmisConsultInterview, self).create(vals)

    def unlink(self):
        # print("Delete triggered", self.project_id.id)
        self.env['pmis.job.application'].browse(self.candidate_name).write({'state': 'evaluated'})
        # print(self.candidate_name)
        return super(PmisConsultInterview, self).unlink()



    available_offer_ids = fields.Many2many(
        comodel_name='pmis.first.shortlist.application',
        compute='_compute_available_ids'
    )

    @api.depends('consult_interview_id')
    def _compute_available_ids(self):
        for rec in self:
            print(rec)
            rec.available_offer_ids = rec.consult_interview_id.evaluation_id.offerghoshai_project_id.offer_shortlist_project_id.shortlist_id.shortlist_application_offer_ids