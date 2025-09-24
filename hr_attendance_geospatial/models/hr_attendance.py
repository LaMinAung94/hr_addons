# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class HrAttendance(models.Model):
    _inherit = "hr.attendance"

    geospatial_check_in_id = fields.Many2one('hr.attendance.geospatial', string="Location geospatial found in", readonly=True)
    geospatial_check_out_id = fields.Many2one('hr.attendance.geospatial', string="Location geospatial found out", readonly=True)
    geospatial_access_check_in = fields.Html(string="Geospatial in", readonly=True)
    geospatial_access_check_out = fields.Html(string="Geospatial out", readonly=True)


class HrAttendanceGEO(models.Model):
    _name = "hr.attendance.geospatial"

    name = fields.Char(string="Name of location")
    description = fields.Char(string="Description of location, display on checkin interface")
    company_id = fields.Many2one('res.company', "Company", required=True)
    # employee_ids = fields.Many2many('hr.employee', string="Only for employees", domain="[('mobile_app_attendance','=',1)]")
    employee_ids = fields.Many2many('hr.employee', string="Only for employees",)
    the_geom2 = fields.GeoPolygon('NPA Shape')

            
    