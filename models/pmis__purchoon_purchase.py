# -*- coding: utf-8 -*-
from odoo import api, fields, models, _, tools
from datetime import datetime, date

from odoo.exceptions import ValidationError


class PmisPurchaseProject(models.Model):
    _name = "pmis.purchase.project"
    _description = "Purchase Project"
    _rec_name = 'request_explanation'

    purchase_type = fields.Selection(
        [('below20000', '1 < 20000'), ('upto250000', '20000 < 250000'), ('upto500000', '250000 < 500000')],
        string='purchase type', default="below20000")

    category_id = fields.Many2one(
        comodel_name='pmis.procurement.category',
        string="Procurement Type", default=1)

    requested_by = fields.Many2one(comodel_name='pmis.directorates', string="Requested By")
    request_explanation = fields.Text(string="Request Explanation")
    application_number = fields.Integer(string="Application Number", default='')
    application_date = fields.Date(string="Application Date")

    maqam_hukm_number = fields.Integer(string="Maqam Hukm Number", default='')
    maqam_hukm_date = fields.Date(string="Maqam Hukm Date")
    currency_id = fields.Selection([('afg', 'Afg'), ('usd-dollar', 'USD')], string='Currency')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('quotation', 'Quotation'),
        ('compare', 'Comparision'),
        ('complete', 'Completed'),
        ('cancel', 'Cancel')
    ], string='State', default='draft')

    documents_ids = fields.One2many(
        comodel_name="pmis.documents",
        inverse_name="purchase_project_id",
        string="Documents",
        readonly=False,
        copy=True,
    )
    product_ids = fields.One2many(
        comodel_name="pmis.products.description",
        inverse_name="purchase_project_id",
        string="Products",
        readonly=False,
        copy=True,

    )

    agent_ids = fields.One2many(
        comodel_name="pmis.vendor.agent",
        inverse_name='purchase_project_id',
        string='Vendor Agent',
        readonly=False,
        copy=True,
    )

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

    def unlink(self):
        for rec in self:
            if self.env['pmis.purchase.project'].browse(rec.id).state != 'draft':
                raise ValidationError(_('You are just allowed to delete draft project'))

        return super(PmisPurchaseProject, self).unlink()


class PmisPurchaseQuotationLine(models.Model):
    _name = "pmis.purchase.quotation"
    _description = "Purchases Quotation"
    _rec_name = 'vendor_id'

    vendor_id = fields.Many2one(string="Vendor", comodel_name='pmis.vendors', required=True,
                                domain=[('status', '=', 'valid')])
    purchase_project_id = fields.Many2one(string="Purchase", related='quotation_id.purchase_project_id')
    product_price_ids = fields.One2many(
        comodel_name='pmis.products.price',
        inverse_name='purchase_quotation_id',
        string='Price',
        required=True
    )
    quotation_amount = fields.Float(string='Quotation Amount')
    quotation_id = fields.Many2one(string="Quotation", comodel_name='pmis.quotation')

    documents_ids = fields.One2many(
        comodel_name="pmis.documents",
        inverse_name="purchase_quotation_line_id",
        string="Documents",
        readonly=False,
        copy=True,
    )

    @api.onchange('product_price_ids')
    def _compute_quotation_total(self):
        self.quotation_amount = 0.0
        for rec in self.product_price_ids:
            self.quotation_amount = self.quotation_amount + rec.sub_total

    @api.onchange('purchase_project_id')
    def onchange_purchase_project_id(self):
        for rec in self:
            product_lines = [(5, 0, 0)]
            for product in self.purchase_project_id.product_ids:
                vals = {
                    'product_description_id': product.id,
                    'name': product.product_id.name,
                    'unit': product.product_id.unit,
                    'description': product.description,
                    'qty': product.qty
                }
                product_lines.append((0, 0, vals))
            self.product_price_ids = product_lines

    @api.model
    def create(self, vals):
        return super(PmisPurchaseQuotationLine, self).create(vals)

    def write(self, vals):
        return super(PmisPurchaseQuotationLine, self).write(vals)

    def unlink(self):
        return super(PmisPurchaseQuotationLine, self).unlink()


class PmisPurchaseQuotation(models.Model):
    _name = "pmis.quotation"
    _description = "Purchases Quotation"
    _rec_name = 'purchase_project_id'

    purchase_project_id = fields.Many2one(
        string="Purchase Project",
        comodel_name='pmis.purchase.project',
        required=True,
        domain=[('state', '=', 'draft'), ('purchase_type', 'in', ('upto250000', 'upto500000'))]
    )

    quotation_lines = fields.One2many(
        string="Quotation Lines",
        comodel_name='pmis.purchase.quotation',
        inverse_name='quotation_id'
    )
    cheap_quotation_amount = fields.Float(string='Cheap Quotation Amount', compute="_compute_less_price")
    cheap_quotation_index = fields.Integer(string='Index')
    cheap_quotation_id = fields.Integer(string='Cheap Quotation')
    cheap_quotation_vendor_id = fields.Many2one('pmis.vendors', string='Vendor')

    documents_ids = fields.One2many(
        comodel_name="pmis.documents",
        inverse_name="purchase_quotation_id",
        string="Documents",
        readonly=False,
        copy=True,
    )
    agent_ids = fields.One2many(
        comodel_name="pmis.vendor.agent",
        inverse_name='quotation_id',
        string='Vendor Agent',
        readonly=False,
        copy=True,
    )

    #
    @api.onchange('quotation_lines')
    def _compute_less_price(self):
        if self.quotation_lines:
            first_record_total = self.quotation_lines[0].quotation_amount
        else:
            first_record_total = 0
        rec_index = ''
        for index, rec in enumerate(self.quotation_lines):
            if rec.quotation_amount <= first_record_total:
                self.cheap_quotation_id = rec.id
                rec_index = index
                self.cheap_quotation_vendor_id = rec.vendor_id
                first_record_total = rec.quotation_amount
        self.cheap_quotation_amount = first_record_total
        self.cheap_quotation_index = rec_index

    @api.model
    def create(self, vals):
        self.env['pmis.purchase.project'].browse(vals['purchase_project_id']).write({'state': 'quotation'})

        return super(PmisPurchaseQuotation, self).create(vals)

    def unlink(self):
        for rec in self.purchase_project_id:
            if self.env['pmis.purchase.project'].browse(rec.id).state == 'complete':
                raise ValidationError('You are not allowed to delete completed project')
            else:
                self.env['pmis.purchase.project'].browse(rec.id).write({'state': 'draft'})
        return super(PmisPurchaseQuotation, self).unlink()


class PmisPurchasKharidari(models.Model):
    _name = "pmis.purchase.kharidari"
    _description = "Purchases Kharidari"
    _rec_name = 'quotation_project_id'

    quotation_project_id = fields.Many2one('pmis.quotation', string='Quoted Project',
                                           domain=[('purchase_project_id.state', '=', 'quotation')])

    purchase_project_type = fields.Selection(
        [('below20000', '1 < 20000'), ('upto250000', '20000 < 250000'), ('upto500000', '250000 < 500000')],
        string='Project Type', default="below20000")

    purchase_project_type = fields.Selection(
        lambda self: self._get_purchase_project_type_selection(),
        string='purchase_type'
    )

    @api.model
    def _get_purchase_project_type_selection(self):
        if self.env.user.has_group('egp_procurement.pmis_purchase_managers_less_20000'):
            return [('below20000', '1 < 20000')]
        elif self.env.user.has_group('egp_procurement.pmis_purchase_managers_less_5000000'):
            return [('upto250000', '20000 < 250000'), ('upto500000', '250000 < 500000')]
        elif self.env.user.has_group('egp_procurement.pmis_head'):
            return [('below20000', '1 < 20000'), ('upto250000', '20000 < 250000'), ('upto500000', '250000 < 500000')]
        else:
            return [('below20000', '1 < 20000'), ('upto250000', '20000 < 250000'), ('upto500000', '250000<500000')]

    purchas_project_20000 = fields.Many2one('pmis.purchase.project', string='Project',
                                            domain=[('state', '=', 'draft'), ('purchase_type', '=', 'below20000')]
                                            )
    purchas_project_20000_index = fields.Integer(string='Purchase Project 20000 Number')
    purchas_project_m3_number = fields.Integer(string='M3 Number')
    purchas_project_m2_number = fields.Integer(string='M2 Number')

    # @api.multi
    def get_project_type_label(self):
        label_mapping = {
            'below20000': '1 < 20000',
            'upto250000': '20000 < 250000',
            'upto500000': '250000 < 500000'
        }
        return label_mapping.get(self.purchase_project_type, '')

    @api.onchange('purchas_project_20000')
    def onchange_purchas_project_20000(self):
        self.purchas_project_20000_index = self.purchas_project_20000.id

    quotation_id = fields.Integer(related='quotation_project_id.cheap_quotation_id', string='Cheap Quotation',
                                  readonly=False)
    vendor_id = fields.Many2one('pmis.vendors',
                                related='quotation_project_id.cheap_quotation_vendor_id',
                                string='Vendor <500000')
    purchase_vendor_id = fields.Many2one('pmis.vendors',
                                         string='Purchase Vendor < 20000')
    purchase_project_id = fields.Integer(related='quotation_project_id.purchase_project_id.id',
                                         string='Purchase Project', readonly=False)
    invoice_number = fields.Char(string='Invoice Number')
    date = fields.Date(string='Purchase Date')
    product_price_ids = fields.One2many(
        comodel_name='pmis.products.price',
        inverse_name='purchase_kharidari_id',
        readonly=False,
        copy=True,
        store=True
    )
    purchase_amount = fields.Float(string='Purchase Amount')

    documents_ids = fields.One2many(
        comodel_name="pmis.documents",
        inverse_name="purchase_id",
        string="Documents",
        readonly=False,
        copy=True,
    )
    purchase_payment_type = fields.Selection(
        [('purchase_payment_cash', 'Cash Payment'), ('purchase_payment_bank', 'Bank Payment'),
         ('purchase_payment_advance', 'Advance Payment')],
        string='Payment Type', default="purchase_payment_cash")

    def get_purchase_payment_type_label(self):
        label_mapping = {
            'purchase_payment_cash': 'Cash Payment',
            'purchase_payment_bank': 'Bank Payment',
            'purchase_payment_advance': 'Advance Payment'
        }
        return label_mapping.get(self.purchase_payment_type, '')

    purchase_payment_cash = fields.Many2one('pmis.cash.reception', string="Cash Payment")
    purchase_payment_cash_id = fields.Integer(string="Cash Payment")

    @api.onchange('purchase_payment_cash')
    def onchange_purchase_payment_cash(self):
        self.purchase_payment_cash_id = self.purchase_payment_cash.id

    agent_ids = fields.One2many(
        comodel_name="pmis.vendor.agent",
        inverse_name='purchase_id',
        string='Vendor Agent',
        readonly=False,
        copy=True,
    )

    @api.onchange('quotation_project_id', 'purchas_project_20000')
    def onchange_purchase_id(self):
        for rec in self:
            product_lines = [(5, 0, 0)]
            if self.quotation_project_id:
                for product in self.quotation_project_id.purchase_project_id.product_ids:
                    vals = {
                        'product_description_id': product.id,
                        'name': product.product_id.name,
                        'unit': product.product_id.unit,
                        'description': product.description,
                        'qty': product.qty
                    }
                    product_lines.append((0, 0, vals))
            else:
                for product in self.purchas_project_20000.product_ids:
                    vals = {
                        'product_description_id': product.id,
                        'name': product.product_id.name,
                        'unit': product.product_id.unit,
                        'description': product.description,
                        'qty': product.qty
                    }
                    product_lines.append((0, 0, vals))

            self.product_price_ids = product_lines

    @api.onchange('product_price_ids')
    def _compute_quotation_total(self):
        self.purchase_amount = 0.0
        for rec in self.product_price_ids:
            self.purchase_amount = self.purchase_amount + rec.sub_total

    product_tashrih_ids = fields.One2many(
        comodel_name='pmis.products.tashrih',
        inverse_name='purchase_kharidari_id',
    )

    # tashrih products
    @api.onchange('quotation_project_id', 'purchas_project_20000')
    def onchange_project_id(self):
        for rec in self:
            product_lines = [(5, 0, 0)]
            if self.quotation_project_id:
                for product in self.quotation_project_id.purchase_project_id.product_ids:
                    vals = {
                        'product_description_id': product.id,
                        'description': product.description,
                        'qty': product.qty
                    }
                    product_lines.append((0, 0, vals))
            else:
                for product in self.purchas_project_20000.product_ids:
                    vals = {
                        'product_description_id': product.id,
                        'description': product.description,
                        'qty': product.qty
                    }
                    product_lines.append((0, 0, vals))

            self.product_tashrih_ids = product_lines

    #
    @api.model
    def create(self, vals):

        print(vals['purchase_payment_cash_id'])
        if vals['purchase_payment_type'] == 'purchase_payment_cash':

            cash_available = self.env['pmis.cash.reception'].browse(vals['purchase_payment_cash_id']).remaining_cash
            print('cash', cash_available)
            print('py', vals['purchase_amount'])
            if cash_available >=  vals['purchase_amount']:
                self.env['pmis.cash.reception'].browse(vals['purchase_payment_cash_id']).expenses += vals[
                    'purchase_amount']
            else:
                raise ValidationError(
                    "Sorry, you don't have enough cash to complete this transaction available balance !!! Available balance: %f" % cash_available)

        if vals['quotation_project_id'] != False:
            quotation_price = self.env['pmis.purchase.quotation'].browse(vals['quotation_id']).quotation_amount
            if vals['purchase_amount'] > quotation_price:
                raise ValidationError('Purchase Price can not be greater then Quotation price')
            else:
                self.env['pmis.purchase.project'].browse(vals['purchase_project_id']).write({'state': 'complete'})
        else:
            self.env['pmis.purchase.project'].browse(vals['purchas_project_20000_index']).write({'state': 'complete'})
        return super(PmisPurchasKharidari, self).create(vals)

    def write(self, vals):

        if self.purchase_payment_type == 'purchase_payment_cash':
            cash_available = self.env['pmis.cash.reception'].browse(self.purchase_payment_cash_id).remaining_cash
            if cash_available >= vals['purchase_amount']:
                self.env['pmis.cash.reception'].browse(self.purchase_payment_cash_id).expenses += vals[
                    'purchase_amount']
            else:
                raise ValidationError("Sorry, you don't have enough cash to complete this transaction !!!")

        if self.quotation_project_id != False:
            quotation_price = self.env['pmis.purchase.quotation'].browse(self.quotation_id).quotation_amount
            if vals['purchase_amount'] > quotation_price:
                raise ValidationError('Purchase Price can not be greater then Quotation price')
            else:
                self.env['pmis.purchase.project'].browse(self.purchase_project_id).write({'state': 'complete'})
        else:
            self.env['pmis.purchase.project'].browse(self.purchas_project_20000_index).write({'state': 'complete'})

        return super(PmisPurchasKharidari, self).write(vals)

    def unlink(self):
        for rec in self:
            if rec.quotation_project_id:
                print('yes')
                self.env['pmis.purchase.project'].browse(rec.purchase_project_id).write({'state': 'quotation'})
            else:
                print('id', rec.purchas_project_20000_index)
                self.env['pmis.purchase.project'].browse(rec.purchas_project_20000_index).write({'state': 'draft'})

        return super(PmisPurchasKharidari, self).unlink()
