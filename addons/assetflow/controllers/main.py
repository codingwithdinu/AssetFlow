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

    @http.route('/assetflow/ai/query', type='json', auth='user')
    def ai_query(self, query=''):
        """AI assistant endpoint."""
        if not query:
            return {'response': 'Please provide a query.'}
        response = request.env['assetflow.ai.assist'].process_query(query)
        return {'response': response}
