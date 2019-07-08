# -*- coding: utf-8 -*-
{
    'name': "Documentation",

    'summary': """
        Your own documentation""",

    'description': """
        
        Ionel Lazar - Documentation
        
        Best module ever for documentation
        
    """,

    'author': "Ionel Lazar",
    'website': "",
    'category': 'documentation',
    'version': '1.0',
    'depends': ['base', 'mail'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/view_board.xml',
        'views/view_documentation.xml',
        'views/view_manual.xml',
        'views/view_app.xml',
        'views/view_script.xml',
        'views/view_category.xml',
        'views/view_language.xml',
        'views/view_tag.xml',
        'views/view_user.xml',
        'views/view_menus.xml',
        'data/data.xml',
        ],
    'qweb': [],
    'installable': True,
    'application': True,
}
