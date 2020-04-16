from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
class EmployeeJoining(models.Model):
    _name = 'earn.leave.assign'
    _description = 'Annual Leave assign days'
    _rec_name = "earn_leave_days"
    _order = "id desc"

    earn_leave_days = fields.Integer(string="Assign Earn Leave Days")


    @api.model
    def create(self, values):
        user_count = self.env['earn.leave.assign'].search_count([])
        if user_count<1:
            return super(EmployeeJoining, self).create(values)
        else:
            raise ValidationError('You can\'t create another days, days are already created, please edit days as your '
                                  'requirements.')
