from odoo import api, fields, models, _, tools
from datetime import datetime, date
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT
from datetime import datetime


class PmisConsultativeOfferGhoshai(models.Model):
    _name = "pmis.consultative.offerghoshai"
    _description = "pmis consultative offerghoshai"
    _rec_name = "offerghoshai_shortlist_project_id"
    #
    # offer_shortlist_project_id = fields.Many2one('pmis.candidate.proposal', required=True,
    #                                              string='Project Name', )
    offerghoshai_shortlist_project_id = fields.Many2one('pmis.consultative.offerghoshai.project', required=True,
                                                        string='Project Name', )
    offerghoshai_type = fields.Selection(
        [('financial', 'Financial Offer Ghoshai'), ('technical', 'Technical Offer Ghoshai')],
        string='Offer Ghoshai Type', required=True)

    meeting_address = fields.Char(string='Meeting Address', default='MCIT 13 Floor Procurement Office Meeting Room', )

    offerghoshi_date = fields.Date(string='Technical Date', required=True, default=fields.Date.context_today)
    start_hour = fields.Datetime(string='Technical Start Hour')
    end_hour = fields.Datetime(string='Technical End Hour')

    note = fields.Text(string='Comments')

    consultative_offerghoshai_agent_ids = fields.One2many('pmis.vendor.agent', 'consultative_offerghoshai_id',
                                                          string='Offerghoshai Agent')

    basic_evaluation_ids = fields.One2many('pmis.consultative.basic.evaluation', 'basic_evaluation_id',
                                           string='Basic Evaluation')



