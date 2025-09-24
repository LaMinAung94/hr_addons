# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _


class HrEmployee(models.AbstractModel):
    _inherit = "hr.employee.base"

    def parse_param(self, vals, mode='in'):
        if self._context.get('ismobile', None):
            vals.update({'ismobile_check_' + mode: self._context.get('ismobile', None)})
        if self._context.get('geospatial_id', None):
            vals.update({'geospatial_check_' + mode + '_id': self._context.get('geospatial_id', None)})
        if self._context.get('ip_id', None):
            vals.update({'ip_check_' + mode + '_id': self._context.get('ip_id', None)})
        if self._context.get('ip', None):
            vals.update({'ip_check_' + mode: self._context.get('ip', None)})
        if self._context.get('geo', None):
            vals.update({'geo_check_' + mode: self._context.get('geo', None)})
        if self._context.get('token', None):
            vals.update({'token_check_' + mode + '_id': self._context.get('token', None)})
        if self._context.get('webcam', None):
            vals.update({'webcam_check_' + mode: self._context.get('webcam', None)})
        if self._context.get('user_agent_html', None):
            vals.update({'user_agent_html_check_' + mode: self._context.get('user_agent_html', None)})
        if self._context.get('face_recognition_image', None):
            vals.update({'face_recognition_image_check_' + mode: self._context.get('face_recognition_image', None)})
        if self._context.get('kiosk_shop_id', None):
            vals.update({'kiosk_shop_id_check_' + mode: self._context.get('kiosk_shop_id', None)})

        access_allowed = self._context.get('access_allowed', None)
        access_denied = self._context.get('access_denied', None)
        access_allowed_disable = self._context.get('access_allowed_disable', None)
        access_denied_disable = self._context.get('access_denied_disable', None)
        accesses = self._context.get('accesses', None)
        if accesses:
            for key, value in accesses.items():
                if value.get('enable', False):
                    if value.get('access', False):
                        vals.update({key + '_check_' + mode: access_allowed})
                    else:
                        vals.update({key + '_check_' + mode: access_denied})
                else:
                    if value.get('access', False):
                        vals.update({key + '_check_' + mode: access_allowed_disable})
                    else:
                        vals.update({key + '_check_' + mode: access_denied_disable})

    def _attendance_action_change(self):
        """ Check In/Check Out action
            Check In: create a new attendance record
            Check Out: modify check_out field of appropriate attendance record
        """
        self.ensure_one()
        action_date = fields.Datetime.now()

        if self.attendance_state != 'checked_in':
            vals = {
                'employee_id': self.id,
                'check_in': action_date,
            }
            self.parse_param(vals)
            return self.env['hr.attendance'].create(vals)
        attendance = self.env['hr.attendance'].search([('employee_id', '=', self.id), ('check_out', '=', False)], limit=1)
        if attendance:
            vals = {
                    'check_out': action_date,
                }
            self.parse_param(vals, 'out')
            attendance.write(vals)
        else:
            raise exceptions.UserError(_('Cannot perform check out on %(empl_name)s, could not find corresponding check in. '
                'Your attendances have probably been modified manually by human resources.') % {'empl_name': self.sudo().name, })
        return attendance
