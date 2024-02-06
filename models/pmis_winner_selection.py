from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import datetime, date


class PmisBiddingWinnerSelection(models.Model):
    _name = 'pmis.winner.selection'
    _description = 'Bidding Winner Information'
    _rec_name = 'evaluated_winner_id'

    evaluated_winner_id = fields.Many2one('pmis.offers.evaluation', string='Evaluated Winner Project',
                                          default='_default_evaluated_winner')
    project_number = fields.Char(string='Project Number',
                                 related='evaluated_winner_id.offer_details_id.offer_ghoshai_project_id.offer_submission_project_id.announced_project_id.planned_project_id.project_id.project_number')
    project_name_id = fields.Many2one(string='Project Name', related='evaluated_winner_id')
    winning_offer_list_id = fields.Many2one(
        'pmis.offer_submission',
        string='Winning Offer'
    )

    @api.model
    def _default_evaluated_winner(self):
        # Get the default value based on project_name_id
        project_name_id = self.env.context.get('default_project_name_id')
        if project_name_id:
            # Find the appropriate evaluated_winner_id based on project_name_id
            evaluated_winner = self.env['pmis.offers.evaluation'].search([('project_name_id', '=', project_name_id)],
                                                                         limit=1)
            return evaluated_winner.id if evaluated_winner else False
        return False

    @api.onchange('project_name_id')
    def onchange_project_name_id(self):
        domain = [('submission_project_id', '=',
                   self.evaluated_winner_id.offer_details_id.offer_ghoshai_project_id.offer_submission_project_id.id)]
        domain.append(('state', '=', 'offer_evaluation'))
        if self.project_name_id:

            return {'domain': {'winning_offer_list_id': domain}}
        else:
            return {'domain': {'winning_offer_list_id': domain}}

    @api.onchange('details_offer_id')
    def onchange_details_offer_id(self):
        self.offer_state = self.winning_offer_list_id.id

    offer_state = fields.Integer(string='Offer state')

    @api.model
    def create(self, vals):
        self.env['pmis.offer_submission'].browse(vals['offer_state']).write({'state': 'offer_winner'})
        print("Creation triggered", vals['offer_state'])
        return super(PmisBiddingWinnerSelection, self).create(vals)

    def unlink(self):
        # print("Delete triggered", self.project_id.id)
        self.env['pmis.offer_submission'].browse(self.offer_state).write({'state': 'offer_evaluation'})
        print(self.offer_state)
        return super(PmisBiddingWinnerSelection, self).unlink()
