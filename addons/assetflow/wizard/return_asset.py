# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ReturnAssetWizard(models.TransientModel):
    _name = 'assetflow.return.asset.wizard'
    _description = 'Return Asset Wizard'

    allocation_id = fields.Many2one(
        'assetflow.allocation',
        string='Allocation',
        required=True,
        domain=[('state', '=', 'active')],
    )
    return_date = fields.Date(string='Return Date', default=fields.Date.today, required=True)
    condition_notes = fields.Text(string='Asset Condition Notes')

    def action_return(self):
        self.allocation_id.actual_return_date = self.return_date
        self.allocation_id.action_return()
        return {'type': 'ir.actions.act_window_close'}
