from odoo import models, fields, api


class PmisConsultInterviewProject(models.Model):
    _name = 'pmis.consult.interview.project'
    _description = 'Interview Candidates '
    _rec_name = 'evaluation_id'

    evaluation_id = fields.Many2one('pmis.consult.evaluation.project', string='Evaluation', required=True,
                                    domain="[('offerghoshai_project_id.offer_shortlist_project_id.shortlist_id.shortlist_project_id.job_title_id.planned_project_id.project_id.state', '=', 'consult_evaluation')]"
                                    )

    interview_panel_ids = fields.One2many('pmis.vendor.agent', 'consult_interview_id', string='Interviewers')

    consult_interview_ids = fields.One2many('pmis.consult.interview', 'consult_interview_id', string='Interview Candidates')


    @api.onchange('evaluation_id')
    def onchange_evaluation_id(self):
        self.project_name = self.evaluation_id.offerghoshai_project_id.offer_shortlist_project_id.shortlist_id.shortlist_project_id.job_title_id.planned_project_id.project_id.id

    project_name = fields.Integer(string='Project Id')

    @api.model
    def create(self, vals):
        self.env['pmis.project'].browse(vals['project_name']).write({'state': 'consult_winners'})
        print("Creation triggered", vals['project_name'])
        return super(PmisConsultInterviewProject, self).create(vals)

    def unlink(self):
        # print("Delete triggered", self.project_id.id)
        self.env['pmis.project'].browse(self.project_name).write({'state': 'consult_evaluation'})
        print(self.project_name)
        return super(PmisConsultInterviewProject, self).unlink()