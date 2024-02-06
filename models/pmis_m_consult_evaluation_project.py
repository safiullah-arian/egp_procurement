from odoo import models, fields, api


class PmisConsultEvaluationProject(models.Model):
    _name = 'pmis.consult.evaluation.project'
    _description = 'Evaluation Candidates '
    _rec_name = 'offerghoshai_project_id'

    offerghoshai_project_id = fields.Many2one('pmis.consultative.offerghoshai.project', string='Evaluation Project', required=True,
                                              domain="[('offer_shortlist_project_id.shortlist_id.shortlist_project_id.job_title_id.planned_project_id.project_id.state', '=', 'consult_offersghoshai')]"
                                              )

    evaluation_condidate_ids = fields.One2many('pmis.consult.evaluation', 'offerghoshai_candidate_id',
                                               'Evaluation Candidate')

    evaluation_consult_panel_ids = fields.One2many('pmis.vendor.agent', 'consult_panel_id',
                                                   string="Consult Evaluation Panel")

    @api.onchange('offerghoshai_project_id')
    def onchange_offerghoshai_project_id(self):
        self.project_name = self.offerghoshai_project_id.offer_shortlist_project_id.shortlist_id.shortlist_project_id.job_title_id.planned_project_id.project_id.id

    project_name = fields.Integer(string='Project Id')

    @api.model
    def create(self, vals):
        self.env['pmis.project'].browse(vals['project_name']).write({'state': 'consult_evaluation'})
        print("Creation triggered", vals['project_name'])
        return super(PmisConsultEvaluationProject, self).create(vals)

    def unlink(self):
        # print("Delete triggered", self.project_id.id)
        self.env['pmis.project'].browse(self.project_name).write({'state': 'consult_offersghoshai'})
        print(self.project_name)
        return super(PmisConsultEvaluationProject, self).unlink()
