const dropdownBtn = document.querySelector(".dropdown-button");
const dropdown = document.querySelector(".dropdown");

dropdownBtn.addEventListener("click", function (e) {
    e.preventDefault();
    dropdown.classList.toggle("active");
});

// Fermer le dropdown si on clique en dehors
document.addEventListener("click", function (event) {
    if (!dropdown.contains(event.target)) {
        dropdown.classList.remove("active");
    }
});

document.addEventListener('focusin', (event) => {
  // Vérifie si l'élément focusé est un input
  if (event.target.classList.contains('field-input')) {
    // Ajoute la classe 'focused' à la div.parent (la div.field)
    event.target.closest('.field')?.classList.add('active');
  }
});

document.addEventListener('focusout', (event) => {
  // Vérifie si l'élément qui a perdu le focus est un input
  if (event.target.classList.contains('field-input')) {
    // Retire la classe 'focused' de la div.parent (la div.field)
    event.target.closest('.field')?.classList.remove('active');
  }
});

const form = document.querySelector('.search');

function getAlerts(params = new URLSearchParams()) {
    getFromAPI('/api/alerts', renderAlerts, params)
}

async function renderAlerts(json) {
    if (json.alerts === undefined) throw new Error("Response from server is not normal");

    const tableBody = document.querySelector('#alerts tbody');
    tableBody.innerHTML = '';

    json.alerts.forEach(alert => {
        const row = document.createElement('tr');

        row.innerHTML = `
            <td class="align-left">${alert.created_at}</td>
            <td>${alert.agent__id}</td>
            <td>${alert.agent__name}</td>
            <td>${alert.source}</td>
            <td>${alert.type}</td>
            <td>${alert.description}</td>
            <td>${alert.level}</td>
            <td>${alert.id}</td>
        `;

        // Ajouter la ligne au tbody
        tableBody.appendChild(row);
    });
}
function getAlertsFromFormEvent(event) {
    event.preventDefault();
    // Utiliser FormData pour récupérer les données du formulaire
    const formData = new FormData(form); // event.target fait référence au formulaire
    const params = new URLSearchParams();

    // Convertir les données du FormData en paramètres d'URL
    formData.forEach((value, key) => {
        if (Array.isArray(value)) {
            // Si la donnée est un tableau (par exemple pour les checkboxes), on les ajoute séparés par une virgule
            params.append(key, value.join(','));
        } else {
            // Sinon, on les ajoute normalement
            params.append(key, value);
        }
    });
    getAlerts(params);
}

document.querySelector('.search').addEventListener('submit', getAlertsFromFormEvent);
getAlerts();

const socketAlerts = new WebSocket("/ws/alerts/");
socketAlerts.onmessage = function (event) {
    console.log('New alert received');
    const json = JSON.parse(event.data);
    console.log(json)
    if (alertMatchesFilters(json.alert)) updateAlerts(json);
};

function alertMatchesFilters(alert) {
    const formData = new FormData(form);

    // Récupérer les valeurs du formulaire
    const searchType = formData.get("type").toLowerCase().trim();
    const startDate = formData.get("start_date");
    const endDate = formData.get("end_date");
    const selectedSources = formData.getAll('source');

    // Vérification du type (recherche textuelle)
    if (searchType && !alert.type.toLowerCase().includes(searchType)) {
        return false;
    }

    // Vérification des dates
    const alertDate = new Date(alert.created_at);
    if (startDate && alertDate < new Date(startDate)) {
        return false;
    }
    if (endDate && alertDate > new Date(endDate)) {
        return false;
    }

    // Vérification des sources
    if (selectedSources.length > 0 && !selectedSources.includes(alert.source)) {
        return false;
    }

    return true;
}

function updateAlerts(json) {
    const alert = json.alert;
    if (json.operation === 'create') {
        const tableBody = document.querySelector('#alerts tbody');
        const row = document.createElement('tr');

        row.innerHTML = `
            <td class="align-left">${parseISODate(alert.created_at)}</td>
            <td>${alert.agent__id}</td>
            <td>${alert.agent__name}</td>
            <td>${alert.source}</td>
            <td>${alert.type}</td>
            <td>${alert.description}</td>
            <td>${alert.level}</td>
            <td>${alert.id}</td>
        `;
        tableBody.insertBefore(row, tableBody.firstChild);
    }
}