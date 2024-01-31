# -*- coding: utf-8 -*-
{
    'name': "Import Forecast",
    'summary': "Customize Import Forecast",
    'description': """Customize Import Forecast""",
    'author': "Taweechai Yuenyang",
    "email": "taweechai.yuenyang@outlook.com",
    'website': 'https://taweechai-yuenyang.github.io',
    'sequence': 5,
    # license คือ หมวดหมู่หน่วยงานของโมดูล
    'license': 'Other OSI approved licence',
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'web', 'mail', 'product'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/forecast_view.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'assets': {
        'web.assets_backend': {
            '/import_forecast/static/src/css/progress_bar_widget.css',
            '/import_forecast/static/src/js/progress_bar_widget.js',
        },
        'web.assets_qweb': {
            '/import_forecast/static/src/xml/progress_bar_widget.xml',
        },
    },
    "application": True,
    'installable': True,  # installable คือ ระบุว่าโมดูลสามารถติดตั้งได้หรือไม่
    'auto_install': False,  # auto_install คือ ระบุว่าโมดูลจะติดตั้งโดยอัตโนมัติหรือไม่
}
