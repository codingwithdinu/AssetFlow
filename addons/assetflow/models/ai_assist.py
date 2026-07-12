# -*- coding: utf-8 -*-
from odoo import models, fields, api


class AiAssist(models.Model):
    """Simple AI assistant model for asset-related queries."""
    _name = 'assetflow.ai.assist'
    _description = 'AI Assistant Query Log'
    _order = 'create_date desc'

    query = fields.Text(string='User Query', required=True)
    response = fields.Text(string='AI Response')
    user_id = fields.Many2one(
        'res.users',
        string='User',
        default=lambda self: self.env.uid,
        readonly=True,
    )
    query_date = fields.Datetime(
        string='Query Date',
        default=fields.Datetime.now,
        readonly=True,
    )

    @api.model
    def process_query(self, query_text):
        """Simple rule-based AI response for demo."""
        query_lower = query_text.lower()
        Asset = self.env['assetflow.asset']

        response = ''

        if 'available' in query_lower:
            count = Asset.search_count([('state', '=', 'available')])
            response = f'There are currently {count} available assets in the system.'

        elif 'maintenance' in query_lower:
            assets = Asset.search([('state', '=', 'maintenance')])
            names = ', '.join(assets.mapped('name')[:5])
            response = (
                f'{len(assets)} asset(s) are under maintenance. '
                + (f'Recent: {names}' if names else '')
            )

        elif 'allocated' in query_lower or 'assigned' in query_lower:
            count = Asset.search_count([('state', '=', 'allocated')])
            response = f'{count} asset(s) are currently allocated to employees.'

        elif 'total' in query_lower or 'count' in query_lower:
            total = Asset.search_count([])
            response = f'Total assets in AssetFlow: {total}'

        elif 'overdue' in query_lower:
            from datetime import date
            overdue = self.env['assetflow.allocation'].search([
                ('state', '=', 'active'),
                ('expected_return_date', '<', str(date.today())),
            ])
            response = f'There are {len(overdue)} overdue allocation(s).'

        else:
            response = (
                "I can help you with: asset counts, availability, "
                "maintenance status, allocations, and overdue returns. "
                "Try asking: 'How many assets are available?' or "
                "'Show me maintenance assets'."
            )

        self.create({'query': query_text, 'response': response})
        return response
