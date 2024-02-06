from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class PmisOffersEvaluation(models.Model):
    _name = "pmis.offers.evaluation"
    _inherit = ['mail.thread']
    _description = "Offer's Evaluations"
    _rec_name = "offer_details_id"

    # this is to use bidding information

    offer_details_id = fields.Many2one('pmis.offers.details', string="Project",
                                       domain=[(
                                           'offer_ghoshai_project_id.offer_submission_project_id.announced_project_id.planned_project_id.project_id.state',
                                           '=',
                                           'offer_details')],
                                       )
    project_number = fields.Char(string='Project Number',
                                 related='offer_details_id.offer_ghoshai_project_id.offer_submission_project_id.announced_project_id.planned_project_id.project_id.project_number')

    offer_evaluation_ids = fields.One2many('pmis.offer', 'offers_evaluation_id', string="offer's Evaluation")

    offer_evaluation_agents_ids = fields.One2many('pmis.vendor.agent', 'offer_evaluation_id', string='Offer Evaluation  Agents')

    @api.onchange('offer_details_id')
    def onchange_offer_details_id(self):
        self.project_name = self.offer_details_id.offer_ghoshai_project_id.offer_submission_project_id.announced_project_id.planned_project_id.project_id.id
        print("test", self.project_name)

    project_name = fields.Integer(string='Project Id')

    @api.model
    def create(self, vals):
        self.env['pmis.project'].browse(vals['project_name']).write({'state': 'offer_testing'})
        print("Creation triggered", vals['project_name'])
        return super(PmisOffersEvaluation, self).create(vals)

    def unlink(self):
        # print("Delete triggered", self.project_id.id)
        for rec in self.offer_evaluation_ids:
            for offer in rec.available_offer_ids:
                if offer.state == 'offer_evaluation':
                    # print(rec)
                    self.env['pmis.offer_submission'].browse(offer.id).write({'state': 'offer_details'})
        self.env['pmis.project'].browse(self.project_name).write({'state': 'offer_details'})
        print("Offer deletion", self.project_name)
        return super(PmisOffersEvaluation, self).unlink()
