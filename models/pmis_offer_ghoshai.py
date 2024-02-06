from odoo import api, fields, models, _, tools
from datetime import datetime, date
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT
from datetime import datetime


class PmisOfferGhoshai(models.Model):
    _name = "pmis.offerghoshai"
    _description = "Offer Ghoshai information"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = "offer_submission_project_id"

    offer_submission_project_id = fields.Many2one('pmis.offer_submission_project', required=True, string='Project Name',
                                                  domain=[(
                                                      'announced_project_id.planned_project_id.project_id.state',
                                                      '=',
                                                      'received_offers')],
                                                  )
    offers_submission_ids = fields.One2many(related='offer_submission_project_id.offers_submission_ids',
                                            string='Offer Submission')
    project_number = fields.Char(string='Project Number',
                                 related='offer_submission_project_id.announced_project_id.planned_project_id.project_id.project_number')

    offer_ghoshai_date = fields.Date(string='Date', required=True, default=fields.Date.context_today)

    meeting_address = fields.Char(string='Meeting Address', default='MCIT 14 Floor Procurement Office Meeting Room', )
    start_hour = fields.Datetime(string='Start Hour')
    start_hour1 = fields.Char(string='Start Time', compute='_compute_time', store=True)
    finish_hour1 = fields.Char(string='Finish Time', compute='_compute_time', store=True)

    @api.depends('start_hour', 'end_hour')
    def _compute_time(self):
        for record in self:
            start_hour1 = 0
            finish_hour1 = 0
            if record.start_hour:
                start_hour1 = record.start_hour.strftime('%H:%M:%S')
                record.start_hour1 = start_hour1
            else:
                record.start_hour1 = False
            if record.end_hour:
                finish_hour1 = record.end_hour.strftime('%H:%M:%S')
                record.finish_hour1 = finish_hour1
            else:
                record.finish_hour1 = False

    end_hour = fields.Datetime(string='End Hour')
    category_id = fields.Many2one(related='offer_submission_project_id.category_id',
                                  string='Catagory')

    day_name = fields.Char(string='Day Name', compute='_compute_day_name', store=True)

    def _compute_day_name(self):
        for record in self:
            if record.offer_ghoshai_date:
                # Calculate the day name using strftime('%A')
                day_name = record.offer_ghoshai_date.strftime('%A')
                record.day_name = day_name
            else:
                record.day_name = False

    note = fields.Text(string='Comments')

    offerghoshai_agent_ids = fields.One2many('pmis.vendor.agent', 'offer_ghoshai_id', string='Offerghoshai Agent')

    basic_evaluation_ids = fields.One2many('basic.evaluation', 'basic_evaluation_id', string='Basic Evaluation')

    number_offers = fields.Integer(string='Number of offers', compute="_compute_number_of_offers", store=True)
    present_offers = fields.Integer(string='Present offers', compute="_compute_present_offers", store=True)
    sealed_offers = fields.Integer(string='Sealed offers', compute="_compute_present_offers", store=True)
    tadel_changes = fields.Integer(string='Changes offers', compute="_compute_present_offers", store=True)
    discount = fields.Integer(string='Discount offers', compute="_compute_present_offers", store=True)

    @api.depends('basic_evaluation_ids')
    def _compute_present_offers(self):
        present_offers = 0
        sealed_offers = 0
        tadel_changes = 0
        discount = 0
        for record in self.basic_evaluation_ids:
            present_offers += 1
            for rec in record.basic_evaluation_checkbox_ids:
                if rec.is_packet_stamped == True:
                    sealed_offers += 1
                if rec.tadel_changes == True:
                    tadel_changes += 1
                if rec.discount == True:
                    discount += 1

        self.present_offers = present_offers
        self.sealed_offers = sealed_offers
        self.tadel_changes = tadel_changes
        self.discount = discount

    @api.depends('offer_submission_project_id.offers_submission_ids')

    def _compute_number_of_offers(self):
        number_offers = 0
        for record in self.offer_submission_project_id.offers_submission_ids:
            number_offers += 1
        self.number_offers = number_offers


    @api.onchange('end_hour')
    def _onchange_end_hour(self):
        if self.start_hour and self.end_hour < self.start_hour:
            return {'warning': {'title': 'Warning', 'message': 'End Hour should be greater than Start Hour'}}


    @api.onchange('offer_submission_project_id')


    def onchange_offer_submission_project_id(self):
        self.project_name = self.offer_submission_project_id.announced_project_id.planned_project_id.project_id.id
        print("test", self.project_name)


    project_name = fields.Integer(string='Project Id')


    @api.model


    def create(self, vals):
        self.env['pmis.project'].browse(vals['project_name']).write({'state': 'offer_opening'})
        print("Creation triggered", vals['project_name'])
        return super(PmisOfferGhoshai, self).create(vals)


    def unlink(self):
        # print("Delete triggered", self.project_id.id)
        for rec in self.basic_evaluation_ids:
            for offer in rec.available_offer_ids:
                if offer.state == 'offer_ghoshai':
                    # print(rec)
                    self.env['pmis.offer_submission'].browse(offer.id).write({'state': 'received'})

        self.env['pmis.project'].browse(self.project_name).write({'state': 'received_offers'})
        print("Offer deletion", self.project_name)

        return super(PmisOfferGhoshai, self).unlink()
# =======
#         return super(PmisOfferGhoshai, self).unlink()
# >>>>>>> 79db0a36702d6f5406753fdaa88a8ca0d0efdc01
