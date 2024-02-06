# -- coding: utf-8 --
import dateutil.utils

from odoo import api, fields, models, _, tools
from datetime import datetime,date




class PmisVendors(models.Model):
    _name = "pmis.vendors"
    # _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "PMIS Vendors"
    _rec_name = 'name'

    name = fields.Char(string='Name', required=True)
    street = fields.Char(string='Street')
    city = fields.Char(string='City')
    country_id = fields.Many2one(comodel_name='pmis.country', string='Country',  required=True)
    address = fields.Char(string='Address')
    reg_number = fields.Integer(string='Register Number', required=True)
    license_number = fields.Char(string='License Number', required=True)
    license_start_date = fields.Date(string='License Start Date')
    license_finish_date = fields.Date(string='License Finish Date')
    license_type = fields.Selection([('municipality', 'Municipality'), ('wazarat_kar', 'Ministry of Public Services')],
                                    string='License Type', default='municipality')

    agent_ids = fields.One2many(
        comodel_name="pmis.vendor.agent",
        inverse_name="vendors_id",
        string='Vendor Agents',
        readonly=False,
        copy=True,
        required=True
    )

    documents_ids = fields.One2many(
        comodel_name="pmis.documents",
        inverse_name="vendor_id",
        string="Documents",
        readonly=False,
        copy=True,
    )

    purchase_id = fields.Many2one(
        comodel_name="pmis.purchase",
        string="purchase ",
        readonly=False,
        copy=True,
        tracking=True,
    )
    status = fields.Selection([('valid', 'Valid'), ('invalid', 'Invalid')], string='Status', default='valid')
    selection_status = fields.Selection([('selected', 'Selected'), ('not_selected', 'Not Selected')],
                                        string='Selection Status', default='not_selected')


class VendorTransactions(models.Model):
    _name = "pmis.vendor.transactions"
    _description = "Vendor Transaction"

    experience_years = fields.Integer(string='Number of Years')
    number_of_transactions = fields.Integer(string='Number of Contracts')
    transactions_amount = fields.Integer(string='Total Amount')

    vendors_id = fields.Many2one(
        comodel_name="pmis.vendors",
        string="Vendor",
        readonly=False,
        copy=True,
    )
    transaction_attachment = fields.Binary(string='Attachment')
    basic_evaluation_transaction_id = fields.Many2one(
        comodel_name="basic.evaluation",
        string="Basic Evaluation Transaction",
    )


class VendorExperience(models.Model):
    _name = "pmis.vendor.experience"
    _description = "Vendor Experience"

    project_name = fields.Char(string='Project Name')
    reference_name = fields.Char(string='Reference')
    project_start_date = fields.Date(string='Start Date')
    project_finish_date = fields.Date(string='Finish Date')
    project_amount = fields.Char(string='Project Amount')
    vendors_id = fields.Many2one(
        comodel_name="pmis.vendors",
        string="Vendor ID",
        readonly=False,
        copy=True,
    )
    basic_evaluation_experience_id = fields.Many2one(
        comodel_name="basic.evaluation",
        string="Basic Evaluation Experience",
    )
    experience_attachment = fields.Binary(string='Attachment')


class VendorAssets(models.Model):
    _name = "pmis.vendor.assets"
    _description = "Vendor Assets"

    amount = fields.Integer(string='Amount')
    balance_date = fields.Date(string='Balance Date')
    attachment = fields.Binary(string='Attachment')

    vendors_id = fields.Many2one(
        comodel_name="pmis.vendors",
        string="Vendor",
        readonly=False,
        copy=True,
    )
    bank_id = fields.Many2one(
        comodel_name="pmis.bank",
        string="Bank",
        readonly=False,
        copy=True,
    )
    basic_evaluation_assets_id = fields.Many2one(
        comodel_name="basic.evaluation",
        string="Basic Evaluation Assets",
    )


class PmisBank(models.Model):
    _name = "pmis.bank"
    _description = "Bank"

    name = fields.Char(string='Name', required=True)
    street = fields.Char(string='Street')
    city = fields.Char(string='City')
    country_id = fields.Many2one(comodel_name='pmis.country', string='Country',)
    address = fields.Char(string='Address')

    agent_ids = fields.One2many(
        comodel_name="pmis.vendor.agent",
        inverse_name='bank_id',
        string='Vendor Agent',
        readonly=False,
        copy=True,
    )



class VendorAgent(models.Model):
    _name = "pmis.vendor.agent"
    _description = "Vendor Agent"

    name = fields.Char(string='Name')
    position_title = fields.Char(string='Position')
    phone = fields.Char(string='Phone')
    email = fields.Char(string='Email')
    role = fields.Selection([('purchase_manager', 'Purchase Manager'),
                             ('offer_opening_manager', 'Offer Opening Manager'),
                             ('vednor_direcotr', 'Vendor Director'),
                             ('vendor_agent', 'Vendor Agent'),
                             ], string='Role')
    vendors_id = fields.Many2one(
        comodel_name="pmis.vendors",
        string="Vendor",
        readonly=False,
        copy=True,
    )
    department_id = fields.Many2one(
        comodel_name="pmis.directorates",
        string="Department ID",
        readonly=False,
        copy=True,
    )

    purchase_project_id = fields.Many2one(
        comodel_name="pmis.purchase.project",
        string='Purchase Project',
        readonly=False,
        copy=True,
    )
    bank_id = fields.Many2one(
        comodel_name="pmis.bank",
        string='Bank',
        readonly=False,
        copy=True,
    )

    offer_submission_id = fields.Many2one(
        comodel_name="pmis.offersubmission",
        string='Offer Submission',
        readonly=False,
        copy=True,
    )

    purchase_id = fields.Many2one(
        comodel_name="pmis.purchase.kharidari",
        string='Purchase',
        readonly=False,
        copy=True,
    )
    quotation_id = fields.Many2one(
        comodel_name="pmis.quotation",
        string='Quotation',
        readonly=False,
        copy=True,
    )
    # bidding
    offer_ghoshai_id = fields.Many2one(
        comodel_name="pmis.offerghoshai", string="Offer Ghoshai"
    )
    offer_m_ghoshai_id = fields.Many2one(
        comodel_name="pmis.consultative.offerghoshai.project", string="Offer Ghoshai"
    )
    offer_evaluation_id = fields.Many2one(
        comodel_name="pmis.offers.evaluation", string="Offer Evaluation"
    )
    Agent_id = fields.Many2one(
        comodel_name="basic.evaluation", string="Company Agent"
    )
    delivery_id = fields.Many2one(
        comodel_name="pmis.delivery.description", string="devivery description"
    )
    consultative_offerghoshai_id = fields.Many2one(
        comodel_name="pmis.consultative.offerghoshai", string="Consultative Offer Ghoshai"
    )
    Agent_consult_id = fields.Many2one(
        comodel_name="pmis.consultative.basic.evaluation", string="Vendor Agent"
    )
    consult_panel_id = fields.Many2one(
        comodel_name="pmis.consult.evaluation.project", string="Consult Evaluation Panel"
    )
    consult_interview_id = fields.Many2one(
        comodel_name="pmis.consult.interview.project", string="Consult Evaluation Panel"
    )
    complaint_winner_id = fields.Many2one(
        comodel_name="pmis.bidding.winning.announcement", string="Compliant Board"
    )



class PmisBlockVendor(models.Model):
    _name = "pmis.vendors.block"
    # _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "PMIS Block Vendor"
    _rec_name = 'vendor_id'

    vendor_id = fields.Many2one('pmis.vendors', required=True)
    date = fields.Date(string='Block Date', default=date.today())
    reason = fields.Text(string='Reason')

    @api.model
    def create(self, vals):
        print(vals['vendor_id'])
        self.env['pmis.vendors'].browse(vals['vendor_id']).write({'status': 'invalid'})
        return super(PmisBlockVendor, self).create(vals)

    def write(self, vals):
        return super(PmisBlockVendor, self).write(vals)

    def unlink(self):
        for rec in self:
            self.env['pmis.vendors'].browse(rec.vendor_id.id).write({'status': 'valid'})
        return super(PmisBlockVendor, self).unlink()
