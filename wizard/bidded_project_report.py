from odoo import api, fields, models, _, tools
from datetime import datetime, date




class PmisPlanReport(models.TransientModel):
    _name = "pmis.bidded_project.pdf.report"
    _description = "PMIS Plan Report"

    state = fields.Selection([
        ('draft', 'Draft'),
        ('plan', 'Plan'),
        ('announce', 'Announced'),
        ('offer_receiving', 'Offer Receiving'),
        ('offer_opening', 'Opening Offers'),
        ('offer_receiving', 'Offer Receiving'),
        ('offer_evaluation', 'Offer Evaluation'),
        ('won', 'Winner'),
        ('appeal', 'Appeal'),
        ('contract', 'Award'),
        ('payment', 'Payment'),
        ('cancel', 'Cancel'),
    ],
        string='States', default='',)

    report_from = fields.Date(string='Report From')
    report_up_to = fields.Date(string='Report To')

    category_id = fields.Many2one(
        comodel_name='pmis.procurement.category',
        string="Procurement Type")

    cat_id = fields.Integer(string='id')
    @api.onchange('category_id')
    def onchange_category_id(self):
        self.cat_id = self.category_id.id
        print(self.cat_id)

    def action_print_report(self):
        data = {
            'state': self.state,
            'report_from': self.report_from,
            'report_up_to': self.report_up_to,
            'category_id': self.category_id.id,
            'cat_id': self.cat_id,
        }
        return self.env.ref('egp_procurement.action_pmis_bidded_projects_report').report_action(self, data=data)


class PmisPlanReportAbstract(models.AbstractModel):
    _name = "report.egp_procurement.bidded_projects_report_template"
    _description = "PMIS Projects Report"

    def _get_report_values(self, docids, data=None):
        #
        print("type",type(data.get('cat_id')))
        # data['category_id'] == :
        #     print("yes")
        # # test = self.env['pmis.procurement.category'].search([('id','=',data.get('category_id'))])
        # # print(test)
        domain = []
        if data['state']:
            domain.append(('state', '=', data.get('state')))
        if data.get('report_from'):
            domain.append(('create_date', '>=', data.get('report_from')))
        if data.get('report_up_to'):
            domain.append(('create_date', '<=', data.get('report_up_to')))
        if data.get('category_id'):
            domain.append(('category_id', '=',data.get('category_id')))
        docs = self.env['pmis.project'].search(domain)
        print(docs)
        return {
            'doc_ids': docs.ids,
            'doc_model': 'pmis.project',
            'docs': docs,
            'datas': data
        }
