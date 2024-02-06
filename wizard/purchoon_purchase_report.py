from odoo import api, fields, models, _, tools
from datetime import datetime, date



class PmisCashReport(models.TransientModel):
    _name = "pmis.purchase.pdf.report"
    _description = "PMIS Purchase Report"


    purchase_type = fields.Selection(
        [('below20000', '1 < 20000'), ('upto250000', '20000 < 250000'), ('upto500000', '250000 < 500000')],
        string='Purchase Type', default="")

    purchase_payment_type = fields.Selection(
        [('purchase_payment_cash', 'Cash Payment'), ('purchase_payment_bank', 'Bank Payment'),
         ('purchase_payment_advance', 'Advance Payment')],
        string='Payment Type', default="purchase_payment_cash")

    report_from = fields.Date(string='Report From')
    report_up_to = fields.Date(string='Report To')

    purchase_type = fields.Selection(
        [('below20000', '1 < 20000'), ('upto250000', '20000 < 250000'), ('upto500000', '250000 < 500000')],
        string='purchase type', default="below20000")

    purchase_type = fields.Selection(
        lambda self: self._get_purchase_type_selection(),
        string='purchase_type'
    )

    @api.model
    def _get_purchase_type_selection(self):
        if self.env.user.has_group('egp_procurement.pmis_purchase_managers_less_20000'):
            return [('below20000', '1 < 20000')]
        elif self.env.user.has_group('egp_procurement.pmis_purchase_managers_less_5000000'):
            return [('upto250000', '20000 < 250000'), ('upto500000', '250000 < 500000')]
        elif self.env.user.has_group('egp_procurement.pmis_head'):
            return [('below20000', '1 < 20000'), ('upto250000', '20000 < 250000'), ('upto500000', '250000 < 500000')]
        else:
            return [('below20000', '1 < 20000'), ('upto250000', '20000 < 250000'), ('upto500000', '250000<500000')]
    def action_print_report(self):
        data = {
            'purchase_type': self.purchase_type,
            'purchase_payment_type': self.purchase_payment_type,
            'report_from': self.report_from,
            'report_up_to': self.report_up_to,
        }
        return self.env.ref('egp_procurement.action_pmis_purchoon_purchase_report').report_action(self, data=data)


class PmisCashReportAbstract(models.AbstractModel):
    _name = "report.egp_procurement.purchoon_purchase_report_template"
    _description = "PMIS Purchoon Purchase Report"

    def _get_report_values(self, docids, data=None):
        # docs=''
        domain = []
        if data['purchase_type'] == 'below20000':
            domain.append(('purchase_project_type', '=', 'below20000'))
        elif data['purchase_type'] == 'upto250000':
            domain.append(('purchase_project_type', '=', 'upto250000'))
        elif data['purchase_type'] == 'upto500000':
            domain.append(('purchase_project_type', '=', 'upto500000'))
        else:
            domain.append(('purchase_project_type', 'in', ['below20000', 'upto250000','upto500000']))
        if data.get('report_from'):
            domain.append(('create_date', '>=', data.get('report_from')))
        if data.get('report_up_to'):
            domain.append(('create_date', '<=', data.get('report_up_to')))
        if data.get('purchase_payment_type'):
            domain.append(('purchase_payment_type', '=', data.get('purchase_payment_type')))

        docs = self.env['pmis.purchase.kharidari'].search(domain)

        return {
            'doc_ids': docs.ids,
            'doc_model': 'pmis.purchase.kharidari',
            'docs': docs,
            'datas': data
        }

