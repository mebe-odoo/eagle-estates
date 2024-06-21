# -*- coding: utf-8 -*-
{
    'name': "Eagle Estates",
    'summary': """A reel estate management solution for Eagle LLC.""",
    'description': """A reel estate management solution for Eagle LLC.""",
    'author': "Eagle Tech LLC.",
    'website': "https://www.eagle-tech.com",
    'category': 'Eagle Tech/Real Estate',
    'version': '17.0.0.1',
    'depends': ['base', 'mail', 'portal'],
    'data': [
        'security/ir.model.access.csv',
        'data/eagle_tag_data.xml',
        'data/eagle_property_data.xml',
        'wizards/eagle_property_room_surface_wizard_views.xml',
        'views/eagle_tag_views.xml',
        'views/eagle_property_room_views.xml',
        'views/eagle_property_views.xml',
        'views/portal_templates.xml'
    ],
    'application': True
}
