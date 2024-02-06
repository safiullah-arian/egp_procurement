from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class PMISOfferSubmission(models.Model):
    _name = "pmis.offersubmission"
    _inherit = ['mail.thread']
    _description = "bidding details"
    _rec_name = "received_offers_id"

    project_number = fields.Char(string='Project Number',
                                 related='offers_details_id.offer_ghoshai_project_id.offer_submission_project_id.announced_project_id.planned_project_id.project_id.project_number')

    received_offers_id = fields.Many2one('pmis.offer_submission', required=True, string="Received Offer's",
                                         domain="[('id', 'in', available_offer_ids),('state', '=', 'offer_ghoshai')]"
                                         )

    offers_details_id = fields.Many2one('pmis.offers.details', string="Offer Details")

    category_id = fields.Many2one(related='offers_details_id.category_id',
                                  string='Catagory')

    product_price_ids = fields.One2many(
        comodel_name='pmis.products.price',
        inverse_name='submission_id',

    )

    total_price = fields.Float(string='Offer Total Amount')

    available_offer_ids = fields.Many2many(
        comodel_name='pmis.offer_submission',
        compute='_compute_available_offers_ids'
    )

    @api.depends('offers_details_id')
    def _compute_available_offers_ids(self):
        for rec in self:
            rec.available_offer_ids = rec.offers_details_id.offer_ghoshai_project_id.offers_submission_ids

    @api.onchange('product_price_ids')
    def _compute_quotation_total(self):
        self.total_price = 0.0
        for rec in self.product_price_ids:
            self.total_price = self.total_price + rec.sub_total

    @api.onchange('offers_details_id')
    def onchange_offer_details_id(self):
        for rec in self:
            product_lines = [(5, 0, 0)]
            for product in self.offers_details_id.offer_ghoshai_project_id.offer_submission_project_id.announced_project_id.planned_project_id.project_id.products_ids:
                vals = {
                    'product_description_id': product.id,
                    'name': product.product_id.name,
                    'unit': product.product_id.unit,
                    'description': product.description,
                    'qty': product.qty
                }
                product_lines.append((0, 0, vals))
        self.product_price_ids = product_lines

        if self.offers_details_id:
            domain = [('submission_project_id', '=',
                       self.offers_details_id.offer_ghoshai_project_id.offer_submission_project_id.id)]
            domain.append(('state', '=', 'offer_ghoshai'))
            return {'domain': {'received_offers_id': domain}}
        else:
            return {'domain': {'received_offers_id': []}}

    # this is linked with other models:

    company_agent_ids = fields.One2many('pmis.vendor.agent', 'offer_submission_id', string='Received from')

    documents_ids = fields.One2many('pmis.documents', 'submission_id', string='Documents')

    implied_services_ids = fields.One2many('implied.services', 'implied_services_id', string='Implied services')

    guarantee_ids = fields.One2many('guaranteefor.bank', 'guarantee_submission_id', string='Project Guarantee')

    product_permit_ids = fields.One2many('production.permit', 'product_permit_id', string='Production Permit')

    construction_section_ids = fields.One2many('pmis.construction.section', 'details_section_id',
                                               string='Construction Details', )

    pmis_services_price_ids = fields.One2many('pmis.services.price', 'construction_submission_id',
                                              string='Services Prices')
    construction_total_price = fields.Float(string='Construction Total Amount')

    @api.onchange('pmis_services_price_ids')
    def _compute_construction_total(self):
        self.construction_total_price = 0.0
        for rec in self.pmis_services_price_ids:
            self.construction_total_price += rec.sub_total

    @api.onchange('offers_details_id')
    def onchange_offers_details_id(self):
        for rec in self:
            services_prices = []
            for section in rec.construction_section_ids:
                for service in section.services_ids:
                    service_vals = {
                        'name': section.name,
                        'work_description': service.work_description,
                        'qty': service.work_amount,
                        'unit_measure': service.unit_measure,
                        'note': service.note,

                    }
                    # print(service_vals)
                    services_prices.append((0, 0, service_vals))

            rec.pmis_services_price_ids = services_prices
        if self.offers_details_id:
            domain = [('submission_project_id', '=',
                       self.offers_details_id.offer_ghoshai_project_id.offer_submission_project_id.id)]
            domain.append(('state', '=', 'offer_ghoshai'))
            return {'domain': {'received_offers_id': domain}}
        else:
            return {'domain': {'received_offers_id': []}}

    construction_services_ids = fields.One2many('pmis.construction.services', 'details_services_id',
                                                string='Construction Details', )

    @api.onchange('offers_details_id')
    def onchange_implied_services_offers_details_id(self):
        for rec in self:
            product_lines = [(5, 0, 0)]
            for product in self.offers_details_id.offer_ghoshai_project_id.offer_submission_project_id.announced_project_id.planned_project_id.project_id.products_ids:
                vals = {
                    'product_description_id': product.id,
                    'qty': product.qty
                }
                product_lines.append((0, 0, vals))
            self.implied_services_ids = product_lines

    @api.onchange('offers_details_id')
    def onchange_production_permit_offers_details_id(self):
        for rec in self:
            product_lines = [(5, 0, 0)]
            for product in self.offers_details_id.offer_ghoshai_project_id.offer_submission_project_id.announced_project_id.planned_project_id.project_id.products_ids:
                vals = {
                    'product_description_id': product.id,
                }
                product_lines.append((0, 0, vals))
            self.product_permit_ids = product_lines

    @api.onchange('offers_details_id')
    def onchange_construction_details_id(self):
        for rec in self:
            construction_sections = []
            for construction_section in rec.offers_details_id.offer_ghoshai_project_id.offer_submission_project_id.announced_project_id.planned_project_id.project_id.section_ids:
                vals = {
                    'name': construction_section.name,
                    'services_ids': [(0, 0, {
                        'work_description': service.work_description,
                        'work_amount': service.work_amount,
                        'unit_measure': service.unit_measure,

                        'note': service.note,
                    }) for service in construction_section.services_ids]
                }
                construction_sections.append((0, 0, vals))
            self.construction_section_ids = construction_sections

    @api.onchange('received_offers_id')
    def onchange_received_offers_id(self):
        self.offer_state = self.received_offers_id.id

    offer_state = fields.Integer(string='Offer state')

    @api.model
    def create(self, vals):
        self.env['pmis.offer_submission'].browse(vals['offer_state']).write({'state': 'offer_details'})
        print("Creation triggered", vals['offer_state'])
        return super(PMISOfferSubmission, self).create(vals)

    def unlink(self):
        # print("Delete triggered", self.project_id.id)

        self.env['pmis.offer_submission'].browse(self.offer_state).write({'state': 'offer_ghoshai'})
        print(self.offer_state)
        return super(PMISOfferSubmission, self).unlink()
