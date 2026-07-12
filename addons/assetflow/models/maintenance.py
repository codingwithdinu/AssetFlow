# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class MaintenanceRequest(models.Model):
    _name = 'assetflow.maintenance'
    _description = 'Maintenance Request'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'
    _order = 'request_date desc'

    name = fields.Char(
        string='Maintenance Reference',
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
    reported_by = fields.Many2one(
        'assetflow.employee',
        string='Reported By',
        required=True,
    )
    department_id = fields.Many2one(
        'assetflow.department',
        string='Department',
        related='reported_by.department_id',
        store=True,
    )
    issue_description = fields.Text(
        string='Issue Description',
        required=True,
    )
    priority = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ], string='Priority', default='medium', tracking=True)
    request_date = fields.Date(
        string='Request Date',
        default=fields.Date.today,
        required=True,
    )
    scheduled_date = fields.Date(string='Scheduled Date')
    completion_date = fields.Date(string='Completion Date')
    technician = fields.Char(string='Technician Name')
    repair_cost = fields.Float(string='Repair Cost (₹)')
    state = fields.Selection([
        ('reported', 'Reported'),
        ('approved', 'Approved'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='reported', tracking=True)
    resolution_notes = fields.Text(string='Resolution Notes')

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'assetflow.maintenance.sequence'
            ) or 'MNT-0000'
        return super().create(vals)

    def action_approve(self):
        for rec in self:
            rec.asset_id.write({'state': 'maintenance'})
            rec.asset_id._log_history('Sent for Maintenance')
        self.write({'state': 'approved'})

    def action_start(self):
        self.write({'state': 'in_progress'})

    def action_complete(self):
        for rec in self:
            rec.asset_id.write({'state': 'available'})
            rec.asset_id._log_history('Maintenance Completed – Asset Available')
        self.write({
            'state': 'completed',
            'completion_date': fields.Date.today(),
        })

    def action_cancel(self):
        self.write({'state': 'cancelled'})
