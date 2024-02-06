from odoo import models, fields, api


class PmisConstructionDetails(models.Model):
    _name = 'pmis.construction.details'
    _description = 'Pmis Construction Details'

    section = fields.Char(string='Section', readonly=False)
    description = fields.Text(string='Description')
    unit = fields.Char(string='Unit')
    quantity = fields.Float(string='Quantity')
    details = fields.Text(string='Details')
    candidate_project_id = fields.Many2one('pmis.winners.candidates.project', string='Candidate Project')

    section_readonly = fields.Boolean(compute='_compute_section_readonly')

    @api.depends('section')
    def _compute_section_readonly(self):
        for record in self:
            record.section_readonly = bool(record.section)

    @api.onchange('section')
    def onchange_section(self):
        for record in self:
            if record.section:
                record.description = False
                record.unit = False
                record.quantity = False
                record.details = False

    @api.onchange('description', 'unit', 'quantity', 'details')
    def onchange_other_fields(self):
        for record in self:
            if any([record.description, record.unit, record.quantity, record.details]):
                record.section = False





# from odoo import models, fields, api
#
#
# class PmisConstructionDetails(models.Model):
#     _name = 'pmis.construction.details'
#     _description = 'Pmis Construction Details'
#
#     section = fields.Char(string='Section', readonly=False)
#     description = fields.Text(string='Description')
#     unit = fields.Char(string='Unit')
#     quantity = fields.Float(string='Quantity')
#     details = fields.Text(string='Details')
#
#     @api.onchange('section')
#     def onchange_section(self):
#         for record in self:
#             if record.section:
#                 record.description = False
#                 record.unit = False
#                 record.quantity = False
#                 record.details = False
#
#     @api.onchange('description', 'unit', 'quantity', 'details')
#     def onchange_other_fields(self):
#         for record in self:
#             if any([record.description, record.unit, record.quantity, record.details]):
#                 record.section = False
#                 record.section = True
#
#     candidate_project_id = fields.Many2one('pmis.winners.candidates.project', string='Candidate Project')
