/** @odoo-module **/
// AssetFlow Dashboard – Client Action

import { registry } from "@web/core/registry";
import { Component, onWillStart, useState, useRef, onMounted } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { loadJs } from "@web/core/assets";

const { DateTime } = luxon;

class AssetFlowDashboard extends Component {
    static template = "assetflow.DashboardView";

    setup() {
        this.rpc = useService("rpc");
        this.state = useState({
            loading: true,
            kpi: {},
            recentAssets: [],
        });
        this.chartsLoaded = false;

        onWillStart(async () => {
            await this.loadCharts();
            await this.fetchData();
        });
    }

    async loadCharts() {
        try {
            await loadJs("/web/static/lib/Chart/Chart.js");
            this.chartsLoaded = true;
        } catch (e) {
            console.warn("Chart.js not available:", e);
        }
    }

    async fetchData() {
        try {
            // Fetch KPI Data
            const kpi = await this.rpc("/assetflow/dashboard/kpi", {});

            // Fetch recent 10 assets
            const recentAssets = await this.rpc("/assetflow/dashboard/recent_assets", {});

            this.state.kpi = kpi;
            this.state.recentAssets = recentAssets || [];
            this.state.loading = false;

            // Use nextTick to ensure DOM is rendered
            await this.renderDashboard();
        } catch (e) {
            console.error("Dashboard fetch error:", e);
            this.state.loading = false;
        }
    }

    async renderDashboard() {
        const kpi = this.state.kpi;
        if (!kpi) return;

        // Update KPI Cards
        document.getElementById("kpi-total-assets").textContent = kpi.total_assets || 0;
        document.getElementById("kpi-available").textContent = kpi.available || 0;
        document.getElementById("kpi-allocated").textContent = kpi.allocated || 0;
        document.getElementById("kpi-maintenance").textContent = kpi.maintenance || 0;
        document.getElementById("kpi-retired").textContent = kpi.retired || 0;
        document.getElementById("kpi-pending-alloc").textContent = kpi.pending_allocations || 0;
        document.getElementById("kpi-active-bookings").textContent = kpi.active_bookings || 0;
        document.getElementById("kpi-open-maint").textContent = kpi.open_maintenance || 0;
        document.getElementById("kpi-pending-transfers").textContent = kpi.pending_transfers || 0;

        // Show content, hide spinner
        document.getElementById("assetflow-dashboard-loading").style.display = "none";
        document.getElementById("assetflow-dashboard-content").style.display = "block";

        // Render Charts if Chart.js loaded
        if (this.chartsLoaded) {
            this.renderCharts(kpi);
        }

        // Render Recent Assets
        this.renderRecentAssets();
    }

    renderCharts(kpi) {
        const { renderBarChart, renderPieChart } = require("assetflow.charts");

        // Department Chart
        if (kpi.dept_data && kpi.dept_data.length > 0) {
            const deptLabels = kpi.dept_data.map(d => d.name);
            const deptCounts = kpi.dept_data.map(d => d.count);
            renderBarChart("chart-department", deptLabels, deptCounts, "Assets by Department");
        }

        // Category Chart
        if (kpi.cat_data && kpi.cat_data.length > 0) {
            const catLabels = kpi.cat_data.map(c => c.name);
            const catCounts = kpi.cat_data.map(c => c.count);
            renderPieChart("chart-category", catLabels, catCounts, "Assets by Category");
        }
    }

    renderRecentAssets() {
        const tbody = document.getElementById("recent-assets-body");
        if (!tbody) return;

        const assets = this.state.recentAssets;
        if (assets.length === 0) {
            tbody.innerHTML = '<tr><td colspan="4" class="text-muted text-center">No assets found</td></tr>';
            return;
        }

        const statusBadge = (state) => {
            const colors = {
                available: "badge bg-success",
                allocated: "badge bg-info",
                maintenance: "badge bg-warning text-dark",
                retired: "badge bg-secondary",
                lost: "badge bg-danger",
            };
            return `<span class="${colors[state] || 'badge bg-light text-dark'}">${state}</span>`;
        };

        tbody.innerHTML = assets.map(asset =>
            `<tr>
                <td>${asset.asset_tag || '-'}</td>
                <td>${asset.name || '-'}</td>
                <td>${asset.category_name || '-'}</td>
                <td>${statusBadge(asset.state)}</td>
            </tr>`
        ).join("");
    }
}

registry.category("actions").add("assetflow.action_dashboard", AssetFlowDashboard);