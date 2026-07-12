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
        self.allocation_id.write({
            'actual_return_date': self.return_date,
        })
        self.allocation_id.asset_id.write({
            'state': 'available',
            'employee_id': False,
        })
        self.allocation_id.asset_id._log_history(
            f'Returned by {self.allocation_id.employee_id.name}'
        )
        self.allocation_id.write({'state': 'returned'})
        return {'type': 'ir.actions.act_window_close'}
