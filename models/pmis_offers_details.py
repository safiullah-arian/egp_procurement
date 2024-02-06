from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class PmisOffersDetails(models.Model):
    _name = "pmis.offers.details"
    _inherit = ['mail.thread']
    _description = "Offer's Details"
    _rec_name = "offer_ghoshai_project_id"

    # this is to use  information

    offer_ghoshai_project_id = fields.Many2one('pmis.offerghoshai', string="Project",
                                               domain=[(
                                                   'offer_submission_project_id.announced_project_id.planned_project_id.project_id.state',
                                                   '=',
                                                   'offer_opening')],
                                               required=True,
                                               )
    project_number = fields.Char(string='Project Number',
                                 related='offer_ghoshai_project_id.offer_submission_project_id.announced_project_id.planned_project_id.project_id.project_number')

    category_id = fields.Many2one(related='offer_ghoshai_project_id.category_id',
                                  string='Catagory')

    offer_submassion_details_ids = fields.One2many('pmis.offersubmission', 'offers_details_id',
                                                   string="offer's Details")



    @api.onchange('offer_ghoshai_project_id')
    def onchange_offer_ghoshai_project_id(self):
        self.project_name = self.offer_ghoshai_project_id.offer_submission_project_id.announced_project_id.planned_project_id.project_id.id
        print("test", self.project_name)

    project_name = fields.Integer(string='Project Id')

    @api.model
    def create(self, vals):
        self.env['pmis.project'].browse(vals['project_name']).write({'state': 'offer_details'})
        print("Creation triggered", vals['project_name'])
        return super(PmisOffersDetails, self).create(vals)

    def unlink(self):
        for rec in self.offer_submassion_details_ids:
            for offer in rec.available_offer_ids:
                if offer.state == 'offer_details':
                    self.env['pmis.offer_submission'].browse(offer.id).write({'state': 'offer_ghoshai'})
        self.env['pmis.project'].browse(self.project_name).write({'state': 'offer_opening'})
        return super(PmisOffersDetails, self).unlink()
