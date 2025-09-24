# -*- coding: utf-8 -*-

from odoo import fields, models, api


class ResConfigSettingsGeospatial(models.TransientModel):
    _inherit = 'res.config.settings'

    geospatial_access = fields.Boolean(string='Enable geospatial access', help="Check in/out user only when employee in geo table polygon")

    def set_values(self):
        res = super(ResConfigSettingsGeospatial, self).set_values()
        config_parameters = self.env['ir.config_parameter']
        config_parameters.set_param(str(self.env.user.company_id.id)+"hr_attendance_geospatial_access", self.geospatial_access)
        return res

    @api.model
    def get_values(self):
        res = super(ResConfigSettingsGeospatial, self).get_values()
        res.update(geospatial_access = self.env['ir.config_parameter'].get_param(str(self.env.user.company_id.id)+'hr_attendance_geospatial_access'))
        return res
