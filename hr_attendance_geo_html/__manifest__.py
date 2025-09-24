# -*- coding: utf-8 -*-
{
    'name': "hr attendance professional policy geolocation via html5 geolocate",

    'summary': """
        Module provides saves the geolocation of the geo-coordinates of
        the employee / user from the device on which it works displays
        them on the openstreet map and also allows you to view the 
        geo-location of the employee in google maps""",

    'author': "Shurshilov Artem",
    'website': "https://eurodoo.com",
    "live_test_url": "https://eurodoo.com",
    'category': 'Human Resources',
    'version': '1.0',
    "license": "OPL-1",
    'price': 90,
    'currency': 'EUR',
    'images': [
        'static/description/Attendance_geo.png',
        'static/description/Attendance_geo.png',
        'static/description/Attendance_geo.png',
        'static/description/Attendance_geo.png',
    ],
    'depends': ['base', 'web', 'hr_attendance_base'],
    'data': [
        'views/res_config_settings_views.xml',
        'views/views.xml',
    ],
    'qweb': [
        "static/src/xml/attendance.xml",
    ],
    'assets': {
        'web.assets_qweb': [
            'hr_attendance_geo_html/static/src/xml/attendance.xml',
        ],
        "web.assets_backend": [
            "hr_attendance_geo_html/static/src/css/leaflet.css",
            "hr_attendance_geo_html/static/src/css/leaflet.fullscreen.css",
            "hr_attendance_geo_html/static/src/css/geo.css",
            # "hr_attendance_geo_html/static/src/js/lib/leaflet.js",
            # "hr_attendance_geo_html/static/src/js/lib/leaflet-geoip.js",
            # "hr_attendance_geo_html/static/src/js/lib/leaflet.fullscreen.js",
            # "hr_attendance_geo_html/static/src/js/geo_html_attendance.js",
        ],
    },
}
