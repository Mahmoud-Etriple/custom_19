# -*- coding: utf-8 -*-
{

    'name': 'Document Management System',
    'summary': 'Document Management System',
    'author': "Add Value For Consulting",
    'company': 'Add Value For Consulting',
    'version': '1.0',
    'license': 'AGPL-3',

    'version': '19.0',
    'depends': ['mail'],
    'data': [
        'security/account_security.xml',
        'security/ir.model.access.csv',
        'views/document.xml',
    ],
    'images': [
        'static/description/main_screenshot.png',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}