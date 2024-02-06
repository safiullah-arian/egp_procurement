from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import datetime, date


class PmisProducts(models.Model):
    _name = "pmis.products"
    _description = "Product Model "

    name = fields.Char(string='Name', required=True)
    unit = fields.Selection([('m', 'Meter'), ('kg', 'Kilo Geram'), ('n', 'Number')], string='Unit', required=True)


class PmisProductsDescription(models.Model):
    _name = "pmis.products.description"
    _description = "Products Price "
    _rec_name = 'product_id'

    unit = fields.Selection([('m', 'Meter'), ('kg', 'Kilo Geram'), ('n', 'Number')], string='Unit', required=True,
                            related='product_id.unit')
    qty = fields.Integer(string='Quantity', required=True)
    description = fields.Char(string='Description', required=False, help='Description')
    price = fields.Float(string='Price')
    sub_total = fields.Float(string='Sub Total', compute="_compute_sub_total")
    product_id = fields.Many2one(
        comodel_name="pmis.products",
        string="Products",
        readonly=False,
        copy=True,
        tracking=True,

    )
    project_id = fields.Many2one(
        comodel_name="pmis.project",
        string="Project",

    )

    purchase_project_id = fields.Many2one(
        comodel_name="pmis.purchase.project",
        string="Purchase Project",
        readonly=False,
        copy=True,
        tracking=True,
    )

    price_id = fields.Many2one(
        comodel_name="pmis.products.price",
        string="Products ",
        readonly=False,

    )

    @api.onchange('qty', 'price')
    def _compute_sub_total(self):
        for rec in self:
            if rec.price:
                rec.sub_total = rec.price * rec.qty
            else:
                rec.sub_total = 0.0


class PmisProductsPrice(models.Model):
    _name = "pmis.products.price"
    _description = "Products Price "
    _rec_name = 'price'

    product_description_id = fields.Many2one(
        comodel_name="pmis.products.description",
        string="Products ",
        readonly=False,

    )

    name = fields.Char(
        string='Name',
    )
    unit = fields.Selection([('m', 'Meter'), ('kg', 'Kilo Geram'), ('n', 'Number')], string='Unit', required=True,
                            )
    qty = fields.Integer(string='Quantity')
    description = fields.Char(string='Description')
    price = fields.Float(string='Price', required=True)
    sub_total = fields.Float(string='Sub Total', compute="_compute_sub_total")
    # total = fields.Float(string='Total', compute="_compute_total")

    submission_id = fields.Many2one('pmis.offersubmission', string='Offer')
    purchase_quotation_id = fields.Many2one('pmis.purchase.quotation', string='Quotation')
    purchase_kharidari_id = fields.Many2one('pmis.purchase.kharidari', string='Kharidari')

    # project_id = fields.Many2one(
    #     comodel_name="pmis.project",
    #     related='submission_id.bidding_id.project_id',
    #     string="Project",
    #
    # )
    @api.onchange('qty', 'price')
    def _compute_sub_total(self):
        for rec in self:
            if rec.price:
                rec.sub_total = rec.price * rec.qty

            else:
                rec.sub_total = 0.0

    #
    # @api.onchange('qty', 'price'))
    # def _compute_total(self):
    #     for rec in self:
    #         if rec.price:
    #             rec.total =  rec.total + rec.sub_total
    #         else:
    #             rec.total = 0.0

    class PmisServicesPrice(models.Model):
        _name = "pmis.services.price"
        _description = "Services Price"
        _rec_name = 'name'

        name = fields.Char(string='Section name')
        work_description = fields.Text(string='Description')
        qty = fields.Integer(string='Work Quantity')
        unit_measure = fields.Selection([('m', 'Meter'), ('m3', 'Square meter'), ('ft', 'Foot'), ('m3', 'Cubic meter')],
                                        string='Unit/Measure')
        note = fields.Text(string='Details')
        price = fields.Integer(string='price')
        sub_total = fields.Float(string='Sub Total', compute="_compute_sub_total")

        @api.depends('price', 'qty')
        def _compute_sub_total(self):
            for rec in self:
                rec.sub_total = rec.price * rec.qty

        #
        construction_submission_id = fields.Many2one('pmis.offersubmission', string='Construction Submission')


class PmisProductsTashrih(models.Model):
    _name = "pmis.products.tashrih"
    _description = "Products Tashri "
    _rec_name = 'product_description_id'

    product_description_id = fields.Many2one(
        comodel_name="pmis.products.description",
        string="Products ",
        readonly=False,
    )
    qty = fields.Integer(string='Quantity')

    description = fields.Char(string='Description')
    is_valid = fields.Boolean(string='Is Valid', required=True)
    note = fields.Text(string='Note', )
    purchase_kharidari_id = fields.Many2one('pmis.purchase.kharidari', string='Kharidari')
