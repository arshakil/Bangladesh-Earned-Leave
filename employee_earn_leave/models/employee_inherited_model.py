from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import date, datetime


class EmployeeInheitedModel(models.Model):
    _inherit = 'hr.employee'

    joining_date = fields.Date(string="Joining Date",)
    count_earn_days = fields.Integer(string="Annual Days", compute='get_earn_days')

    # @api.depends('joining_date')
    def get_earn_days(self):
        self.employeeEarnLeaveCalculation()


    @api.multi
    def write(self, vals):
        res = super(EmployeeInheitedModel, self).write(vals)
        if vals.get('joining_date'):
            self.employeeEarnLeaveCalculation()
        else:
            holiday_status_id = self.env['hr.holidays.status'].search([('name', '=', 'Earn Leaves')], limit=0)

            check_earn_leave = self.env['hr.holidays'].search(
                [("employee_id", "=", self.id), ("holiday_status_id.id", "=", holiday_status_id.id),
                 ('type', '=', 'add')])
            if check_earn_leave:
                for val in check_earn_leave:
                    self.env['hr.holidays'].browse(val.id).write({
                        'id': val.id,
                        'number_of_days_temp': 0,
                        'number_of_days': 0
                    })
        return res

# calculating
    def employeeEarnLeaveCalculation(self):
        employee_id = self.env['hr.employee'].search([('id', '=', self.id)])

        if employee_id.joining_date:
            # checking leave assign days
            check_earn_assign_days = self.env['earn.leave.assign'].search([])
            assign_days = check_earn_assign_days.earn_leave_days

            # checking earn leave id
            holiday_status_id = self.env['hr.holidays.status'].search([('name', '=', 'Earn Leaves')], limit=0)

            # checking earn leave exist or not
            check_earn_leave = self.env['hr.holidays'].search(
                [("employee_id", "=", employee_id.id), ("holiday_status_id.id", "=", holiday_status_id.id),
                 ('type', '=', 'add')])

            # calculating earn leave according to joining date of employee
            employee_joining_date = datetime.strptime(employee_id.joining_date, "%Y-%m-%d").date()
            today = datetime.now().date()
            total_days = (today - employee_joining_date).days
            if total_days < 1:
                raise ValidationError(
                    "You can\'t select advanced date, since you selected: %s" % abs(total_days) + " days Advance")
            else:
                earn_leave = total_days / assign_days
                # earn_leave_days = total_days/18
                self.count_earn_days = earn_leave

                if check_earn_leave:
                    for val in check_earn_leave:
                        if earn_leave > val.number_of_days_temp:
                            #
                            self.env['hr.holidays'].browse(val.id).write({
                                'id': val.id,
                                'number_of_days_temp': earn_leave,
                                'number_of_days': earn_leave
                            })
                        else:
                            self.env['hr.holidays'].browse(val.id).write({
                                'id': val.id,
                                'number_of_days_temp': earn_leave,
                                'number_of_days': earn_leave
                            })
                else:
                    holiday_status_id = holiday_status_id.id
                    employee_id = employee_id.id
                    holiday_type = "employee"
                    number_of_days_temp = earn_leave
                    state = "validate"
                    manager_id = 1
                    type = "add"
                    department_id = self.department_id.id
                    number_of_days = earn_leave

                    # current user
                    context = self._context
                    current_uid = context.get('uid')
                    user_id = self.env['res.users'].browse(current_uid).id

                    create_earn_leave = self.env['hr.holidays'].browse(self.env.context.get('active_ids', []))
                    create_earn_leave.create({'holiday_status_id': holiday_status_id,
                                              'employee_id': employee_id,
                                              'holiday_type': holiday_type,
                                              'number_of_days_temp': number_of_days_temp,
                                              'state': state,
                                              'manager_id': manager_id,
                                              'type': type,
                                              'department_id': department_id,
                                              'number_of_days': number_of_days,
                                              'user_id': user_id
                                              })

        else:
            self.count_earn_days = 0

            holiday_status_id = self.env['hr.holidays.status'].search([('name', '=', 'Earn Leaves')], limit=0)

            check_earn_leave = self.env['hr.holidays'].search(
                [("employee_id", "=", employee_id.id), ("holiday_status_id.id", "=", holiday_status_id.id),
                 ('type', '=', 'add')])
            if check_earn_leave:
                for val in check_earn_leave:
                    self.env['hr.holidays'].browse(val.id).write({
                        'id': val.id,
                        'number_of_days_temp': 0,
                        'number_of_days': 0
                    })


    @api.multi
    def action_earn_leaves(self):
        print ('Button Clicked')


    # @api.model
    # def default_get(self, vals):
    #     defaults = super(EmployeeInheitedModel, self).default_get(vals)
    #     print ('default get call')
    #
    #     return defaults


    # Scheduler for Earn Leaves
    @api.model
    def employee_earn_leave_scheduler(self, *args, **kwargs):

        check_employee_id = self.env['hr.employee'].search([])

        for emp_id in check_employee_id:

            employee_id = self.env['hr.employee'].search([('id', '=', emp_id.id)])
            if employee_id.joining_date:
                # checking leave assign days
                check_earn_assign_days = self.env['earn.leave.assign'].search([])
                assign_days = check_earn_assign_days.earn_leave_days

                # checking earn leave id
                holiday_status_id = self.env['hr.holidays.status'].search([('name', '=', 'Earn Leaves')], limit=0)


                # checking earn leave exist or not
                check_earn_leave = self.env['hr.holidays'].search(
                    [("employee_id", "=", employee_id.id), ("holiday_status_id.id", "=", holiday_status_id.id),
                     ('type', '=', 'add')])
                # calculating earn leave according to joining date of employee
                employee_joining_date = datetime.strptime(employee_id.joining_date, "%Y-%m-%d").date()
                today = datetime.now().date()
                total_days = (today - employee_joining_date).days
                earn_leave = total_days / assign_days
                # earn_leave_days = total_days/18
                # self.count_earn_days = earn_leave

                if check_earn_leave:
                    for val in check_earn_leave:
                        if earn_leave > val.number_of_days_temp:

                            #
                            self.env['hr.holidays'].browse(val.id).write({
                                'id': val.id,
                                'number_of_days_temp': earn_leave,
                                'number_of_days': earn_leave
                            })
                        else:
                            self.env['hr.holidays'].browse(val.id).write({
                                'id': val.id,
                                'number_of_days_temp': earn_leave,
                                'number_of_days': earn_leave
                            })





