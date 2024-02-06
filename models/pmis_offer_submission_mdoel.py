from odoo import api, fields, models, _
from odoo.exceptions import ValidationError



class PmisOffer_Submission_project(models.Model):
    _name = "pmis.offer_submission_project"
    _inherit = ['mail.thread']
    _description = "Offer submission project"
    _rec_name = "announced_project_id"

    # this is to use bidding information
    announced_project_id = fields.Many2one('project.announcement', string='Project', required=True,
                                           domain=[('planned_project_id.project_id.state', '=', 'announce'),
                                                   ('planned_project_id.project_id.category_id', '!=', 2)])

    project_number = fields.Char(string='Project Number',
                                 related='announced_project_id.planned_project_id.project_id.project_number')


    offers_submission_ids = fields.One2many('pmis.offer_submission', 'submission_project_id', string='Offer Submission')

    category_id = fields.Many2one(related='announced_project_id.planned_project_id.project_id.category_id',
                                  string='Catagory', store=True)

    @api.onchange('announced_project_id')
    def onchange_announced_project_id(self):
        self.project_name = self.announced_project_id.planned_project_id.project_id.id

    project_name = fields.Integer(string='Project Id')

    @api.model
    def create(self, vals):
        self.env['pmis.project'].browse(vals['project_name']).write({'state': 'received_offers'})
        print("Creation triggered", vals['project_name'])
        return super(PmisOffer_Submission_project, self).create(vals)

    def unlink(self):
        # print("Delete triggered", self.project_id.id)

        for rec in self.offers_submission_ids:
            self.env['pmis.offer_submission'].browse(rec.id).unlink()
        self.env['pmis.project'].browse(self.project_name).write({'state': 'announce'})

        return super(PmisOffer_Submission_project, self).unlink()


class PmisOffer_Submission(models.Model):
    _name = "pmis.offer_submission"
    _inherit = ['mail.thread']
    _description = "bidding Records"
    _rec_name = "vendor_id"

    # this is to use bidding information
    submission_project_id = fields.Many2one('pmis.offer_submission_project', string='Submission Project')

    offer_submission_no = fields.Char(string='Submission No', required=True)
    offer_submission_date = fields.Datetime(string='Submission Date', default=fields.Datetime.now)
    receiving_office = fields.Many2one('pmis.directorates', string='Receiving Office', required=True)

    offer_submission_address = fields.Char(string='Submission Address', default='MCIT 13 Floor Procurement Office', )
    note = fields.Text(string='Note')

    vendor_id = fields.Many2one('pmis.vendors', string='Vendor', required=True)
    project_id = fields.Many2one(string='Project',
                                 related='submission_project_id.announced_project_id.planned_project_id.project_id')

    state = fields.Selection([
        ('received', 'Received'),
        ('offer_ghoshai', 'Offer Ghoshai'),
        ('offer_details', 'Offer Details'),
        ('offer_evaluation', 'Offer Evaluation'),
        ('announced_winner', 'Candidate Winner'),
        ('offer_winner', 'Offer Winner'),
    ], default='received', string='Offer State')
