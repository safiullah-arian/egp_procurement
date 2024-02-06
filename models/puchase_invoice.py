from odoo import api, fields, models, _, tools
from datetime import datetime, date
from odoo.exceptions import ValidationError



class PmisCahsReception(models.Model):
    _name = 'pmis.cash.reception'
    _description = 'Receiving Cash From Finance Department'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'director'

    director = fields.Many2one('pmis.vendor.agent', 'Received By', required=True)
    amount = fields.Float(string=' Cash Received', tracking=True  ,required=True)
    remaining_cash = fields.Float(string=' Cash Remaining', compute='compute_remaining')
    remain_cash = fields.Float(string=' Cash Remaining')
    expenses = fields.Float(string='Expenses', tracking=True)
    refund_cash = fields.Float(string='Refund Cash', tracking=True)
    date = fields.Date(string='Date',required=True)
    recived_from = fields.Many2one('pmis.vendor.agent', 'Received From',required=True)
    attachment = fields.Binary(string='Documents')

    @api.depends('expenses','amount','refund_cash')
    def compute_remaining(self):
        for rec in self:
            rec.remaining_cash = rec.amount - (rec.expenses + rec.refund_cash)
            rec.remain_cash =   rec.remaining_cash

    purchase_ids = fields.One2many(
        comodel_name ='pmis.purchase.kharidari',
        inverse_name = 'purchase_payment_cash',
        readonly=False

    )


class PmisCashRefund(models.Model):
    _name = 'pmis.cash.refund'
    _description = 'Refund Extra Cash From to Finance Directorate'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'cash_reception_id'

    cash_reception_id = fields.Many2one('pmis.cash.reception', string= 'Refund From',  domain = [('remain_cash', '!=', 0.00)] ,required=True)
    amount = fields.Float(string='Refund Amount', tracking=True ,required=True)
    cash_reception_id_index = fields.Integer(string=' Cash Reception Index')
    date = fields.Date(string='Date',required=True)
    refunt_to = fields.Many2one('pmis.vendor.agent', 'Refund To' ,required=True)
    attachment = fields.Binary(string='Documents')


    @api.onchange('cash_reception_id')
    def compute_remaining(self):
            self.amount = self.cash_reception_id.remaining_cash
            self.cash_reception_id_index = self.cash_reception_id.id

    @api.model
    def create(self, vals):
        self.env['pmis.cash.reception'].browse(vals['cash_reception_id_index']).write({'refund_cash': vals['amount']})
        return super(PmisCashRefund, self).create(vals)


    def write(self, vals):
        return super(PmisCashRefund, self).write(vals)


    def unlink(self):
        return super(PmisCashRefund, self).unlink()
