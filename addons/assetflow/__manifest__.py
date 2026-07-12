# -*- coding: utf-8 -*-
{
    'name': 'AssetFlow – Enterprise Asset & Resource Management',
    'version': '17.0.1.0.0',
    'category': 'Operations/Assets',
    'summary': 'Manage company assets, allocations, bookings, maintenance, and audits.',
    'description': """
AssetFlow – Enterprise Asset & Resource Management System
=========================================================
A complete ERP module for managing:
- Company assets lifecycle (register → allocate → maintain → audit → retire)
- Department-wise asset allocation with approval workflow
- Resource booking with conflict detection
- Maintenance requests and approvals
- Audit cycles
- Role-based access control (Admin, Asset Manager, Dept Head, Employee)
- KPI Dashboard with charts
- PDF & Excel reports
    """,
    'author': 'Team BugBusters – Vijay Jangid & Dinesh',
    'website': 'https://github.com/codingwithdinu/AssetFlow',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'mail',
        'hr',
        'web',
    ],
    'data': [
        # Security (always first)
        'security/assetflow_security.xml',
        'security/ir.model.access.csv',
        'security/record_rules.xml',

        # Data
        'data/sequence_data.xml',
        'data/mail_template.xml',
        'data/cron.xml',

        # Views
        'views/assetflow_menu.xml',
        'views/department_views.xml',
        'views/employee_views.xml',
        'views/asset_category_views.xml',
        'views/asset_views.xml',
        'views/allocation_views.xml',
        'views/transfer_views.xml',
        'views/booking_views.xml',
        'views/maintenance_views.xml',
        'views/audit_views.xml',
        'views/dashboard_views.xml',
        'views/report_views.xml',

        # Reports
        'report/report.xml',
        'report/asset_report.xml',
        'report/booking_report.xml',
        'report/maintenance_report.xml',
    ],
    'demo': [
        'data/demo.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'assetflow/static/src/css/assetflow.css',
            'assetflow/static/src/js/dashboard.js',
            'assetflow/static/src/js/charts.js',
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
