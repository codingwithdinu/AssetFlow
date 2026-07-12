# -*- coding: utf-8 -*-
from odoo import models, fields


class AssetHistory(models.Model):
    _name = 'assetflow.asset.history'
    _description = 'Asset History Log'
    _rec_name = 'asset_id'
    _order = 'create_date desc'

    asset_id = fields.Many2one(
        'assetflow.asset',
        string='Asset',
        required=True,
        ondelete='cascade',
    )
    action = fields.Char(string='Action', required=True)
    employee_id = fields.Many2one('assetflow.employee', string='Employee')
    department_id = fields.Many2one('assetflow.department', string='Department')
    date = fields.Datetime(
        string='Date',
        default=fields.Datetime.now,
        readonly=True,
    )
    performed_by = fields.Many2one(
        'res.users',
        string='Performed By',
        default=lambda self: self.env.uid,
        readonly=True,
    )
    notes = fields.Text(string='Notes')
