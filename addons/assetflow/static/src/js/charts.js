/** @odoo-module **/
// AssetFlow Charts – Chart.js integration

let chartInstance = {
    department: null,
    category: null,
};

const COLORS = [
    '#4e73df', '#1cc88a', '#36b9cc', '#f6c23e', '#e74a3b',
    '#5a5c69', '#858796', '#6610f2', '#fd7e14', '#20c9a6'
];

export function renderBarChart(canvasId, labels, data, label, color = COLORS) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;

    // Destroy previous chart
    const chartKey = canvasId === 'chart-department' ? 'department' : 'category';
    if (chartInstance[chartKey]) {
        chartInstance[chartKey].destroy();
    }

    chartInstance[chartKey] = new Chart(ctx.getContext('2d'), {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: label,
                data: data,
                backgroundColor: COLORS.slice(0, labels.length),
                borderColor: COLORS.slice(0, labels.length),
                borderWidth: 1,
                borderRadius: 4,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: { stepSize: 1 }
                }
            }
        }
    });
}

export function renderPieChart(canvasId, labels, data, label) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;

    const chartKey = canvasId === 'chart-department' ? 'department' : 'category';
    if (chartInstance[chartKey]) {
        chartInstance[chartKey].destroy();
    }

    chartInstance[chartKey] = new Chart(ctx.getContext('2d'), {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: data,
                backgroundColor: ['#4e73df', '#1cc88a', '#36b9cc', '#f6c23e', '#e74a3b', '#5a5c69'],
                hoverOffset: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: { boxWidth: 12, padding: 12 }
                }
            }
        }
    });
}