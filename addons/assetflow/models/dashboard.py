# -*- coding: utf-8 -*-
from odoo import models, fields, api


class AssetFlowDashboard(models.Model):
    """Transient model to provide KPI data for the dashboard."""
    _name = 'assetflow.dashboard'
    _description = 'AssetFlow Dashboard KPIs'

    @api.model
    def get_kpi_data(self):
        Asset = self.env['assetflow.asset']
        Allocation = self.env['assetflow.allocation']
        Booking = self.env['assetflow.booking']
        Maintenance = self.env['assetflow.maintenance']
        Transfer = self.env['assetflow.transfer']

        total_assets = Asset.search_count([])
        available = Asset.search_count([('state', '=', 'available')])
        allocated = Asset.search_count([('state', '=', 'allocated')])
        maintenance = Asset.search_count([('state', '=', 'maintenance')])
        retired = Asset.search_count([('state', '=', 'retired')])

        pending_allocations = Allocation.search_count([('state', '=', 'draft')])
        active_bookings = Booking.search_count([('state', '=', 'confirmed')])
        open_maintenance = Maintenance.search_count(
            [('state', 'in', ['reported', 'approved', 'in_progress'])]
        )
        pending_transfers = Transfer.search_count(
            [('state', 'in', ['draft', 'submitted'])]
        )

        # Assets by department
        dept_data = []
        for dept in self.env['assetflow.department'].search([]):
            count = Asset.search_count([('department_id', '=', dept.id)])
            if count:
                dept_data.append({'name': dept.name, 'count': count})

        # Assets by category
        cat_data = []
        for cat in self.env['assetflow.category'].search([]):
            count = Asset.search_count([('category_id', '=', cat.id)])
            if count:
                cat_data.append({'name': cat.name, 'count': count})

        return {
            'total_assets': total_assets,
            'available': available,
            'allocated': allocated,
            'maintenance': maintenance,
            'retired': retired,
            'pending_allocations': pending_allocations,
            'active_bookings': active_bookings,
            'open_maintenance': open_maintenance,
            'pending_transfers': pending_transfers,
            'dept_data': dept_data,
            'cat_data': cat_data,
        }
