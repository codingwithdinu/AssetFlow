# -*- coding: utf-8 -*-
from odoo import models, fields, api


class AssetFlowDashboard(models.TransientModel):
    """Model to provide KPI data for the dashboard."""
    _name = 'assetflow.dashboard'
    _description = 'AssetFlow Dashboard KPIs'
    _auto = True

    name = fields.Char(string='Name', default='Dashboard')

    @api.model
    def get_kpi_data(self):
        Asset = self.env['assetflow.asset']
        Allocation = self.env['assetflow.allocation']
        Booking = self.env['assetflow.booking']
        Maintenance = self.env['assetflow.maintenance']
        Transfer = self.env['assetflow.transfer']

        return {
            'total_assets': Asset.search_count([]),
            'available': Asset.search_count([('state', '=', 'available')]),
            'allocated': Asset.search_count([('state', '=', 'allocated')]),
            'maintenance': Asset.search_count([('state', '=', 'maintenance')]),
            'retired': Asset.search_count([('state', '=', 'retired')]),
            'pending_allocations': Allocation.search_count([('state', '=', 'draft')]),
            'active_bookings': Booking.search_count([('state', '=', 'confirmed')]),
            'open_maintenance': Maintenance.search_count(
                [('state', 'in', ['reported', 'approved', 'in_progress'])]
            ),
            'pending_transfers': Transfer.search_count(
                [('state', 'in', ['draft', 'submitted'])]
            ),
        }
