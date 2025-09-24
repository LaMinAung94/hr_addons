from odoo import fields, models, _
from odoo.exceptions import UserError, ValidationError

class Branch(models.Model):    
    _name = 'res.branch'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = 'Branch'

    code  = fields.Char(string='Code',tracking=True)
    name  = fields.Char(string='Name',tracking=True)
    company_id  = fields.Many2one('res.company', string='Company',tracking=True)
    analytic_account_id  = fields.Many2one('account.analytic.account', string='Analytic Account',tracking=True)
    ssb_office_no = fields.Char(string='SSB Office No',tracking=True)
    ssb_branch_name = fields.Char(string='SSB Branch Name',tracking=True)
    ssb_office_address = fields.Char(string='SSB Office Address',tracking=True)
    active = fields.Boolean(default=True)

    _sql_constraints = [
        ('code_uniq', 'unique(code)', 'code must be unique!')
    ]

    def toggle_active(self):
        for res in self:
            if self.active:
                department_obj = self.env['hr.department'].search([('branch_id', '=', res.id)])
                emp_obj = self.env['hr.employee'].search([('branch_id', '=', res.id)])
                if department_obj:
                    raise ValidationError(_('Some Department is used %s Branch.') % (res.name))
                if emp_obj:
                    raise ValidationError(_('Some Employee is used %s Branch.') % (res.name))
                if not department_obj and not emp_obj:
                    return super(Branch, self).toggle_active()
            else:
                return super(Branch, self).toggle_active()