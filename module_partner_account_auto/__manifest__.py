# -*- coding: utf-8 -*-
{
    'name': "module_account_increment",

    'summary': """
        Partner's account auto creation
     """,

    'description': """
        Automatic creation of payable and receivable accounts for partners on creation
    """,

    'author': "Nanobytes",
    'website': "http://nanobytes.es",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account', 'account_reports'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
}
