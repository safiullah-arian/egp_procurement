from odoo import api, fields, models


class Payment(models.Model):
    _name = 'pmis.payment'
    _description = 'Payment Information'
    _rec_name = "delivery_project_id"

    delivery_project_id = fields.Many2one('pmis.delivery.description',
                                          domain=[(
                                              'contract_project_id.winner_id.evaluated_project_id.evaluation_Project_id.offer_details_id.offer_ghoshai_project_id.offer_submission_project_id.announced_project_id.planned_project_id.project_id.state',
                                              '=',
                                              'delivery')], string='Delivery',required=True)
    delivery_project_name_id = fields.Many2one(string="Project Name", related="delivery_project_id")
    note = fields.Text(string='Note')
    payment_ids = fields.One2many('pmis.project.payment', 'payment_id', string='Payment')

    @api.onchange('delivery_project_id')
    def onchange_delivery_project_id(self):
        self.project_name = self.delivery_project_id.contract_project_id.winner_id.evaluated_project_id.evaluation_Project_id.offer_details_id.offer_ghoshai_project_id.offer_submission_project_id.announced_project_id.planned_project_id.project_id.id
        print("test", self.project_name)

    project_name = fields.Integer(string='Project Id')

    @api.model
    def create(self, vals):
        self.env['pmis.project'].browse(vals['project_name']).write({'state': 'payment'})
        print("Creation triggered", vals['project_name'])
        return super(Payment, self).create(vals)

    def unlink(self):
        # print("Delete triggered", self.project_id.id)
        self.env['pmis.project'].browse(self.project_name).write({'state': 'delivery'})
        print("Offer deletion", self.project_name)
        return super(Payment, self).unlink()


class PmisPayment(models.Model):
    _name = 'pmis.project.payment'
    _description = 'Payment Information'
    _rec_name = "invoice_id"

    payment_number = fields.Char(string='Payment Number', required=True)
    invoice_id = fields.Char(string='Invoice')
    payment_date = fields.Date(string='Payment Date', default=fields.Date.today())
    payment_amount = fields.Float(string='Payment Amount')
    payment_method = fields.Selection([
        ('cash', 'Cash'),
        ('credit_card', 'Credit Card'),
        ('bank_transfer', 'Bank Transfer'),
        ('check', 'Check'),
        ('other', 'Other'),
    ], string='Payment Method')
    payment_id = fields.Many2one('pmis.payment', string='Delivery')
