# -*- coding: utf-8 -*-
{
    'name': 'Steven_servicios',
    'version': '17.0.1.0',
    'description': """ Steven_servicios Description """,
    'summary': """ Steven_servicios Summary """,
    'author': 'Steven Slezak Bellido',
    'website': '',
    'category': 'Uncategorized',
    'depends': ['base', 'web', 'mail'],
    "data": [
        "security/ir.model.access.csv",
        "views/cliente_views.xml",
        "views/cita_views.xml",
        "views/empleado_views.xml",
        "views/servicio_views.xml",
        "views/steven_servicios_menu.xml",
        "data/cron_data.xml",
    ],'assets': {
            'web.assets_backend': [
                'steven_servicios/static/src/**/*'
            ],
        },
    'application': True,
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
    'icon': 'steven_servicios/static/description/icon.png',
}
