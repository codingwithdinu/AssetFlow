# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class AssetAllocation(models.Model):
    _name = 'assetflow.allocation'
    _description = 'Asset Allocation'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'
    _order = 'allocation_date desc'

    name = fields.Char(
        string='Allocation Reference',
        required=True,
        copy=False,
        readonly=True,
        default='New',
    )
    asset_id = fields.Many2one(
        'assetflow.asset',
        string='Asset',
        required=True,
        domain=[('state', '=', 'available')],
        tracking=True,
        ondelete='restrict',
    )
    employee_id = fields.Many2one(
        'assetflow.employee',
        string='Allocated To',
        required=True,
        tracking=True,
    )
    department_id = fields.Many2one(
        'assetflow.department',
        string='Department',
        related='employee_id.department_id',
        store=True,
    )
    allocation_date = fields.Date(
        string='Allocation Date',
        required=True,
        default=fields.Date.today,
    )
    expected_return_date = fields.Date(string='Expected Return Date')
    actual_return_date = fields.Date(string='Actual Return Date')
    purpose = fields.Text(string='Purpose / Reason')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('returned', 'Returned'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', tracking=True)
    notes = fields.Text(string='Notes')

    # ─── Auto-generate reference ──────────────────────────────────────
    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'assetflow.allocation.sequence'
            ) or 'ALLOC-0000'
        return super().create(vals)

    # ─── Business Rule: Prevent double allocation ─────────────────────
    @api.constrains('asset_id', 'state')
    def _check_double_allocation(self):
        for rec in self:
            if rec.state == 'active':
                conflict = self.search([
                    ('asset_id', '=', rec.asset_id.id),
                    ('state', '=', 'active'),
                    ('id', '!=', rec.id),
                ])
                if conflict:
                    raise ValidationError(
                        f'Asset "{rec.asset_id.name}" is already allocated to '
                        f'"{conflict[0].employee_id.name}". '
                        f'Please return it before re-allocating.'
                    )

    # ─── Workflow Actions ─────────────────────────────────────────────
    def action_allocate(self):
        for rec in self:
            if rec.asset_id.state != 'available':
                raise ValidationError(
                    f'Asset "{rec.asset_id.name}" is not available for allocation. '
                    f'Current status: {rec.asset_id.state}'
                )
            rec.asset_id.write({
                'state': 'allocated',
                'employee_id': rec.employee_id.id,
                'department_id': rec.department_id.id,
            })
            rec.asset_id._log_history(f'Allocated to {rec.employee_id.name}')
            rec.write({'state': 'active'})
        return True

    def action_return(self):
        for rec in self:
            rec.actual_return_date = fields.Date.today()
            rec.asset_id.write({
                'state': 'available',
                'employee_id': False,
            })
            rec.asset_id._log_history(f'Returned by {rec.employee_id.name}')
            rec.write({'state': 'returned'})
        return True

    def action_cancel(self):
        self.write({'state': 'cancelled'})
