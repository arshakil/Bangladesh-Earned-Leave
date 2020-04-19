{
    'name': "Bangladesh Earned Leave",
    'version': '10.0',
    'author': "Metamorphosis",
    'category': 'Human Resources',
    'summary': """
       Our Company credits 21 days' of Earned Leave to an employee after the completion of one year from the date to joining. The calculation is that for every 18 days' worked, the employee earns one day Earned Leave.""",
    'description': """
            An employee may use annual leave for vacations, rest and relaxation, 
            and personal business or emergencies. An employee has a right to take annual leave, 
            subject to the right of the supervisor to schedule the time at which annual leave may be taken. 
            An employee will receive a lump-sum payment for accumulated and accrued annual leave when he or she separates from Federal service or enters on active duty in the industry and elects to receive a lump-sum payment.
            """,
    'maintainer':'Metamorphosis',
    'website':'https://metamorphosis.com.bd',
    'sequence':'1',
    'depends': ['mail','base','hr_holidays','hr'],
    'data': [
        'security/ir.model.access.csv',
        'views/employee_inherited_view.xml',
        'views/annual_leave_assign.xml',
        'data/data.xml',
        'data/scheduler.xml',
    ],
    'demo': [],
    'icon': "/employee_earn_leave/static/description/icon.png",
    'images': ['static/static/description/cover.png'],
    'installable': True,
    'application': True,
    "license": "OPL-1",
    'price':149.0,
    'currency':'EUR',
}
