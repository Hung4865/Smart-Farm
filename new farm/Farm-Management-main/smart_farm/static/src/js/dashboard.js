// Smart Farm Dashboard JS
document.addEventListener("DOMContentLoaded", function() {
    var dataElement = document.getElementById('sf-chart-data');
    if (dataElement) {
        try {
            var rawData = dataElement.getAttribute('data-chart');
            var chartData = JSON.parse(rawData);
            
            if (chartData.labels && chartData.labels.length > 0) {
                var ctx = document.getElementById('historyChart').getContext('2d');
                new Chart(ctx, {
                    type: 'line',
                    data: {
                        labels: chartData.labels,
                        datasets: [
                            {
                                label: 'Nhiệt độ (°C)',
                                data: chartData.temps,
                                borderColor: '#ff6b6b',
                                backgroundColor: 'rgba(255, 107, 107, 0.1)',
                                yAxisID: 'y',
                                tension: 0.4,
                                fill: true
                            },
                            {
                                label: 'Độ ẩm (%)',
                                data: chartData.hums,
                                borderColor: '#4dabf7',
                                backgroundColor: 'rgba(77, 171, 247, 0.1)',
                                yAxisID: 'y1',
                                tension: 0.4,
                                fill: true
                            }
                        ]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        interaction: {
                            mode: 'index',
                            intersect: false,
                        },
                        scales: {
                            y: {
                                type: 'linear',
                                display: true,
                                position: 'left',
                                title: {
                                    display: true,
                                    text: 'Nhiệt độ (°C)'
                                }
                            },
                            y1: {
                                type: 'linear',
                                display: true,
                                position: 'right',
                                title: {
                                    display: true,
                                    text: 'Độ ẩm (%)'
                                },
                                grid: {
                                    drawOnChartArea: false,
                                }
                            }
                        },
                        plugins: {
                            legend: {
                                position: 'top',
                            }
                        }
                    }
                });
            }
        } catch (e) {
            console.error("Error parsing chart data: ", e);
        }
    }
});