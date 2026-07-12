# -*- coding: utf-8 -*-
{
    'name': 'AssetFlow - Enterprise Asset & Resource Management',
    'version': '18.0.1.0.0',
    'category': 'Operations/Assets',
    'summary': 'Manage company assets, allocations, bookings, maintenance, and audits.',
    'description': """
AssetFlow - Enterprise Asset & Resource Management
==================================================
Complete ERP solution for managing company assets,
allocations, bookings, maintenance, audits and reports.
""",
    'author': 'Team BugBusters - Vijay Jangid & Dinesh',
    'website': 'https://github.com/codingwithdinu/AssetFlow',
    'license': 'LGPL-3',

    'depends': [
        'base',
        'mail',
        'hr',
        'web',
    ],

    'data': [

        # --------------------
        # SECURITY
        # --------------------
        'security/assetflow_security.xml',
        'security/ir.model.access.csv',
        'security/record_rules.xml',

        # --------------------
        # DATA
        # --------------------
        'data/sequence_data.xml',
        'data/mail_template.xml',
        'data/cron.xml',

        # --------------------
        # DASHBOARD ACTION FIRST
        # --------------------
        'views/dashboard_views.xml',

        # --------------------
        # MASTER VIEWS
        # --------------------
        'views/department_views.xml',
        'views/employee_views.xml',
        'views/asset_category_views.xml',
        'views/asset_views.xml',

        # --------------------
        # TRANSACTION VIEWS
        # --------------------
        'views/allocation_views.xml',
        'views/transfer_views.xml',
        'views/booking_views.xml',
        'views/maintenance_views.xml',
        'views/audit_views.xml',

        # --------------------
        # REPORT VIEWS
        # --------------------
        'views/report_views.xml',

        # --------------------
        # REPORT DEFINITIONS
        # --------------------
        'report/report.xml',
        'report/asset_report.xml',
        'report/booking_report.xml',
        'report/maintenance_report.xml',

        # --------------------
        # MENU MUST BE LAST
        # --------------------
        'views/assetflow_menu.xml',
    ],

    'demo': [
        'data/demo.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'assetflow/static/src/css/assetflow.css',
            'assetflow/static/src/js/charts.js',
            'assetflow/static/src/js/dashboard.js',
        ],
        'web.assets_qweb': [
            'assetflow/static/src/xml/dashboard.xml',
        ],
    },

    'installable': True,
    'application': True,
    'auto_install': False,
    'sequence': 1,
}