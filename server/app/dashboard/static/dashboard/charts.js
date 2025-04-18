// Register the plugin to all charts:
Chart.register(ChartDataLabels);

// Alert Type
const alertType = document.querySelector('#alert-type-chart');
const alertTypeData = JSON.parse(
    document.querySelector('#alert-type-data').textContent
);
const dataAlertType = {
    labels: alertTypeData[0],
    datasets: [{
        label: 'Nombre d\'alertes',
        data: alertTypeData[1],
        backgroundColor: [
            'rgb(241,39,80)',
            'rgb(19,19,32)',
            'rgb(61,132,239)',
            'rgb(246,196,82)'
        ],
        hoverOffset: 4,
    }]
};
const optionsAlertType = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
        legend: {
            display: true,
            position: 'right',
            labels: {
                usePointStyle: true,
            }
        },
        datalabels: {
            anchor: "center",
            align: "center",
            color: 'rgb(251,251,251)',
            font: {
                weight: "bold",
            },
            formatter: (value, ctx) => {
                const dataset = ctx.chart.data.datasets;

                const total = dataset[0].data.reduce((data, total) => total + data);

                return ((value / total) * 100).toFixed(1) + "%";
            },
        },
    }
};
const configAlertType = {
    type: 'doughnut',
    data: dataAlertType,
    options: optionsAlertType
};

new Chart(alertType, configAlertType);

// Agents
const agent = document.querySelector('#agent-chart');
const agentData = JSON.parse(
    document.querySelector('#agent-data').textContent
)
const dataAgent = {
    labels: agentData[0],
    datasets: [
        {
            label: 'Nombre requetes sans alertes',
            data: agentData[1].request_without_alert_per_agent,
            backgroundColor: 'rgb(0,178,255)',
            stack: 'stack'
        },
        {
            label: 'Nombre d\'alertes',
            data: agentData[1].alert_per_agent,
            backgroundColor: 'rgb(255,0,21)',
            stack: 'stack',
            datalabels: {
                labels: {
                    total: {
                        anchor: "end",
                        align: "top",
                        color: 'black',
                        formatter: (value, ctx) => {
                            const dataset = ctx.chart.data.datasets;
                            const dataIndex = ctx.dataIndex;

                            let total = 0;
                            dataset.forEach((ds) => {
                                total += ds.data[dataIndex];
                            });

                            return total;
                        },
                    }
                }
            }
        }
    ]
};

const optionsAgent = {
    responsive: true,
    maintainAspectRatio: false,
    scales: {
        x: {
            stacked: true
        }
    },
    plugins: {
        legend: {
            display: true,
            position: 'top',
            align: 'end',
            labels: {
                usePointStyle: true
            }
        },
        datalabels: {
            anchor: "center",
            align: "center",
            color: 'rgb(251,251,251)',
            font: {
                weight: "bold",
            },
            labels: {
                percent: {
                    formatter: (value, ctx) => {
                        if(value === 0) return "";

                        const dataset = ctx.chart.data.datasets;
                        const dataIndex = ctx.dataIndex;

                        let total = 0;
                        dataset.forEach((ds) => {
                            total += ds.data[dataIndex];
                        });

                        return ((value / total) * 100).toFixed(1) + "%";
                    }
                }
            }
        },
    }
};

const configAgent = {
    type: 'bar',
    data: dataAgent,
    options: optionsAgent
};

new Chart(agent, configAgent);

// IA stats
const IA = document.querySelector('#ia-stats-chart');
const IAData = JSON.parse(
    document.querySelector('#ia-data').textContent
)
const dataIA = {
  labels: [
    'BotNet',
    'DOS 1',
    'DOS 2',
    'DDOS 2',
    'DDOS 1',
    'BruteForce',
    'Phishing'
  ],
  datasets: [{
    label: IAData[0].name,
    data: IAData[0].data,
    fill: true,
    backgroundColor: 'rgba(255, 99, 132, 0.2)',
    borderColor: 'rgb(255, 99, 132)',
    pointBackgroundColor: 'rgb(255, 99, 132)',
    pointBorderColor: '#fff',
    pointHoverBackgroundColor: '#fff',
    pointHoverBorderColor: 'rgb(255, 99, 132)'
  }, {
    label: IAData[1].name,
    data: IAData[1].data,
    fill: true,
    backgroundColor: 'rgba(54, 162, 235, 0.2)',
    borderColor: 'rgb(54, 162, 235)',
    pointBackgroundColor: 'rgb(54, 162, 235)',
    pointBorderColor: '#fff',
    pointHoverBackgroundColor: '#fff',
    pointHoverBorderColor: 'rgb(54, 162, 235)'
  }]
};

const optionsIA = {
    responsive: true,
    maintainAspectRatio: false,
    elements: {
        line: {
            borderWidth: 3
        }
    },
    plugins: {
        legend: {
            display: true,
            position: 'bottom',
            align: 'center',
            labels: {
                usePointStyle: true
            }
        },
    }
};

const configIA = {
  type: 'radar',
  data: dataIA,
  options: optionsIA,
};

new Chart(IA, configIA);

// Alerts evolution
const alertEvolution = document.querySelector('#alert-evolution-chart');
const alertEvolutionData = JSON.parse(
    document.querySelector('#alert-evolution-data').textContent
)
const labels = alertEvolutionData[0].map(hour => new Date(hour).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }))
console.log(labels)
const dataAlertEvolution = {
    labels: labels,
    datasets: [{
        label: "Nombre d'alertes",
        data: alertEvolutionData[1],
        borderColor: 'red',  // Ligne rouge
        fill: true,
        tension: 0.3,  // Effet courbe
        borderWidth: 2, // Épaisseur de la ligne
        pointRadius: 3, // Taille des points
        pointBackgroundColor: 'red', // Couleur des points
        pointHoverRadius: 5 // Taille des points au survol
    }]
};

// Options du graphique
const optionsAlertEvolution = {
    responsive: true,
    maintainAspectRatio: false,
    scales: {
        x: {
            grid: {
                drawBorder: false
            }
        },
        y: {
            grid: {
                drawBorder: false
            },
            suggestedMin: 0,
            suggestedMax: 10
        }
    },
    plugins: {
        legend: {
            display: true,
            position: 'top',
            align: 'end',
            labels: {
                usePointStyle: true
            }
        },
    }
};

// Création du graphique avec un callback pour définir le gradient dynamiquement
new Chart(alertEvolution, {
    type: 'line',
    data: dataAlertEvolution,
    options: optionsAlertEvolution,
    plugins: [{
        id: 'customGradient',
        beforeDraw: (chartInstance) => {
            const max = Math.max(...dataAlertEvolution.datasets[0].data)
            const min = Math.min(...dataAlertEvolution.datasets[0].data)

            if(max === 0) {
                return;
            }

            const ctx = chartInstance.ctx;
            const chartArea = chartInstance.chartArea;
            // Trouver la hauteur dynamique du plus haut et plus bas point de la courbe
            const yAxis = chartInstance.scales.y;
            const topY = yAxis.getPixelForValue(max); // Point le plus haut
            const bottomY = yAxis.getPixelForValue(min); // Point le plus haut
            const stopPosition = (bottomY - topY) / (chartArea.bottom - topY);
            // Créer un gradient ajusté à la courbe
            const gradient = ctx.createLinearGradient(0, topY, 0, chartArea.bottom);
            gradient.addColorStop(0, 'rgba(255, 0, 0, 0.5)'); // Rouge semi-transparent en haut de la courbe
            gradient.addColorStop(stopPosition, 'rgba(255, 0, 0, 0.05)'); // Rouge Grandement transparent au point le plus bas de la courbe
            gradient.addColorStop(1, 'rgba(255, 0, 0, 0)'); // Complètement transparent en bas
            // Appliquer le gradient comme backgroundColor
            chartInstance.data.datasets[0].backgroundColor = gradient;
            chartInstance.update(); // Forcer le rafraîchissement
        }
    }]
});

