// static/js/health_radar.js
function createHealthRadar(scores) {
    const ctx = document.getElementById('health-radar').getContext('2d');
    
    const data = {
        labels: ['Sleep', 'Activity', 'Nutrition', 'Mental', 'Cardio', 'Overall'],
        datasets: [{
            label: 'Your Health',
            data: scores,
            backgroundColor: 'rgba(34, 197, 94, 0.2)',
            borderColor: '#22c55e',
            pointBackgroundColor: '#22c55e'
        }, {
            label: 'Optimal',
            data: [100, 100, 100, 100, 100, 100],
            backgroundColor: 'rgba(59, 130, 246, 0.1)',
            borderColor: '#3b82f6',
            pointBackgroundColor: '#3b82f6'
        }]
    };
    
    new Chart(ctx, {
        type: 'radar',
        data: data,
        options: {
            scales: {
                r: {
                    beginAtZero: true,
                    max: 100,
                    ticks: {
                        stepSize: 20
                    }
                }
            }
        }
    });
}