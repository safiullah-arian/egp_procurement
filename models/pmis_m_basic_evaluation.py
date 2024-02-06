from odoo import api, fields, models, api, tools
from odoo.exceptions import ValidationError
from datetime import datetime, date


class PmisConsultativeBasicEvaluation(models.Model):
    _name = 'pmis.consultative.basic.evaluation'
    _description = 'Consultative Basic Evaluation'
    _rec_name = "basic_evaluation_id"

    basic_evaluation_id = fields.Many2one('pmis.consultative.offerghoshai', string='Basic Evaluation')
    shortlist_project_offer_id = fields.Many2one("pmis.first.shortlist.application", required=True, string="Offer",
                                                 domain="[('id', 'in', available_offer_ids),('candidate_id.state', '=', 'shortlisted'),('candidate_id.state', '=', 'offerghoshai')]")
    note = fields.Text(string='Note')

    Agent_consult_ids = fields.One2many('pmis.vendor.agent', 'Agent_consult_id', string='Vendor Agent')

    consult_basic_evaluation_checkbox_ids = fields.One2many(
        'basic.evaluation.checkbox',
        'consult_evaluation_checkbox_id',
        string="Basic Evaluation CheckBox"
    )
    consult_guarantee_ids = fields.One2many('guaranteefor.bank', 'consult_basic_evaluation_guarantee_id',
                                            string="Offer Guarantee")


    candidate_name = fields.Integer(string='Candidate Id')

    @api.onchange('shortlist_project_offer_id')
    def onchange_shortlist_project_offer_id(self):
        if self.shortlist_project_offer_id:
            self.candidate_name = self.shortlist_project_offer_id.candidate_id.id

    @api.model
    def create(self, vals):
        if 'candidate_name' in vals:
            self.env['pmis.job.application'].browse(vals['candidate_name']).write({'state': 'offerghoshai'})
            print("Creation triggered", vals['candidate_name'])
        return super(PmisConsultativeBasicEvaluation, self).create(vals)

    def unlink(self):
        if self.candidate_name:
            self.env['pmis.job.application'].browse(self.candidate_name).write({'state': 'shortlisted'})
            print(self.candidate_name)
        return super(PmisConsultativeBasicEvaluation, self).unlink()

    # @api.onchange('basic_evaluation_id')
    # def onchange_basic_evaluation_id(self):
    #     if self.basic_evaluation_id:
    #         print("Shortlist Candidate ID:",
    #               self.basic_evaluation_id.offerghoshai_shortlist_project_id.offer_shortlist_project_id.shortlist_id.id)
    #         domain = [
    #             ('first_shortlist_id', '=',
    #              self.basic_evaluation_id.offerghoshai_shortlist_project_id.offer_shortlist_project_id.shortlist_id.id),
    #             ('candidate_id.state', '=', 'shortlisted')
    #         ]
    #         return {'domain': {'shortlist_project_offer_id': domain}}

    available_offer_ids = fields.Many2many(
        comodel_name='pmis.first.shortlist.application',
        compute='_compute_available_ids'
    )

    @api.depends('basic_evaluation_id')
    def _compute_available_ids(self):
        for rec in self:
            print(rec)
            rec.available_offer_ids = rec.basic_evaluation_id.offerghoshai_shortlist_project_id.offer_shortlist_project_id.shortlist_id.shortlist_application_offer_ids
