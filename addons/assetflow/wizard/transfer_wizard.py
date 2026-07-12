# -*- coding: utf-8 -*-
from odoo import models, fields, api


class TransferWizard(models.TransientModel):
    _name = 'assetflow.transfer.wizard'
    _description = 'Quick Transfer Wizard'

    asset_id = fields.Many2one('assetflow.asset', string='Asset', required=True)
    from_department_id = fields.Many2one(
        'assetflow.department', string='From Department', required=True)
    to_department_id = fields.Many2one(
        'assetflow.department', string='To Department', required=True)
    reason = fields.Text(string='Reason', required=True)

    def action_create_transfer(self):
        self.env['assetflow.transfer'].create({
            'asset_id': self.asset_id.id,
            'from_department_id': self.from_department_id.id,
            'to_department_id': self.to_department_id.id,
            'reason': self.reason,
        })
        return {'type': 'ir.actions.act_window_close'}
