# -*- coding: utf-8 -*-
{
    'name': "hr attendance  professional policy geospatial address mechanism",
    'summary': """
        Module allows you to automatically check whether an employee
        is in a given geofence (store or office) with GPS coordinates
        accuracy from html5 standard (1 meter at best)""",

    'author': "Shurshilov Artem",
    'website': "https://eurodoo.com",
    "live_test_url": "https://eurodoo.com",
    'category': 'Human Resources',
    'version': '1.0',
    "license": "OPL-1",
    'price': 100,
    'currency': 'EUR',
    'images': [
        'static/description/preview.gif',
    ],
    'depends': ['base', 'web', 'hr_attendance_base', 'hr_attendance_geo_html'],
    "external_dependencies": {"python": ["pyproj", "shapely"]},
    'data': [
        'security/ir.model.access.csv',
        'security/hr_attendance_security.xml',
        'views/views.xml',
        'views/res_config_settings_views.xml',
    ],
    "assets": {
        "web.assets_backend": [
            # "hr_attendance_geospatial/static/src/js/attendances_geospatial.js",
        ],
    },
    'qweb': [
        "static/src/xml/attendance.xml",
    ],
}
