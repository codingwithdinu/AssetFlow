# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date


class AssetFlowAsset(models.Model):
    _name = 'assetflow.asset'
    _description = 'Asset'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'
    _order = 'asset_tag'

    # ─── Identification ───────────────────────────────────────────────
    asset_tag = fields.Char(
        string='Asset Tag',
        required=True,
        copy=False,
        readonly=True,
        default='New',
        tracking=True,
    )
    name = fields.Char(string='Asset Name', required=True, tracking=True)
    serial_number = fields.Char(string='Serial Number', tracking=True)
    brand = fields.Char(string='Brand / Manufacturer')
    model_number = fields.Char(string='Model Number')

    # ─── Classification ───────────────────────────────────────────────
    category_id = fields.Many2one(
        'assetflow.category',
        string='Category',
        required=True,
        ondelete='restrict',
    )

    # ─── Assignment ───────────────────────────────────────────────────
    department_id = fields.Many2one(
        'assetflow.department',
        string='Department',
        tracking=True,
    )
    employee_id = fields.Many2one(
        'assetflow.employee',
        string='Current Holder',
        tracking=True,
    )
    location = fields.Char(string='Physical Location')

    # ─── Financial ────────────────────────────────────────────────────
    purchase_date = fields.Date(string='Purchase Date')
    purchase_price = fields.Float(string='Purchase Price (₹)')
    warranty_expiry = fields.Date(string='Warranty Expiry Date')
    depreciation_rate = fields.Float(string='Depreciation Rate (%)', default=20.0)

    # ─── Status ───────────────────────────────────────────────────────
    state = fields.Selection([
        ('available', 'Available'),
        ('allocated', 'Allocated'),
        ('maintenance', 'Under Maintenance'),
        ('retired', 'Retired'),
        ('lost', 'Lost / Missing'),
    ], string='Status', default='available', tracking=True, required=True)

    # ─── Notes ────────────────────────────────────────────────────────
    description = fields.Text(string='Description / Specs')
    notes = fields.Text(string='Internal Notes')
    image = fields.Binary(string='Asset Image')
    active = fields.Boolean(default=True)

    # ─── Computed ─────────────────────────────────────────────────────
    warranty_status = fields.Selection([
        ('valid', 'Under Warranty'),
        ('expired', 'Warranty Expired'),
        ('na', 'N/A'),
    ], string='Warranty Status', compute='_compute_warranty_status', store=True)

    age_years = fields.Float(
        string='Age (Years)',
        compute='_compute_age',
        store=True,
    )

    # ─── Auto-generate asset tag ──────────────────────────────────────
    @api.model
    def create(self, vals):
        if vals.get('asset_tag', 'New') == 'New':
            vals['asset_tag'] = self.env['ir.sequence'].next_by_code(
                'assetflow.asset.sequence'
            ) or 'AF-0000'
        return super().create(vals)

    @api.depends('warranty_expiry')
    def _compute_warranty_status(self):
        today = date.today()
        for rec in self:
            if not rec.warranty_expiry:
                rec.warranty_status = 'na'
            elif rec.warranty_expiry >= today:
                rec.warranty_status = 'valid'
            else:
                rec.warranty_status = 'expired'

    @api.depends('purchase_date')
    def _compute_age(self):
        today = date.today()
        for rec in self:
            if rec.purchase_date:
                delta = today - rec.purchase_date
                rec.age_years = round(delta.days / 365.25, 1)
            else:
                rec.age_years = 0.0

    # ─── Business Rule: Cannot allocate retired/lost assets ──────────
    @api.constrains('state')
    def _check_state_transition(self):
        for rec in self:
            if rec.state == 'allocated' and not rec.employee_id:
                raise ValidationError(
                    'Cannot mark asset as Allocated without assigning an employee!'
                )

    _sql_constraints = [
        ('serial_unique', 'UNIQUE(serial_number)',
         'Serial number must be unique per asset!'),
    ]

    # ─── Action buttons ───────────────────────────────────────────────
    def action_mark_available(self):
        self.write({'state': 'available', 'employee_id': False})
        self._log_history('Marked as Available')

    def action_mark_maintenance(self):
        self.write({'state': 'maintenance'})
        self._log_history('Sent for Maintenance')

    def action_retire(self):
        self.write({'state': 'retired'})
        self._log_history('Asset Retired')

    def _log_history(self, action):
        self.env['assetflow.asset.history'].create({
            'asset_id': self.id,
            'action': action,
            'employee_id': self.employee_id.id,
            'department_id': self.department_id.id,
        })
