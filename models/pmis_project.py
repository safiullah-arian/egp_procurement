# -*- coding: utf-8 -*-
from odoo import api, fields, models, _, tools
from datetime import datetime, date
from odoo.exceptions import ValidationError


class PmisProject(models.Model):
    _name = "pmis.project"
    _description = "Project"
    # _inherit = ['mail.thread', 'mail.activity.mixin', 'ir.attachment']
    _rec_name = 'name'

    project_number = fields.Char(string='Project Number')

    name = fields.Char(string='Project Name')
    name_pa = fields.Char(string=' Name Pashto', )
    name_dr = fields.Char(string='  Name Dari', )
    estimated_cost = fields.Char(string='Estimated Cost', tracking=True)
    date_recieved = fields.Date(string='Date', required=True, default=fields.Date.context_today)
    note = fields.Text(string='Comments')

    budget_code = fields.Selection([('0', '220'), ('1', '222'), ('2', '225')], string='Budget Code')

    category_id = fields.Many2one(
        comodel_name='pmis.procurement.category',
        string="Procurement Type", default=1)

    state = fields.Selection([
        ('draft', 'Draft'),
        ('plan', 'Plan'),
        ('announce', 'Announced'),
        ('received_offers', 'Offer Receiving'),
        ('offer_opening', 'Opening Offers'),
        ('offer_details', 'Offer Details'),
        ('offer_testing', 'Offer Testing'),
        ('offer_evaluation', 'Offer Evaluation'),
        ('winner_announcement', 'Winner Announcement'),
        ('offer_winning', 'Offer Winner'),
        ('won', 'Winner'),
        ('appeal', 'Appeal'),
        ('contract', 'Award'),
        ('delivery', 'Delivery'),
        ('payment', 'Payment'),
        ('cancel', 'Cancel'),
        ('shortlist', 'Shortlist'),
        ('consult_offers_received', 'Offer Receiving'),
        ('consult_offersghoshai', 'Offer Ghoshai'),
        ('consult_evaluation', 'Offer Evaluation'),
        ('consult_interview', 'Interview'),
        ('consult_winners', 'Winners'),
        ('consult_candidate_won', 'Winner Candidates'),
    ],
        string='States', default='draft', required=True)

    # purchase_type = fields.Selection(
    #     [('below20000', '1 < 20000'), ('upto250000', '20000 < 250000'), ('upto500000', '250000 < 500000')],
    #     string='purchase type', default="below20000")
    #
    # purchase_type = fields.Selection(
    #     lambda self: self._get_purchase_type_selection(),
    #     string='purchase_type'
    # )
    #
    # @api.model
    # def _get_purchase_type_selection(self):
    #     if self.env.user.has_group('egp_procurement.pmis_purchase_managers_less_20000'):
    #         return [('below20000', '1 < 20000')]
    #     elif self.env.user.has_group('egp_procurement.pmis_purchase_managers_less_5000000'):
    #         return [('upto250000', '20000 < 250000'), ('upto500000', '250000 < 500000')]
    #     elif self.env.user.has_group('egp_procurement.pmis_head'):
    #         return [('below20000', '1 < 20000'), ('upto250000', '20000 < 250000'), ('upto500000', '250000 < 500000')]
    #     else:
    #         return [('below20000', '1 < 20000'), ('upto250000', '20000 < 250000'), ('upto500000', '250000<500000')]

    documents_ids = fields.One2many(
        comodel_name="pmis.documents",
        string="Documents",
        inverse_name="project_id",
        readonly=False,
        copy=True,
        tracking=True,
    )

    # Products Project
    products_ids = fields.One2many(
        comodel_name="pmis.products.description",
        inverse_name="project_id",
        string="Products",
        readonly=False,
        copy=True,
        tracking=True,

    )

    # consultative services
    hiring_ids = fields.One2many(
        comodel_name="pmis.conultative.hiring",
        inverse_name="project_id",
        string="Hiring",
        readonly=False,
        copy=True,
        tracking=True,
    )
    # Construction services
    section_ids = fields.One2many(
        comodel_name="pmis.construction.section",
        string="Section",
        inverse_name="project_id",
        readonly=False,
        copy=True,
        tracking=True,
    )
    project_plan_id = fields.Many2one(comodel_name='pmis.project.plan', string="Plan")
    directorates_id = fields.Many2one(comodel_name='pmis.directorates', string="Directorate")

    comments = fields.Html(string="Comments")


    @api.model
    def create(self, vals):
        vals['project_number'] = self.env['ir.sequence'].next_by_code('project.sequence')
        return super(PmisProject, self).create(vals)

    # Valiating date of recieving of the project

    # @api.constrains('date_recieved')
    # def check_date_recieved(self):
    #     for rec in self:
    #         if rec.date_recieved and rec.date_recieved > fields.Date.today():
    #             raise ValidationError('Date of Reception can not be greater then today !!')

    def unlink(self):
        for rec in self:
            if rec.state != 'draft':
                raise ValidationError("You can only delete draft projects !!")
        return super(PmisProject, self).unlink()

    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):

        if default is None:
            default = {}
        if not default.get('[project_number]'):
            default['project_number'] = _(" %s (copy)", self.project_number)

        return super(PmisProject, self).copy(default=default)

    # check weather the project has gone to plan

    # @api.ondelete(at_uninstall=False)
    # def check_plan(self):
    #     for rec in self:
    #         if rec.project_plan_id:
    #             raise ValidationError(_('You cant delete this project unless you delete the project from plan.'))



class ProcurementCategory(models.Model):
    _name = "pmis.procurement.category"
    _description = "Procurement Category"
    _rec_name = 'name'

    name = fields.Char(string='Procurement Group', required=True)
    description = fields.Char(string='Description', required=False)


class PmisDirectorates(models.Model):
    _name = "pmis.directorates"
    _description = "PMIS Directorates"
    _rec_name = 'name'

    name = fields.Char(string='Directorate', required=True)


class PmisConsultativeServices(models.Model):
    _name = "pmis.conultative.hiring"
    _description = "Product Consultative service Hiring "

    position_name = fields.Char(string='Position Name', required=True)
    candidiate_experience = fields.Integer(string='Work Experience')

    hiring_type = fields.Selection([('individual', 'Individual'), ('company', 'Company')], string='Hiring Type',
                                   required=True)
    number_employees = fields.Integer(string='Number of Employees', default=1)
    note = fields.Text(string='Note')

    project_id = fields.Many2one(
        comodel_name="pmis.project",
        string="Project",
        readonly=False,
        copy=True,
        tracking=True,
    )


class PmisConstuctionServices(models.Model):
    _name = "pmis.construction.services"
    _description = "Construction service "
    name = fields.Char(string='Section name', related='section_id.name')
    work_description = fields.Text(string='Description', required=True)
    work_amount = fields.Integer(string='Work Amount')
    unit_measure = fields.Selection([('m', 'Meter'), ('m3', 'Square meter'), ('m3', 'Cubic meter')],
                                    string='Unit/Measure', required=True)
    unit_price = fields.Integer(string='Cost/Unit', default=1)
    note = fields.Text(string='Considerations')

    section_id = fields.Many2one(
        comodel_name="pmis.construction.section",
        string="Section",
        readonly=False,
        copy=True,
        tracking=True,
    )
    details_services_id = fields.Many2one('pmis.offersubmission', "Details Services")


class PmisConstructionSection(models.Model):
    _name = "pmis.construction.section"
    _description = "Procurement Category"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'

    name = fields.Char(string='Section Name', required=True)

    services_ids = fields.One2many(
        comodel_name="pmis.construction.services",
        string="Services",
        inverse_name="section_id",
        readonly=False,
        copy=True,
        tracking=True,
    )

    project_id = fields.Many2one(
        comodel_name="pmis.project",
        string="Project",
        readonly=False,
        copy=True,
        tracking=True,
    )
    details_section_id = fields.Many2one('pmis.offersubmission', "Details Section")