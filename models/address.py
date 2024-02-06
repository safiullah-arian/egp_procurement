from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import datetime, date


class PmisCountry(models.Model):
    _name = "pmis.country"
    _description = "PMIS Country"

    name = fields.Char(string='Name')
    province_ids = fields.One2many('pmis.country.province', 'country_id' )


class PmisProvicnes(models.Model):
    _name = "pmis.country.province"
    _description = "PMIS Province"

    name = fields.Char(string='Name')
    country_id = fields.Many2one('pmis.country',string='Country ')
    district_ids = fields.One2many('pmis.districts', 'province_id' , string='Districts')



class PmisDistricts(models.Model):
    _name = "pmis.districts"
    _description = "PMIS Districts"

    name = fields.Char(string='Name')
    province_id = fields.Many2one('pmis.country.province', string='Province ')