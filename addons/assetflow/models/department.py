# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class AssetFlowDepartment(models.Model):
    _name = 'assetflow.department'
    _description = 'Department'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'
    _order = 'name'

    name = fields.Char(
        string='Department Name',
        required=True,
        tracking=True,
    )
    code = fields.Char(
        string='Department Code',
        required=True,
        size=10,
    )
    description = fields.Text(string='Description')
    head_id = fields.Many2one(
        'assetflow.employee',
        string='Department Head',
        tracking=True,
    )
    location = fields.Char(string='Location / Floor')
    active = fields.Boolean(default=True)

    # Computed
    employee_count = fields.Integer(
        string='Employees',
        compute='_compute_employee_count',
    )
    asset_count = fields.Integer(
        string='Assets',
        compute='_compute_asset_count',
    )

    @api.depends()
    def _compute_employee_count(self):
        for rec in self:
            rec.employee_count = self.env['assetflow.employee'].search_count(
                [('department_id', '=', rec.id)]
            )

    @api.depends()
    def _compute_asset_count(self):
        for rec in self:
            rec.asset_count = self.env['assetflow.asset'].search_count(
                [('department_id', '=', rec.id)]
            )

    _sql_constraints = [
        ('code_unique', 'UNIQUE(code)', 'Department code must be unique!'),
    ]
