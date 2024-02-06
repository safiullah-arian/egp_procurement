from odoo import models, fields, api


class PmisConsultEvaluation(models.Model):
    _name = 'pmis.consult.evaluation'
    _description = 'Pmis Consult Evaluation Project'
    _rec_name = 'consult_offerghoshai_id'

    offerghoshai_candidate_id = fields.Many2one('pmis.consult.evaluation.project', string='Evaluation Candidate')

    consult_offerghoshai_id = fields.Many2one('pmis.first.shortlist.application', string='Candidate Name',
                                              domain="[('id', 'in', available_offer_ids),('candidate_id.state', '=', 'offerghoshai')]"
                                              )

    total_marks = fields.Integer(string='Total Marks', compute='_compute_total_marks', store=True)

    financial_evaluation_ids = fields.One2many('pmis.consult.financial.evaluation', 'consult_evaluation_id',
                                               'Financial Evaluation')
    technical_evaluation_ids = fields.One2many('pmis.consult.technical.evaluation', 'consult_evaluation_id',
                                               'Technical Evaluation')

    candidate_name = fields.Integer(string='Candidate Id')

    @api.onchange('consult_offerghoshai_id')
    def onchange_consult_offerghoshai_id(self):
        self.candidate_name = self.consult_offerghoshai_id.candidate_id.id
        # print(self.candidate_name)

    @api.model
    def create(self, vals):
        self.env['pmis.job.application'].browse(vals['candidate_name']).write({'state': 'evaluated'})
        # print("Creation triggered", vals['candidate_name'])
        return super(PmisConsultEvaluation, self).create(vals)

    def unlink(self):
        # print("Delete triggered", self.project_id.id)
        self.env['pmis.job.application'].browse(self.candidate_name).write({'state': 'offerghoshai'})
        # print(self.candidate_name)
        return super(PmisConsultEvaluation, self).unlink()

    # @api.onchange('offerghoshai_candidate_id')
    # def onchange_offerghoshai_candidate_id(self):
    #     if self.offerghoshai_candidate_id:
    #         print("Shortlist Candidate ID:",
    #               self.offerghoshai_candidate_id.offerghoshai_project_id.offer_shortlist_project_id.shortlist_id.id)
    #         domain = [
    #             ('first_shortlist_id', '=',
    #              self.offerghoshai_candidate_id.offerghoshai_project_id.offer_shortlist_project_id.shortlist_id.id),
    #             ('candidate_id.state', '=', 'offerghoshai')
    #         ]
    #         return {'domain': {'consult_offerghoshai_id': domain}}

    available_offer_ids = fields.Many2many(
        comodel_name='pmis.first.shortlist.application',
        compute='_compute_available_ids'
    )

    @api.depends('offerghoshai_candidate_id')
    def _compute_available_ids(self):
        for rec in self:
            print(rec)
            rec.available_offer_ids = rec.offerghoshai_candidate_id.offerghoshai_project_id.offer_shortlist_project_id.shortlist_id.shortlist_application_offer_ids

    @api.depends('financial_evaluation_ids.financial_marks', 'technical_evaluation_ids.evaluation_marks')
    def _compute_total_marks(self):
        for evaluation in self:
            financial_total = sum(e.financial_marks for e in evaluation.financial_evaluation_ids)
            technical_total = sum(e.evaluation_marks for e in evaluation.technical_evaluation_ids)
            total = financial_total + technical_total
            evaluation.total_marks = total


class PmisConsultFinancialEvaluation(models.Model):
    _name = 'pmis.consult.financial.evaluation'
    _description = 'Pmis Consult Financial Evaluation Project'
    _rec_name = 'consult_evaluation_id'

    consult_evaluation_id = fields.Many2one('pmis.consult.evaluation', string='Candidate Name')
    financial_marks = fields.Integer(string='Total Financial Marks', default=0)
    financial_doc = fields.Binary(string='Financial Document')


class PmisConsultTechnicalEvaluation(models.Model):
    _name = 'pmis.consult.technical.evaluation'
    _description = 'Pmis Consult Technical Evaluation Project'
    _rec_name = 'consult_evaluation_id'

    consult_evaluation_id = fields.Many2one('pmis.consult.evaluation', string='Candidate Name')
    evaluation_marks = fields.Integer(string='Total Technical Marks', default=0)
    evaluation_doc = fields.Binary(string='Technical Document')
