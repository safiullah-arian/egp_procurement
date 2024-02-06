from odoo import api, fields, models, _, tools
from datetime import datetime, date



class PmisCashReport(models.TransientModel):
    _name = "pmis.cash.pdf.report"
    _description = "PMIS Cash Report"

    cash_reception_id = fields.Many2one('pmis.cash.reception', string='Cash Reception')
    amount = fields.Float(string='Amount', related='cash_reception_id.amount')


    def action_print_report(self):
        data = {
            'cash_reception_id': self.cash_reception_id.id,
            'amount': self.amount,
        }
        return self.env.ref('egp_procurement.action_pmis_cash_report').report_action(self, data=data)


class PmisCashReportAbstract(models.AbstractModel):
    _name = "report.egp_procurement.cash_report_template"
    _description = "PMIS Cash Report Domain"

    def _get_report_values(self, docids, data=None):
        docs = self.env['pmis.purchase.kharidari'].search([('purchase_payment_cash', '=', data['cash_reception_id'])])
        cash_reception_by_name = self.env['pmis.cash.reception'].browse(data.get('cash_reception_id')).director.name
        refund_cash = self.env['pmis.cash.reception'].browse(data.get('cash_reception_id')).refund_cash
        cash_reception_from_name = self.env['pmis.cash.reception'].browse(data.get('cash_reception_id')).recived_from.name
        cash_reception_by_role = self.env['pmis.cash.reception'].browse(data.get('cash_reception_id')).director.position_title
        cash_reception_date = self.env['pmis.cash.reception'].browse(data.get('cash_reception_id')).date


        data.update(
            {'cash_reception_by_name': cash_reception_by_name,
             'cash_reception_by_role': cash_reception_by_role,
             'cash_reception_date': cash_reception_date,
             'cash_reception_from_name': cash_reception_from_name,
             'refund_cash': refund_cash,
             'cash_reception_report_up_to_date': date.today()})

        return {
            'doc_ids': docs.ids,
            'doc_model': 'pmis.purchase.kharidari',
            'docs': docs,
            'datas': data
        }

