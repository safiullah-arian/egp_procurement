from odoo import api, fields, models, _, tools
from datetime import datetime, date
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT
from datetime import datetime


class PmisConsultativeOfferGhoshaiProject(models.Model):
    _name = "pmis.consultative.offerghoshai.project"
    _description = "pmis consultative offerghoshai project"
    _rec_name = "offer_shortlist_project_id"

    offer_shortlist_project_id = fields.Many2one('pmis.candidate.proposal', required=True,
                                                 string='Project Name',
                                                 domain="[('shortlist_id.shortlist_project_id.job_title_id.planned_project_id.project_id.state', '=', 'consult_offers_received')]")

    offerghoshai_details_ids = fields.One2many('pmis.consultative.offerghoshai', 'offerghoshai_shortlist_project_id',
                                               string='Offer Ghoshai Details')

    @api.onchange('offer_shortlist_project_id')
    def onchange_offer_shortlist_project_id(self):
        self.project_name = self.offer_shortlist_project_id.shortlist_id.shortlist_project_id.job_title_id.planned_project_id.project_id.id

    project_name = fields.Integer(string='Project Id')
    offerghoshai_agent_ids = fields.One2many('pmis.vendor.agent', 'offer_m_ghoshai_id', string='Offerghoshai Agent')

    @api.model
    def create(self, vals):
        self.env['pmis.project'].browse(vals['project_name']).write({'state': 'consult_offersghoshai'})
        print("Creation triggered", vals['project_name'])
        return super(PmisConsultativeOfferGhoshaiProject, self).create(vals)

    def unlink(self):
        # print("Delete triggered", self.project_id.id)
        self.env['pmis.project'].browse(self.project_name).write({'state': 'consult_offers_received'})
        print(self.project_name)
        return super(PmisConsultativeOfferGhoshaiProject, self).unlink()
