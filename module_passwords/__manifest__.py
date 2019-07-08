# -*- coding: utf-8 -*-
{
    'name': "Secure Password",

    'summary': """
        Manage your partner passwords""",

    'description': """
        
        Nanobytes - Password
        
        This module was made with the intention to manage
        your partner passwords with high security
        
        This module was made by Nanobytes Informatica y Telecomunicaciones S.L,
        for more information, contact us : http://nanobytes.es
        
    """,

    'author': "Nanobytes Informatica y Telecomunicaciones S.L",
    'category': 'Security',
    'version': '1.0',
    'depends': ['base', 'mail', 'helpdesk'],
    'installable': True,
    'application': True,
    'data': [             
        'security/security.xml',
        'views/passwords_view.xml',
        'views/passwords_assets.xml',
        'views/res_partner_view.xml',
        'views/helpdesk_inherit_view.xml',      
        'security/ir.model.access.csv',
    ],
}
