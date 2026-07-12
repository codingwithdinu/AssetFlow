# -*- coding: utf-8 -*-
from odoo import models, fields


class AssetCategory(models.Model):
    _name = 'assetflow.category'
    _description = 'Asset Category'
    _rec_name = 'name'
    _order = 'name'

    name = fields.Char(string='Category Name', required=True)
    code = fields.Char(string='Category Code', required=True, size=5)
    description = fields.Text(string='Description')
    depreciation_years = fields.Integer(
        string='Useful Life (Years)',
        default=5,
    )
    icon = fields.Char(string='Icon Class', default='fa-cubes')
    active = fields.Boolean(default=True)

    asset_count = fields.Integer(
        string='Assets',
        compute='_compute_asset_count',
    )

    def _compute_asset_count(self):
        for rec in self:
            rec.asset_count = self.env['assetflow.asset'].search_count(
                [('category_id', '=', rec.id)]
            )

    _sql_constraints = [
        ('code_unique', 'UNIQUE(code)', 'Category code must be unique!'),
    ]
