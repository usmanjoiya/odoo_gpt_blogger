# -*- coding: utf-8 -*-
{
    'name': "OdooGPT Blogger",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "MountSol",
    'website': "https://www.mountsol.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'website_blog', 'website', 'web'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'data/ai_blog_button.xml',
        'data/ai_content_page.xml',
    ],
    'assets': {
        'web.assets_backend': [
            '/odoo_gpt_blogger/static/src/js/update_button.js',
        ],
        'web.assets_qweb': [
            # 'ms_dashboard/static/src/xml/dashboard_template.xml',
        ],
    },

    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
