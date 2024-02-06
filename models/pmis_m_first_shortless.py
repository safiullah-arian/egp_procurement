from odoo import models, fields, api


class PmisFirstShortlist(models.Model):
    _name = 'pmis.first.shortlist'
    _description = 'First Shortlist'
    _rec_name = 'shortlist_project_id'

    shortlist_project_id = fields.Many2one('pmis.job.announcement', string='Project',
                                           required=True,
                                           domain="[('job_title_id.planned_project_id.project_id.state', '=', 'received_offers')]")
    procurement_type = fields.Many2one(string='Procurement Type', related="shortlist_project_id.category_job_id",
                                       required=True)

    shortlist_application_offer_ids = fields.One2many('pmis.first.shortlist.application', 'first_shortlist_id',
                                                      string='Related Offers', )





    @api.onchange('shortlist_project_id')
    def onchange_shortlist_project_id(self):
        self.project_name = self.shortlist_project_id.job_title_id.planned_project_id.project_id.id

    project_name = fields.Integer(string='Project Id')

    @api.model
    def create(self, vals):
        self.env['pmis.project'].browse(vals['project_name']).write({'state': 'shortlist'})
        print("Creation triggered", vals['project_name'])
        return super(PmisFirstShortlist, self).create(vals)

    def unlink(self):
        # print("Delete triggered", self.project_id.id)
        self.env['pmis.project'].browse(self.project_name).write({'state': 'received_offers'})
        print(self.project_name)
        return super(PmisFirstShortlist, self).unlink()


class PmisFirstShortlistApplication(models.Model):
    _name = 'pmis.first.shortlist.application'
    _description = 'Pmis First shortlist Application'
    _rec_name = 'candidate_id'

    first_shortlist_id = fields.Many2one('pmis.first.shortlist', string='First Shortlist')
    candidate_id = fields.Many2one('pmis.job.application', string='Candidate', required=True,
                                   domain="[('id', 'in', available_offer_ids),('state', '=', 'draft')]")

    experience = fields.Char(string='Related Experience',
                             related="candidate_id.experience")

    proposal_text = fields.Text(string='Shortlist Note')
    #
    available_offer_ids = fields.Many2many(
        comodel_name='pmis.job.application',
        compute='_compute_available_ids'
    )

    @api.depends('first_shortlist_id')
    def _compute_available_ids(self):
        for rec in self:
            print(rec)
            rec.available_offer_ids = rec.first_shortlist_id.shortlist_project_id.job_application_ids

    @api.onchange('candidate_id')
    def onchange_candidate_id(self):
        self.candidate_name = self.candidate_id.id

    candidate_name = fields.Integer(string='Candidate Id')

    @api.model
    def create(self, vals):
        self.env['pmis.job.application'].browse(vals['candidate_name']).write({'state': 'submitted'})
        print("Creation triggered", vals['candidate_name'])
        return super(PmisFirstShortlistApplication, self).create(vals)

    def unlink(self):
        # print("Delete triggered", self.project_id.id)
        self.env['pmis.job.application'].browse(self.candidate_name).write({'state': 'draft'})
        print(self.candidate_name)
        return super(PmisFirstShortlistApplication, self).unlink()



    # @api.onchange('first_shortlist_id')
    # def onchange_first_shortlist_id(self):
    #     if self.first_shortlist_id:
    #         print("Shortlist Candidate ID:", self.first_shortlist_id.shortlist_project_id.id)
    #         domain = [
    #             ('job_announcement_id', '=', self.first_shortlist_id.shortlist_project_id.id), ('state', '=', 'draft')
    #         ]
    #         return {'domain': {'candidate_id': domain}}


