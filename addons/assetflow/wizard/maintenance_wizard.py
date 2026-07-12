# -*- coding: utf-8 -*-
from odoo import models, fields, api


class MaintenanceWizard(models.TransientModel):
    _name = 'assetflow.maintenance.wizard'
    _description = 'Quick Maintenance Request Wizard'

    asset_id = fields.Many2one('assetflow.asset', string='Asset', required=True)
    reported_by = fields.Many2one('assetflow.employee', string='Reported By', required=True)
    issue_description = fields.Text(string='Issue', required=True)
    priority = fields.Selection([
        ('low', 'Low'), ('medium', 'Medium'),
        ('high', 'High'), ('critical', 'Critical'),
    ], default='medium', required=True)

    def action_submit(self):
        self.env['assetflow.maintenance'].create({
            'asset_id': self.asset_id.id,
            'reported_by': self.reported_by.id,
            'issue_description': self.issue_description,
            'priority': self.priority,
        })
        return {'type': 'ir.actions.act_window_close'}
