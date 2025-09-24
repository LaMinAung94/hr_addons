# -*- coding: utf-8 -*-

from odoo import http
from pyproj import Proj
from pyproj import Proj, transform

from odoo.http import request
from shapely.geometry import Point

from odoo.addons.hr_attendance_base.controllers.controllers import HrAttendanceBase


class HrAttendanceGeospatial(HrAttendanceBase):
    @http.route('/hr_attendance_base', auth='user', type="json")
    def index(self, **kw):
        res = super(HrAttendanceGeospatial, self).index(**kw)
        geospatial_access_enable = request.env['ir.config_parameter'].sudo().get_param(str(request.env.user.company_id.id)+'hr_attendance_geospatial_access')
        res.update({'geospatial_enable': True if geospatial_access_enable else False})
        if kw.get('latitude') and kw.get('longitude'):
            P3857 = Proj(init='epsg:3857')
            P4326 = Proj(init='epsg:4326')
            x,y = transform(P4326, P3857, kw.get('longitude'), kw.get('latitude'))
            point3 = Point(x, y)
            the_geom_ids = []
            for i in request.env['hr.attendance.geospatial'].sudo().search([('company_id', '=', request.env.user.company_id.id)]):
                if i.employee_ids:
                    users = i.employee_ids.mapped('user_id')
                    if  request.env.user in users:
                        if point3.within(i.the_geom2) or i.the_geom2.contains(point3):
                            the_geom_ids = i
                            break
                else:
                    if point3.within(i.the_geom2) or i.the_geom2.contains(point3):
                        the_geom_ids = i
                        break
            res.update({'geospatial_access': True if the_geom_ids else False})
            if the_geom_ids:
                res.update({'geospatial_description': the_geom_ids.description if the_geom_ids else False})
                res.update({'geospatial_name': the_geom_ids.name if the_geom_ids else False})
                res.update({'geospatial_id': the_geom_ids.id if the_geom_ids else False})
        return res
