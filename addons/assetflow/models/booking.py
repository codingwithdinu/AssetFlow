# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ResourceBooking(models.Model):
    _name = 'assetflow.booking'
    _description = 'Resource Booking'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'
    _order = 'start_datetime desc'

    name = fields.Char(
        string='Booking Reference',
        required=True,
        copy=False,
        readonly=True,
        default='New',
    )
    asset_id = fields.Many2one(
        'assetflow.asset',
        string='Resource / Asset',
        required=True,
        tracking=True,
        domain=[('state', 'in', ['available', 'allocated'])],
    )
    employee_id = fields.Many2one(
        'assetflow.employee',
        string='Booked By',
        required=True,
        tracking=True,
    )
    department_id = fields.Many2one(
        'assetflow.department',
        string='Department',
        related='employee_id.department_id',
        store=True,
    )
    start_datetime = fields.Datetime(
        string='Start Date & Time',
        required=True,
        tracking=True,
    )
    end_datetime = fields.Datetime(
        string='End Date & Time',
        required=True,
        tracking=True,
    )
    purpose = fields.Char(string='Purpose', required=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', tracking=True)
    notes = fields.Text(string='Notes')

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'assetflow.booking.sequence'
            ) or 'BK-0000'
        return super().create(vals)

    # ─── Business Rule: No overlapping bookings ───────────────────────
    @api.constrains('asset_id', 'start_datetime', 'end_datetime', 'state')
    def _check_booking_overlap(self):
        for rec in self:
            if rec.state in ('draft', 'cancelled'):
                continue
            if rec.start_datetime >= rec.end_datetime:
                raise ValidationError('End time must be after start time!')
            overlapping = self.search([
                ('asset_id', '=', rec.asset_id.id),
                ('state', '=', 'confirmed'),
                ('id', '!=', rec.id),
                ('start_datetime', '<', rec.end_datetime),
                ('end_datetime', '>', rec.start_datetime),
            ])
            if overlapping:
                raise ValidationError(
                    f'"{rec.asset_id.name}" is already booked from '
                    f'{overlapping[0].start_datetime} to {overlapping[0].end_datetime}. '
                    f'Please choose a different time slot.'
                )

    def action_confirm(self):
        self._check_booking_overlap()
        self.write({'state': 'confirmed'})

    def action_complete(self):
        self.write({'state': 'completed'})

    def action_cancel(self):
        self.write({'state': 'cancelled'})
