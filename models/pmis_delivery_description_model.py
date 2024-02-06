from odoo import api, fields, models, _, tools
from datetime import datetime, date
from odoo.exceptions import ValidationError


class PmisDeliveryDescription(models.Model):
    _name = 'pmis.delivery.description'
    _description = 'Description and Delivery for Procurement'
    _rec_name = "contract_project_id"

    contract_project_id = fields.Many2one('pmis.contract.management',
                                          domain=[(
                                              'winner_id.evaluated_project_id.evaluation_Project_id.offer_details_id.offer_ghoshai_project_id.offer_submission_project_id.announced_project_id.planned_project_id.project_id.state',
                                              '=',
                                              'contract')], string='Project', required=True)
    contract_project_name_id = fields.Many2one(string="Project Name", related="contract_project_id")
    delivery_date = fields.Date(string='Delivery Date', default=fields.Date.context_today)
    vendor_id = fields.Many2one('pmis.vendors', string='Vendor', related="contract_project_id.vendor_id")
    Offer_number = fields.Char(string='Project Number', related="contract_project_id.contract_number")
    warehouse = fields.Selection([
        ('it', 'IT store'),
        ('goods', 'Goods store'),
        ('construction', 'Construction store'),
    ], string='Places in Warehouse', default="goods")
    notes = fields.Text(string='Notes')


    category_id = fields.Many2one('pmis.procurement.category', string='Procurement Type', related="contract_project_id.winner_id.evaluated_project_id.evaluation_Project_id.offer_details_id.offer_ghoshai_project_id.offer_submission_project_id.announced_project_id.planned_project_id.project_id.category_id")

    # product_id = fields.Many2one('pmis.products.price', string='Product')
    # quantity = fields.Integer(string='Quantity', related="product_id.qty")
    # unit_of_measure = fields.Selection([('m', 'Meter'), ('kg', 'Kilo Geram'), ('n', 'Number')],
    #                                    string='Unit',
    #                                    related='product_id.unit')

    #
    delivery_services_ids = fields.One2many('pmis.services.delivery', 'delivery_service_id', string='Delivery Services')

    @api.onchange('contract_project_id')
    def onchange_delivery_services_id(self):
        for rec in self:
            services_prices = []
            for section in rec.contract_project_id.winner_id.evaluated_project_id.evaluation_Project_id.offer_details_id.offer_ghoshai_project_id.offer_submission_project_id.announced_project_id.planned_project_id.project_id.section_ids:
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

            rec.delivery_services_ids = services_prices

    delivery_product_ids = fields.One2many('delivery.product', 'delivery_product_id', string='Delivery Product')

    @api.onchange('contract_project_id')
    def onchange_delivery_products_contract_project_id(self):
        for rec in self:
            product_lines = [(5, 0, 0)]
            for product in self.contract_project_id.winner_id.evaluated_project_id.evaluation_Project_id.offer_details_id.offer_ghoshai_project_id.offer_submission_project_id.announced_project_id.planned_project_id.project_id.products_ids:
                vals = {
                    'product_description_id': product.id,
                    'unit': product.product_id.unit,
                    'description': product.description,
                    'qty': product.qty
                }
                print(product)
                product_lines.append((0, 0, vals))
            self.delivery_product_ids = product_lines

    vendor_agent_ids = fields.One2many('pmis.vendor.agent', 'delivery_id', string='Vendor Agent')

    document_ids = fields.One2many('pmis.documents', 'delivery_doc_id', string="Document")

    invoice_ids = fields.One2many('pmis.invoice', 'delivery_id', string="Invoice")

    m7_ids = fields.One2many('pmis.m_seven', 'delivery_id', string="M7")

    @api.onchange('contract_project_id')
    def onchange_contract_project_id(self):
        self.project_name = self.contract_project_id.winner_id.evaluated_project_id.evaluation_Project_id.offer_details_id.offer_ghoshai_project_id.offer_submission_project_id.announced_project_id.planned_project_id.project_id.id
        print("test", self.project_name)

    project_name = fields.Integer(string='Project Id')

    @api.model
    def create(self, vals):
        self.env['pmis.project'].browse(vals['project_name']).write({'state': 'delivery'})
        print("Creation triggered", vals['project_name'])
        return super(PmisDeliveryDescription, self).create(vals)

    def unlink(self):
        # print("Delete triggered", self.project_id.id)
        self.env['pmis.project'].browse(self.project_name).write({'state': 'contract'})
        print("Offer deletion", self.project_name)
        return super(PmisDeliveryDescription, self).unlink()


class delivery_product(models.Model):
    _name = "delivery.product"
    _description = "delivery product"

    product_description_id = fields.Many2one(
        comodel_name="pmis.products.description",
        string="Products ",
        readonly=False,
    )
    unit = fields.Selection([('m', 'Meter'), ('kg', 'Kilo Geram'), ('n', 'Number')], string='Unit', required=True,
                            )
    qty = fields.Integer(string='Quantity')
    description = fields.Char(string='Description')

    is_delivery = fields.Boolean(string="Is Delivery")
    details = fields.Text(string="Note")
    delivery_product_id = fields.Many2one('pmis.delivery.description', string='Delivery Product')


class PmisServicesdelivery(models.Model):
    _name = "pmis.services.delivery"
    _description = "Services Delivery"
    _rec_name = 'name'

    name = fields.Char(string='Section name')
    work_description = fields.Text(string='Description')
    qty = fields.Integer(string='Work Quantity')
    unit_measure = fields.Selection([('m', 'Meter'), ('m3', 'Square meter'), ('ft', 'Foot'), ('m3', 'Cubic meter')],
                                    string='Unit/Measure')
    note = fields.Text(string='Details')

    delivery_service_id = fields.Many2one('pmis.delivery.description', string='Delivery Product')
    is_service_delivery = fields.Boolean(string="Is Done")
    details = fields.Text(string="Note")
