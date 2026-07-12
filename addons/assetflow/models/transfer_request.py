# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class AssetTransfer(models.Model):
    _name = 'assetflow.transfer'
    _description = 'Asset Transfer Request'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'
    _order = 'request_date desc'

    name = fields.Char(
        string='Transfer Reference',
        required=True,
        copy=False,
        readonly=True,
        default='New',
    )
    asset_id = fields.Many2one(
        'assetflow.asset',
        string='Asset',
        required=True,
        tracking=True,
        ondelete='restrict',
    )
    from_department_id = fields.Many2one(
        'assetflow.department',
        string='From Department',
        required=True,
        tracking=True,
    )
    to_department_id = fields.Many2one(
        'assetflow.department',
        string='To Department',
        required=True,
        tracking=True,
    )
    from_employee_id = fields.Many2one(
        'assetflow.employee',
        string='From Employee',
    )
    to_employee_id = fields.Many2one(
        'assetflow.employee',
        string='To Employee',
    )
    request_date = fields.Date(
        string='Request Date',
        default=fields.Date.today,
        required=True,
    )
    transfer_date = fields.Date(string='Transfer Date')
    reason = fields.Text(string='Transfer Reason', required=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('completed', 'Completed'),
        ('rejected', 'Rejected'),
    ], string='Status', default='draft', tracking=True)
    approved_by = fields.Many2one('res.users', string='Approved By', readonly=True)
    notes = fields.Text(string='Notes')

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'assetflow.transfer.sequence'
            ) or 'TRF-0000'
        return super().create(vals)

    @api.constrains('from_department_id', 'to_department_id')
    def _check_different_departments(self):
        for rec in self:
            if rec.from_department_id == rec.to_department_id:
                raise ValidationError(
                    'Source and destination departments must be different!'
                )

    def action_submit(self):
        self.write({'state': 'submitted'})

    def action_approve(self):
        self.write({
            'state': 'approved',
            'approved_by': self.env.uid,
        })

    def action_complete(self):
        for rec in self:
            rec.asset_id.write({
                'department_id': rec.to_department_id.id,
                'employee_id': rec.to_employee_id.id if rec.to_employee_id else False,
            })
            rec.asset_id._log_history(
                f'Transferred from {rec.from_department_id.name} '
                f'to {rec.to_department_id.name}'
            )
            rec.write({
                'state': 'completed',
                'transfer_date': fields.Date.today(),
            })

    def action_reject(self):
        self.write({'state': 'rejected'})
