from odoo import models, fields, api


class PmisJobAnnouncement(models.Model):
    _name = 'pmis.job.announcement'
    _description = 'Job Announcement'
    _rec_name = 'job_title_id'

    job_title_id = fields.Many2one('project.consultative.announcement', string='Job Title',
                                   domain="[('planned_project_id.project_id.category_id', '=', 2),('planned_project_id.project_id.state', '=', 'announce')]")

    category_job_id = fields.Many2one(related='job_title_id.planned_project_id.project_id.category_id',
                                      string='Catagory')

    note = fields.Text(string='Description')

    job_application_ids = fields.One2many('pmis.job.application', 'job_announcement_id', string='Job Application')

    @api.onchange('job_title_id')
    def onchange_job_title_id(self):
        self.project_name = self.job_title_id.planned_project_id.project_id.id

    project_name = fields.Integer(string='Project Id')

    @api.model
    def create(self, vals):
        self.env['pmis.project'].browse(vals['project_name']).write({'state': 'received_offers'})
        print("Creation triggered", vals['project_name'])
        return super(PmisJobAnnouncement, self).create(vals)

    def unlink(self):
        # print("Delete triggered", self.project_id.id)
        self.env['pmis.project'].browse(self.project_name).write({'state': 'announce'})
        print(self.project_name)
        return super(PmisJobAnnouncement, self).unlink()


class PmisJobApplication(models.Model):
    _name = 'pmis.job.application'
    _description = 'Job Application'
    _rec_name = 'candidate_name'

    candidate_name = fields.Char(string='Candidate Name')
    email = fields.Char(string='Email')
    phone = fields.Char(string='Phone')
    experience = fields.Char(string='Related Experience')
    cv_attachment = fields.Binary(string='CV Attachment')
    proposal_attachment = fields.Binary(string='Proposal Attachment')
    proposal_text = fields.Text(string='Proposal')
    job_announcement_id = fields.Many2one('pmis.job.announcement', string='Job Announcement')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('shortlisted', 'Shortlisted'),
        ('offerghoshai', 'Offer Ghoshai'),
        ('evaluated', 'Evaluated'),
        ('interviewed', 'Interviewed'),
        ('winner', 'Winner'),
        ('rejected', 'Rejected'),
    ], string='State', default='draft')
#
