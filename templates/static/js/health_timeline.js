// static/js/health_timeline.js
class HealthTimeline {
    constructor(userId) {
        this.userId = userId;
        this.initChart();
    }
    
    initChart() {
        this.chart = new Chart(document.getElementById('health-timeline'), {
            type: 'line',
            data: {
                datasets: [
                    {
                        label: 'Health Score',
                        data: [],
                        borderColor: '#22c55e',
                        tension: 0.4
                    },
                    {
                        label: 'Sleep Hours',
                        data: [],
                        borderColor: '#3b82f6',
                        tension: 0.4
                    },
                    {
                        label: 'Stress Level',
                        data: [],
                        borderColor: '#ef4444',
                        tension: 0.4
                    }
                ]
            },
            options: {
                responsive: true,
                plugins: {
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return `${context.dataset.label}: ${context.parsed.y}`;
                            }
                        }
                    }
                }
            }
        });
        
        this.loadData();
    }
}