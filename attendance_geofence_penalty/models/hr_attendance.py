# models/hr_attendance.py

from odoo import models, fields, api, _

class HrAttendance(models.Model):
    _inherit = 'hr.attendance'

    geo_status = fields.Selection([
        ('in_office', 'In Office'),
        ('out_of_office', 'Out of Office')
    ], string='Geo Status', default='in_office')

    late_minutes = fields.Integer(string='Late Minutes', compute='_compute_late_minutes', store=True)

    @api.depends('check_in')
    def _compute_late_minutes(self):
        for rec in self:
            rec.late_minutes = 0
            if rec.check_in:
                try:
                    check_in_dt = fields.Datetime.from_string(rec.check_in)
                    office_start = check_in_dt.replace(hour=9, minute=0, second=0, microsecond=0)
                    if check_in_dt > office_start:
                        delta = check_in_dt - office_start
                        rec.late_minutes = int(delta.total_seconds() / 60)
                except Exception:
                    rec.late_minutes = 0
