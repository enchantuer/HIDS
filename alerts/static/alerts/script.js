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

async function getFromAPI(path, callback, params = new URLSearchParams()) {
    try {
        const response = await fetch(`${path}?${params}`)
        if (!checkResponse(response)) throw new Error("Could not fetch response from API");
        callback(await response.json());
    } catch (e) {
        console.log(e)
    }
}

function checkResponse (response) {
    return response && response.status === 200;
}

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
    const formData = new FormData(event.target); // event.target fait référence au formulaire
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