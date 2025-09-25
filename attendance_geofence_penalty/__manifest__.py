# -*- coding: utf-8 -*-
{
    'name': 'Attendance with GPS Late Check In Penalty',
    'version': '17.1',
    'category': 'Human Resources',
    'summary': 'The Attendance Geo-Fence Penalty module automatically tracks employee attendance based on their '
               'check-in location and arrival time. If an employee checks in outside the offices set geo-location or '
               'arrives late, the system can apply penalties (leave deductions or salary cuts) automatically '
               'through scheduled jobs (cron).',
    'description': """ This module is designed for companies that want strict control over: Where employees check 
    in (office geo-location rules). How punctual employees are. Automatically applying penalties for repeated violations.
     It integrates with Odoo’s Attendance module and adds: Geo-status checks on check-in. Late minute calculation. 
     Automatic penalty scheduling (cron jobs run daily or weekly).""",
    'author': 'AppsComp Widgets Pvt Ltd',
    'company': 'AppsComp Widgets Pvt Ltd',
    'website': 'https://www.appscomp.com',
    'license': 'LGPL-3',
    'images': ['static/description/banner.png'],
    'depends': ['hr_attendance', 'hr'],
    'data': [
        'views/hr_attendance_views.xml',
        'data/attendance_cron.xml',
    ],
    'installable': True,
    'application': False,
}
