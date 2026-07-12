# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class AssetFlowEmployee(models.Model):
    _name = 'assetflow.employee'
    _description = 'Employee'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'
    _order = 'name'

    name = fields.Char(string='Full Name', required=True, tracking=True)
    employee_id = fields.Char(string='Employee ID', required=True)
    email = fields.Char(string='Email', required=True)
    phone = fields.Char(string='Phone')
    department_id = fields.Many2one(
        'assetflow.department',
        string='Department',
        required=True,
        tracking=True,
        ondelete='restrict',
    )
    job_title = fields.Char(string='Job Title')
    image = fields.Binary(string='Photo')
    active = fields.Boolean(default=True)
    user_id = fields.Many2one('res.users', string='Related User')

    # Computed fields
    allocated_asset_count = fields.Integer(
        string='Allocated Assets',
        compute='_compute_allocated_assets',
    )

    @api.depends()
    def _compute_allocated_assets(self):
        for rec in self:
            rec.allocated_asset_count = self.env['assetflow.allocation'].search_count([
                ('employee_id', '=', rec.id),
                ('state', '=', 'active'),
            ])

    _sql_constraints = [
        ('employee_id_unique', 'UNIQUE(employee_id)', 'Employee ID must be unique!'),
        ('email_unique', 'UNIQUE(email)', 'Employee email must be unique!'),
    ]
