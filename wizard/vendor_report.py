from odoo import api, fields, models, _, tools
from datetime import datetime, date


class PmisCashReport(models.TransientModel):
    _name = "pmis.vendor.pdf.report"
    _description = "PMIS Report Report"

    vendor_type = fields.Selection(
        [('vendor', 'All Vendor'), ('invalid', 'Block Vendor'), ('valid_vendor', 'Valid Vendor')], default='vendor')
    report_from = fields.Date(string='Report From')
    report_up_to = fields.Date(string='Report To')

    def action_print_report(self):
        data = {
            'vendor_type': self.vendor_type,
            'report_from': self.report_from,
            'report_up_to': self.report_up_to,
        }
        return self.env.ref('egp_procurement.action_pmis_vendor_report').report_action(self, data=data)


class PmisCashReportAbstract(models.AbstractModel):
    _name = "report.egp_procurement.vendor_report_template"
    _description = "PMIS Cash Report Domain"

    def _get_report_values(self, docids, data=None):
        # docs=''
        domain = []
        if data['vendor_type'] == 'valid_vendor':
            domain.append(('status', '=', 'valid'))
        elif data['vendor_type'] == 'invalid':
            domain.append(('status', '=', 'invalid'))
        else:
            domain.append(('status', 'in', ['invalid', 'valid']))
        if data.get('report_from'):
            domain.append(('create_date', '>=', data.get('report_from')))
        if data.get('report_up_to'):
            domain.append(('create_date', '<=', data.get('report_up_to')))
        docs = self.env['pmis.vendors'].search(domain)


        return {
            'doc_ids': docs.ids,
            'doc_model': 'pmis.vendors',
            'docs': docs,
            'datas': data
        }
