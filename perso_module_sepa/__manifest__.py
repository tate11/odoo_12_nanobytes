# -*- coding: utf-8 -*-
{
    'name': "Personalización Módulo SEPA",

    'summary': """
        Personalizaciones para elegir el tipo de mandato""",

    'description': """
        Este módulo engloba las personalizaciones realizadas para elegir el tipo de mandato incluyendo:

    """,

    'author': "Nanobytes Informática y Telecomunicaciones S.L.",
    'website': "https://www.nanobytes.es",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Specific Industry Applications',
    'version': '0.1',

    # any module necessary for this one to work correctly
    # 'depends': ['base', 'sale_management', 'account_invoicing', 'account_accountant', 'l10n_es'],
    'depends': [
        'base', 'account', 'account_sepa_direct_debit', 'sale_subscription', 'sale', 'sale_management'
    ],

    # always loaded
    'data': [
        'views/view_mandate.xml'
    ],
    'qweb': [
    ],
    # only loaded in demonstration mode
    'demo': [
    ],

    'installable': True,
    'application': True,
    'auto_install': False,
}
