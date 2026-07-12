# -*- coding: utf-8 -*-
from odoo import models, fields, api


class AssetAudit(models.Model):
    _name = 'assetflow.audit'
    _description = 'Asset Audit'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'
    _order = 'audit_date desc'

    name = fields.Char(
        string='Audit Reference',
        required=True,
        copy=False,
        readonly=True,
        default='New',
    )
    audit_date = fields.Date(
        string='Audit Date',
        required=True,
        default=fields.Date.today,
    )
    conducted_by = fields.Many2one('res.users', string='Conducted By', required=True)
    department_id = fields.Many2one(
        'assetflow.department',
        string='Department (scope)',
    )
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ], string='Status', default='draft', tracking=True)
    notes = fields.Text(string='Audit Notes')

    audit_line_ids = fields.One2many(
        'assetflow.audit.line',
        'audit_id',
        string='Audit Lines',
    )

    # Summary computed
    total_assets = fields.Integer(
        string='Total Audited', compute='_compute_summary', store=True)
    found_count = fields.Integer(
        string='Found', compute='_compute_summary', store=True)
    missing_count = fields.Integer(
        string='Missing', compute='_compute_summary', store=True)
    damaged_count = fields.Integer(
        string='Damaged', compute='_compute_summary', store=True)

    @api.depends('audit_line_ids.status')
    def _compute_summary(self):
        for rec in self:
            lines = rec.audit_line_ids
            rec.total_assets = len(lines)
            rec.found_count = len(lines.filtered(lambda l: l.status == 'found'))
            rec.missing_count = len(lines.filtered(lambda l: l.status == 'missing'))
            rec.damaged_count = len(lines.filtered(lambda l: l.status == 'damaged'))

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'assetflow.audit.sequence'
            ) or 'AUD-0000'
        return super().create(vals)

    def action_start(self):
        self.write({'state': 'in_progress'})

    def action_complete(self):
        # Update asset status for missing/damaged
        for line in self.audit_line_ids:
            if line.status == 'missing':
                line.asset_id.write({'state': 'lost'})
            elif line.status == 'damaged':
                line.asset_id.write({'state': 'maintenance'})
        self.write({'state': 'completed'})

    def action_load_assets(self):
        """Auto-load all assets of the selected department."""
        domain = []
        if self.department_id:
            domain = [('department_id', '=', self.department_id.id)]
        assets = self.env['assetflow.asset'].search(domain)
        existing = self.audit_line_ids.mapped('asset_id')
        for asset in assets:
            if asset not in existing:
                self.env['assetflow.audit.line'].create({
                    'audit_id': self.id,
                    'asset_id': asset.id,
                    'status': 'found',
                })


class AssetAuditLine(models.Model):
    _name = 'assetflow.audit.line'
    _description = 'Audit Line'

    audit_id = fields.Many2one(
        'assetflow.audit',
        string='Audit',
        required=True,
        ondelete='cascade',
    )
    asset_id = fields.Many2one(
        'assetflow.asset',
        string='Asset',
        required=True,
    )
    asset_tag = fields.Char(related='asset_id.asset_tag', string='Tag', store=True)
    category_id = fields.Many2one(
        related='asset_id.category_id', string='Category', store=True)
    status = fields.Selection([
        ('found', 'Found'),
        ('missing', 'Missing'),
        ('damaged', 'Damaged'),
    ], string='Condition', default='found', required=True)
    remarks = fields.Char(string='Remarks')
