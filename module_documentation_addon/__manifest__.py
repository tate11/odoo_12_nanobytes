# -*- coding: utf-8 -*-
{
    'name': "Documentation Addon",

    'summary': """
        Your own documentation addon""",

    'description': """
        
        Ionel Lazar - Documentation addon
        
        Best module ever for documentation
        
    """,

    'author': "Ionel Lazar",
    'website': "",
    'category': 'documentation',
    'version': '1.0',
    'depends': ['base', 'module_documentation', 'helpdesk', 'documents'],
    'data': [
        'views/view_documentation.xml',
        'views/view_manual.xml',
        'views/view_helpdesk.xml',
        'data/data.xml',
        'views/documents_views.xml'
        ],
    'qweb': [],
    'installable': True,
    'application': False,
}
