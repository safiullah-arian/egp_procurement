from odoo import api, fields, models, _, tools
from datetime import datetime, date




class PmisPlanReport(models.TransientModel):
    _name = "pmis.plan.pdf.report"
    _description = "PMIS Plan Report"

    category_id = fields.Many2one(
        comodel_name='pmis.procurement.category',
        string="Procurement Type", default=1)
    financial_year = fields.Integer(string='Financial Year',
                                    limit=4,
                                    default=date.today().year
                                    )

    def action_print_report(self):
        data = {
            'category_id': self.category_id.id,
            'financial_year': self.financial_year,
        }
        return self.env.ref('egp_procurement.action_pmis_plan_report').report_action(self, data=data)


class PmisPlanReportAbstract(models.AbstractModel):
    _name = "report.egp_procurement.pmis_plan_report_template"
    _description = "PMIS Plan Report"

    def _get_report_values(self, docids, data=None):

        domain = []
        if data['category_id'] == 1:
            domain.append(('category_id', '=', 1))
        elif data['category_id'] == 2:
            domain.append(('category_id', '=', 2))
        elif data['category_id'] == 3:
            domain.append(('category_id', '=', 3))
        else:
            domain.append(('category_id', 'in', [1, 2, 3]))
        if data.get('financial_year'):
            domain.append(('financial_year', '=', data.get('financial_year')))
        # if data.get('report_up_to'):
        #     domain.append(('create_date', '<=', data.get('report_up_to')))
        docs = self.env['pmis.plan.template'].search(domain)

        # data.update(
        #     {'cash_reception_by_name': cash_reception_by_name,
        #      'cash_reception_by_role': cash_reception_by_role,
        #      'cash_reception_date': cash_reception_date,
        #      'cash_reception_from_name': cash_reception_from_name,
        #      'refund_cash': refund_cash,
        #      'cash_reception_report_up_to_date': Date.today()})

        return {
            'doc_ids': docs.ids,
            'doc_model': 'pmis.plan.template',
            'docs': docs,
            'datas': data
        }
