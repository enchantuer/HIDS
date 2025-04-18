document.addEventListener('DOMContentLoaded', function() {
    const switches = document.querySelectorAll('input[type="checkbox"]');

    switches.forEach(function(switchEl) {
        switchEl.addEventListener('change', function() {
            console.log(`Switch ${switchEl.id} is now ${switchEl.checked ? 'ON' : 'OFF'}`);

        });
    });
});

// IA stats
const IA = document.querySelector('#ia-stats-chart');
const IAData = JSON.parse(
    document.querySelector('#ia-data').textContent
)
console.log(IAData)
const dataIA = {
  labels: IAData.labels,
  datasets: [{
    label: IAData.data[0].name,
    data: IAData.data[0].data,
    fill: true,
    backgroundColor: 'rgba(255, 99, 132, 0.2)',
    borderColor: 'rgb(255, 99, 132)',
    pointBackgroundColor: 'rgb(255, 99, 132)',
    pointBorderColor: '#fff',
    pointHoverBackgroundColor: '#fff',
    pointHoverBorderColor: 'rgb(255, 99, 132)'
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