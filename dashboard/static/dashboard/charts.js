// Register the plugin to all charts:
Chart.register(ChartDataLabels);

// Alert Type
const alertType = document.querySelector('#alert-type-chart');

const dataAlertType = {
    labels: [
        'Brute Force',
        'SSH',
        'DDOS',
        'BotNet'
    ],
    datasets: [{
        label: 'Nombre d\'alertes',
        data: [30, 30, 10, 30],
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

const dataAgent = {
    labels: [
        '1',
        '10',
        '11',
        '4',
        '10',
        '44',
        '50',
        '1',
        '10',
        '11',
        '4',
        '10',
        '44'
    ],
    datasets: [
        {
            label: 'Nombre requetes sans alertes',
            data: [40, 100, 45, 30, 60, 130, 39, 50, 90, 100, 34, 60, 110],
            backgroundColor: 'rgb(0,178,255)',
            stack: 'stack'
        },
        {
            label: 'Nombre d\'alertes',
            data: [30, 30, 10, 30, 40, 119, 4, 30, 30, 10, 30, 40, 100],
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
    label: 'Model 1',
    data: [65, 59, 90, 81, 56, 55, 40],
    fill: true,
    backgroundColor: 'rgba(255, 99, 132, 0.2)',
    borderColor: 'rgb(255, 99, 132)',
    pointBackgroundColor: 'rgb(255, 99, 132)',
    pointBorderColor: '#fff',
    pointHoverBackgroundColor: '#fff',
    pointHoverBorderColor: 'rgb(255, 99, 132)'
  }, {
    label: 'Model 2',
    data: [28, 48, 40, 19, 96, 27, 100],
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

/*
// Alerts evolution
const alertEvolution = document.querySelector('#alert-evolution-chart');

const ctx = alertEvolution.getContext("2d");
// Création du gradient
const gradient = ctx.createLinearGradient(0, 0, 0, alertEvolution.height);
gradient.addColorStop(0, 'rgba(255, 99, 132, 1)');  // Couleur en haut (plus intense)
gradient.addColorStop(1, 'rgba(255, 99, 132, 0)');    // Couleur en bas (transparent)

const dataAlertEvolution = {
    labels: ["12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00"],
    datasets: [{
        label: "Nombre d'alertes",
        data: [30, 30, 10, 30, 40, 40, 30],
        borderColor: 'red',
        backgroundColor: gradient,
        fill: true,
        tension: 0.3
    }]
};

const optionsAlertEvolution = {
    scales: {
        y: {
            suggestedMin: 0,
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

const configAlertEvolution = {
    type: 'line',
    data: dataAlertEvolution,
    options: optionsAlertEvolution
};

new Chart(alertEvolution, configAlertEvolution);*/

// Sélection du canvas
const alertEvolution = document.querySelector('#alert-evolution-chart');

// Configuration des données
const dataAlertEvolution = {
    labels: ["12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00"],
    datasets: [{
        label: "Nombre d'alertes",
        data: [100, 80, 60, 90, 40, 70, 80],
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
            suggestedMax: 200
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
            const ctx = chartInstance.ctx;
            const chartArea = chartInstance.chartArea;
            // Trouver la hauteur dynamique du plus haut et plus bas point de la courbe
            const yAxis = chartInstance.scales.y;
            const topY = yAxis.getPixelForValue(Math.max(...dataAlertEvolution.datasets[0].data)); // Point le plus haut
            const bottomY = yAxis.getPixelForValue(Math.min(...dataAlertEvolution.datasets[0].data)); // Point le plus haut
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

