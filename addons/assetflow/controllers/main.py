# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import json


class AssetFlowController(http.Controller):

    @http.route('/assetflow/dashboard/kpi', type='json', auth='user')
    def get_dashboard_kpi(self):
        """Returns KPI data for the dashboard."""
        data = request.env['assetflow.dashboard'].get_kpi_data()
        return data

    @http.route('/assetflow/dashboard/recent_assets', type='json', auth='user')
    def get_recent_assets(self):
        """Returns recent 10 assets for dashboard."""
        assets = request.env['assetflow.asset'].search([], limit=10, order='create_date desc')
        return [{
            'id': a.id,
            'asset_tag': a.asset_tag,
            'name': a.name,
            'category_name': a.category_id.name or '',
            'state': a.state,
            'employee_name': a.employee_id.name or '',
        } for a in assets]

    @http.route('/assetflow/ai/query', type='json', auth='user')
    def ai_query(self, query=''):
        """AI assistant endpoint."""
        if not query:
            return {'response': 'Please provide a query.'}
        response = request.env['assetflow.ai.assist'].process_query(query)
        return {'response': response}
