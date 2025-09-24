# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class HrAttendance(models.Model):
    _inherit = "hr.attendance"

    employee_id_image = fields.Image(string="Image employee", related='employee_id.image_1920')
    ismobile_check_in = fields.Boolean(string="Mobile device check in?")
    ismobile_check_out = fields.Boolean(string="Mobile device check out?")
