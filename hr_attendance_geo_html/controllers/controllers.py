# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request

from odoo.addons.hr_attendance_base.controllers.controllers import HrAttendanceBase

class HrAttendanceGeoHtml(HrAttendanceBase):
    @http.route('/hr_attendance_base', auth='user', type="json")
    def index(self, **kw):
        res = super(HrAttendanceGeoHtml, self).index(**kw)
        geo_access_enable = request.env['ir.config_parameter'].sudo().get_param('hr_attendance_geo_access')
        res.update({'geo_enable': True if geo_access_enable else False})
        return res
