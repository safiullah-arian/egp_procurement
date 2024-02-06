from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import datetime, date


class ProjectAnnouncement(models.Model):
    _name = "project.announcement"
    _description = "Project Announcement"
    _rec_name = "planned_project_id"

    planned_project_id = fields.Many2one('pmis.project.plan', string='Project',
                                         domain=[('project_id.state', '=', 'plan')],
                                         )


    @api.onchange('planned_project_id')
    def onchange_project_id(self):
        self.pro_announcement_date = self.env['pmis.project.plan'].search(
            [('project_id', '=', self.planned_project_id.id)]).project_announcement_date
        self.project_name = self.planned_project_id.project_id.id
        # print(self.project_name)

    project_name = fields.Integer(string='Project Id')
    pro_announcement_date = fields.Date(string='Announcement Date', default=fields.Date.today)

    pro_announcement_end_date = fields.Date(string='Announcement End Date')
    submission_address = fields.Text(
        string='Submission Address',
        default='MCIT 13 Floor Procurement Office',
    )

    announcement_source = fields.Char(string='Announcement Source',
                                      default='MCIT Website and Ministry of Information and Culture', )
    need_announcements = fields.Selection([
        ('need announcement', 'Announcement Needed'),
        ('dont need announcement', 'Announcement Not Needed'), ],
        string='Is announcement needed?', defualt='need announcement',
        tracking=True)
    note = fields.Text(string="Note")


    # date method to check the strat date and end date
    @api.constrains('pro_announcement_date', 'pro_announcement_end_date')
    def _check_dates(self):
        for record in self:
            if record.pro_announcement_date and record.pro_announcement_end_date \
                    and record.pro_announcement_date > record.pro_announcement_end_date:
                raise ValidationError("Start date cannot be later than the end date!")

    @api.model
    def create(self, vals):
        self.env['pmis.project'].browse(vals['project_name']).write({'state': 'announce'})
        print("Delete triggered", vals['project_name'])
        return super(ProjectAnnouncement, self).create(vals)

    def unlink(self):
        # print("Delete triggered", self.project_id.id)
        self.env['pmis.project'].browse(self.planned_project_id.project_id.id).write({'state': 'plan'})
        print(self.planned_project_id)
        return super(ProjectAnnouncement, self).unlink()


class ProjectConsultativeAnnouncement(models.Model):
    _name = "project.consultative.announcement"
    _description = "Project Consultative Announcement"
    _rec_name = "planned_project_id"

    planned_project_id = fields.Many2one('pmis.project.plan', string='Project',
                                         domain=[('project_id.state', '=', 'plan'),('project_id.category_id','=',2)],
                                         )


    @api.onchange('planned_project_id')
    def onchange_project_id(self):
        self.pro_announcement_date = self.env['pmis.project.plan'].search(
            [('project_id', '=', self.planned_project_id.id)]).project_announcement_date
        self.project_name = self.planned_project_id.project_id.id
        # print(self.project_name)

    project_name = fields.Integer(string='Project Id')
    pro_announcement_date = fields.Date(string='Announcement Date', default=fields.Date.today)

    pro_announcement_end_date = fields.Date(string='Announcement End Date')
    submission_address = fields.Text(
        string='Submission Address',
        default='MCIT 13 Floor Procurement Office',
    )

    announcement_source = fields.Char(string='Announcement Source',
                                      default='MCIT Website and Ministry of Information and Culture', )
    need_announcements = fields.Selection([
        ('need announcement', 'Announcement Needed'),
        ('dont need announcement', 'Announcement Not Needed'), ],
        string='Is announcement needed?', defualt='need announcement',
        tracking=True)
    note = fields.Text(string="Note")


    # date method to check the strat date and end date
    @api.constrains('pro_announcement_date', 'pro_announcement_end_date')
    def _check_dates(self):
        for record in self:
            if record.pro_announcement_date and record.pro_announcement_end_date \
                    and record.pro_announcement_date > record.pro_announcement_end_date:
                raise ValidationError("Start date cannot be later than the end date!")

    @api.model
    def create(self, vals):
        self.env['pmis.project'].browse(vals['project_name']).write({'state': 'announce'})
        print("Delete triggered", vals['project_name'])
        return super(ProjectConsultativeAnnouncement, self).create(vals)

    def unlink(self):
        # print("Delete triggered", self.project_id.id)
        self.env['pmis.project'].browse(self.planned_project_id.project_id.id).write({'state': 'plan'})
        print(self.planned_project_id)
        return super(ProjectConsultativeAnnouncement, self).unlink()
