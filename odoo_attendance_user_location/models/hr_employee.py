# -*- coding: utf-8 -*-
################################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2023-TODAY Cybrosys Technologies(<https://www.cybrosys.com>).
#    Author: Sreenath K, Shafna K (odoo@cybrosys.com)
#
#    You can modify it under the terms of the GNU AFFERO
#    GENERAL PUBLIC LICENSE (AGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU AFFERO GENERAL PUBLIC LICENSE (AGPL v3) for more details.
#
#    You should have received a copy of the GNU AFFERO GENERAL PUBLIC LICENSE
#    (AGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
from geopy.geocoders import Nominatim
from odoo import exceptions, fields, models, _
from odoo import models, fields, exceptions, _
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError

class HrEmployee(models.AbstractModel):
    """Inherits HR Employee model"""
    _inherit = 'hr.employee'

    def attendance_manual(self, next_action, entered_pin=None):
        """
        Override attendance_manual to capture geolocation data
        passed via context (latitude, longitude).
        """
        self.ensure_one()

        latitude = self.env.context.get('latitude')
        longitude = self.env.context.get('longitude')

        # Determine whether the user can check in/out without a PIN
        has_attendance_rights = self.user_has_groups(
            'hr_attendance.group_hr_attendance_user,'
            '!hr_attendance.group_hr_attendance_use_pin'
        )

        can_check_without_pin = (
            has_attendance_rights or
            (self.user_id == self.env.user and entered_pin is None)
        )

        # Check-in/out logic
        if can_check_without_pin or (entered_pin and entered_pin == self.sudo().pin):
            return self._attendance_action(latitude, longitude, next_action)

        # Error: PIN required but missing or incorrect
        if not self.user_has_groups('hr_attendance.group_hr_attendance_user'):
            return {
                'warning': _(
                    'To activate Kiosk mode without pin code, you must have '
                    'access rights as an Officer or above in the Attendance app. '
                    'Please contact your administrator.'
                )
            }

        return {'warning': _('Wrong PIN')}

    def _attendance_action(self, latitudes, longitudes, next_action):
        """ Changes the attendance of the employee.
            Returns an action to the check in/out message,
            next_action defines which menu the check in/out message should
            return to. ("My Attendances" or "Kiosk Mode")
        """
        self.ensure_one()
        employee = self.sudo()
        action_message = self.env['ir.actions.actions']._for_xml_id('hr_attendance.'
                                                                    'hr_attendance_action_greeting_message')

        action_message['previous_attendance_change_date'] = employee.last_attendance_id and (
                employee.last_attendance_id.check_out
                or employee.last_attendance_id.check_in) or False
        action_message['employee_name'] = employee.name
        action_message['barcode'] = employee.barcode
        action_message['next_action'] = next_action
        action_message['hours_today'] = employee.hours_today
        action_message['kiosk_delay'] = \
            employee.company_id.attendance_kiosk_delay * 1000

        if employee.user_id:
            modified_attendance = employee.with_user(employee.user_id).sudo()._attendance_action_change(longitudes,
                                                                                                        latitudes)
        else:
            modified_attendance = employee._attendance_action_change(longitudes,
                                                                     latitudes)
        action_message['attendance'] = modified_attendance.read()[0]
        action_message['total_overtime'] = employee.total_overtime

        # Overtime have a unique constraint on the day, no need for limit=1

        action_message['overtime_today'] = \
            self.env['hr.attendance.overtime'].sudo().search([('employee_id', '=', employee.id),
                                                              ('date', '=', fields.Date.context_today(self)),
                                                              ('adjustment', '=', False)]).duration or 0
        return {'action': action_message}

    def _attendance_action_change(self, geoip_data=None, latitude=None, longitude=None):
        """
        Perform check-in/check-out with GPS data.
        Handles both original Odoo calls and custom GPS functionality.
        """
        self.ensure_one()
        action_date = fields.Datetime.now()

        # Handle different calling patterns
        if geoip_data and latitude is None and longitude is None:
            # Original Odoo call pattern - use geoip data
            if hasattr(geoip_data, 'get'):
                # It's a dict-like object with location data
                latitude = geoip_data.get('latitude')
                longitude = geoip_data.get('longitude')
            else:
                # Fallback to original behavior without GPS
                return self._original_attendance_action_change(geoip_data)

        # Your existing GPS logic continues here...
        geolocator = Nominatim(user_agent='odoo-attendance-location')
        address = "Unknown location"

        if latitude and longitude:
            try:
                location = geolocator.reverse(f"{latitude}, {longitude}", timeout=10)
                if location:
                    address = location.address
            except (GeocoderTimedOut, GeocoderServiceError, Exception):
                address = "Reverse geolocation failed"

            map_link = f"https://www.google.com/maps/search/?api=1&query={latitude},{longitude}"
        else:
            address = "Location not available"
            map_link = None

        if self.attendance_state != 'checked_in':
            # CHECK IN
            vals = {
                'employee_id': self.id,
                'checkin_address': address,
                'checkin_latitude': latitude,
                'checkin_longitude': longitude,
                'checkin_location': map_link,
                'check_in': action_date,
            }
            return self.env['hr.attendance'].create(vals)

        # CHECK OUT
        attendance = self.env['hr.attendance'].search([
            ('employee_id', '=', self.id),
            ('check_out', '=', False)
        ], limit=1)

        if attendance:
            attendance.write({
                'checkout_address': address,
                'checkout_latitude': latitude,
                'checkout_longitude': longitude,
                'checkout_location': map_link,
                'check_out': action_date,
            })
            return attendance

        raise exceptions.UserError(_(
            "Cannot perform check-out for %(name)s — no open check-in found. "
            "Your attendances may have been modified manually by HR."
        ) % {'name': self.name})

    def _original_attendance_action_change(self, geoip_data):
        """Fallback to original Odoo attendance action without GPS"""
        if self.attendance_state != 'checked_in':
            return self.env['hr.attendance'].create({
                'employee_id': self.id,
                'check_in': fields.Datetime.now(),
            })
        else:
            attendance = self.env['hr.attendance'].search([
                ('employee_id', '=', self.id),
                ('check_out', '=', False)
            ], limit=1)
            if attendance:
                attendance.write({'check_out': fields.Datetime.now()})
                return attendance
            raise exceptions.UserError(_("Cannot perform check-out, no check-in found."))
