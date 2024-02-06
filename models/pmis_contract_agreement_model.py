from odoo import api, fields, models, _


class PMISContractAgreement(models.Model):
    _name = "pmis.contractagreement"
    _inherit = ['mail.thread']
    _description = "Bidding Offer Acceptance Letter Records"

    contract_agree_date = fields.Date(string='Contract Agreement Date')
    department_name = fields.Many2one(string='Department Name',
                                      related="winner_bidding_agreement_id.evaluated_project_id.evaluation_Project_id.offer_details_id.offer_ghoshai_project_id.offer_submission_project_id.announced_project_id.planned_project_id.project_id.directorates_id")
    contract_start_date = fields.Date(string='Contract Start Date')
    contract_expiry_date = fields.Date(string='Contract Expiry Date')
    department_representative = fields.Char(string='Department Representative')
    department_representative_job = fields.Char(string='Dep Rep Job', )
    supplier_representative_name = fields.Char(string='Supplier Rep Name')
    supplier_representative_job = fields.Char(string='Supplier Rep Job', )
    ref = fields.Char(string='Reference', default=lambda self: _('New'))
    notes = fields.Text(string='Notes')

    winner_bidding_agreement_id = fields.Many2one('bidding.winner', string="Winner Bidding")
