from odoo import models, fields


class PmisTestAnnouncement(models.Model):
    _name = 'pmis.announcement.test'
    _description = 'Test Model'

    # job_title_id = fields.Many2one('project.announcement', string='Job Title')
    # category_job_id = fields.Many2one('your.category.model', string='Category')
    note = fields.Text(string='Note')
    job_title_id = fields.Integer(string='Job Title')

    # job_title_id = fields.Char(string='Job Title')
    category_job_id = fields.Char(string='Category')
