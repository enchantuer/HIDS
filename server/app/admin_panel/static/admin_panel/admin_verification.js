document.addEventListener('DOMContentLoaded', function () {
    const switches = document.querySelectorAll('input[type="checkbox"]');

    switches.forEach(function (switchEl) {
        switchEl.addEventListener('change', async function () {
            const editKey = switchEl.id;
            const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            console.log(`Switch ${editKey} is now ${switchEl.checked ? 'ON' : 'OFF'}`);
            const formData = new FormData();
            formData.append('editKey', editKey);

            fetch(UPDATE_CONFIG, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken,
                },
                body: formData,
            });

        });
    });
});

document.addEventListener("DOMContentLoaded", () => {
    fetch(GET_CONFIG)
        .then(response => response.json())
        .then(config => {
            console.log("Config reçue :", config);

            const mapping = {
                YARA: 'yara',
                SURICATA: 'suricata',
                SNORT: 'snort',
                VIRUS_TOTAL: 'virustotal',
                IPDB: 'ipdb',
                IA: 'ope',
                RANDOM_FOREST: 'modele1',
                SUPPORT_VECTOR_MACHINE: 'modele2'
            };

            for (const [configKey, switchId] of Object.entries(mapping)) {
                const checkbox = document.getElementById(switchId);
                if (checkbox) {
                    checkbox.checked = !!config[configKey]; // Assure que c'est bien un booléen
                }
            }
        })
        .catch(error => {
            console.error("Erreur lors du chargement de la config :", error);
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