# -*- coding: utf-8 -*-
from odoo import models, fields, api


class AssetFlowDashboard(models.Model):
    """Model to provide KPI data for the dashboard."""
    _name = 'assetflow.dashboard'
    _description = 'AssetFlow Dashboard KPIs'
    _auto = False  # No database table - virtual model

    total_assets = fields.Integer(string='Total Assets')
    available = fields.Integer(string='Available')
    allocated = fields.Integer(string='Allocated')
    maintenance = fields.Integer(string='Under Maintenance')
    retired = fields.Integer(string='Retired')
    pending_allocations = fields.Integer(string='Pending Allocations')
    active_bookings = fields.Integer(string='Active Bookings')
    open_maintenance = fields.Integer(string='Open Maintenance')
    pending_transfers = fields.Integer(string='Pending Transfers')

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

    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        res.update(self.get_kpi_data())
        return res
