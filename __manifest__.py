# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2021 Denis Vasquez
#    All Rights Reserved.
#
##############################################################################
{
    'name': "Mejoras conductor",

    'summary': 'Mejoras al app flota',

    'description': """
        Nuevas caracteristicas para el modulo de flota
    """,

    'author': "Denis Vasquez",
    'website': "",
    'license': 'Other proprietary',
    'version': '0.1',
    'contributors': [
        'dvasquez@guip.com',
        'wcerrato@guip.com',
    ],
    'category': 'Extra Tools',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'fleet',
        'hr',
        'sale',
        'product',
        'contacts',
    ],
    'data': [
        
        # D A T A

        # S E C U R I T Y
        'security/ir.model.access.csv',

        # V I E W S
        'views/hr_views.xml',
        'views/fleet_vehicle_views.xml',
        'views/etapas_conductor.xml',
        'views/sale_order_view.xml',
        'views/product_template.xml',
        # 'views/portal_templates.xml',

        # M E N U
        'views/menu_view.xml',
    ],
    'css': ['static/src/css/crm.css'],
    'demo': ['data/fleet_demo.xml'],
    'installable': True,
    'application': True,
    'auto_install': False,
}