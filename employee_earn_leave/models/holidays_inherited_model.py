from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import date, datetime

class Holidays_inherited_Model(models.Model):
    _inherit = 'hr.holidays'




    @api.onchange('employee_id')
    def check_leave_type(self):
        # if str(self.holiday_status_id.name) == "Earn Leaves":
        check_earn_assign_days = self.env['earn.leave.assign'].search([])
        assign_days = check_earn_assign_days.earn_leave_days
        print ('assign_days', assign_days)

        holiday_status_id = self.env['hr.holidays.status'].search([('name','=','Earn Leaves')], limit=0)
        print ('holiday_status_id',holiday_status_id.id)

        for record in self:
            check_earn_leave = self.env['hr.holidays'].search(
                [("employee_id", "=", record.employee_id.id), ("holiday_status_id.id", "=", holiday_status_id.id),
                 ('type', '=', 'add')])
            if record.employee_id.joining_date:
                employee_joining_date = datetime.strptime(record.employee_id.joining_date, "%Y-%m-%d").date()
                today = datetime.now().date()
                total_days = (today - employee_joining_date).days
                earn_leave=total_days/assign_days

                if check_earn_leave:
                    for val in check_earn_leave:
                        if earn_leave>val.number_of_days_temp:
                            print('need update')
                            print('need number_of_days_temp', val.number_of_days)
                            print('need number_of_days', val.number_of_days)
                            print('need id', val.id)
                            #
                            self.env['hr.holidays'].browse(val.id).write({
                                'id': val.id,
                                'number_of_days_temp': earn_leave,
                                'number_of_days': earn_leave
                            })
                            #
                            # val.number_of_days_temp=earn_leave
                            # val.number_of_days=earn_leave
                        else:
                            print('no need to update please continue')
                            self.env['hr.holidays'].browse(val.id).write({
                                'id': val.id,
                                'number_of_days_temp': earn_leave,
                                'number_of_days': earn_leave
                            })
                else:
                    holiday_status_id=holiday_status_id.id
                    employee_id=record.employee_id.id
                    holiday_type="employee"
                    number_of_days_temp=earn_leave
                    state="validate"
                    manager_id=1
                    type="add"
                    department_id=record.department_id.id
                    number_of_days=earn_leave

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
                                              'user_id':user_id
                                              })
            else:
                if check_earn_leave:
                    for val in check_earn_leave:
                        self.env['hr.holidays'].browse(val.id).write({
                            'id': val.id,
                            'number_of_days_temp': 0,
                            'number_of_days': 0
                        })
