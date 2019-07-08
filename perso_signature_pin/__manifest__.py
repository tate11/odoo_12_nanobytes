# -*- coding: utf-8 -*-
{
    'name': "Personalizacion Firma por Pin",

    'summary': """
        Modulo personalizado para firmar con pin""",

    'description': """
        
        Nanobytes - Personalizacion Firma por Pin
        
        This module was made by Nanobytes Informatica y Telecomunicaciones S.L,
        for more information, contact us : http://nanobytes.es
        
    """,

    'author': "Nanobytes Informatica y Telecomunicaciones S.L",
    'website': "http://nanobytes.es",
    'category': 'sale',
    'version': '1.0',
    'depends': ['base','sale','sale_management','website','crm'],
    'data': [
        'data/mail_template_data.xml',
        'views/assets.xml',
        'views/view_sale_order.xml',
        'views/view_crm_team.xml',
        'static/src/xml/signature_pin.xml',
        'report/sale_report_templates.xml',
    ],
    'qweb': [],
}
