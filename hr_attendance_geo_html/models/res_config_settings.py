# -*- coding: utf-8 -*-

from odoo import fields, models, api


class ResConfigSettingsGeo(models.TransientModel):
    _inherit = 'res.config.settings'

    geo_html_access = fields.Boolean(string='Enable ip access', help="Check in/out user only when ip-address found in IP table")

    # @api.multi
    def set_values(self):
        res = super(ResConfigSettingsGeo, self).set_values()
        config_parameters = self.env['ir.config_parameter'].sudo()
        config_parameters.set_param('hr_attendance_geo_access', self.geo_html_access)
        return res

    @api.model
    def get_values(self):
        res = super(ResConfigSettingsGeo, self).get_values()
        res.update(geo_html_access = self.env['ir.config_parameter'].sudo().get_param('hr_attendance_geo_access'))
        return res
