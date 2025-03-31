async function getFromAPI(path, callback, params = new URLSearchParams()) {
    try {
        const response = await fetch(`${path}?${params}`)
        if (!checkResponse(response)) throw new Error("Could not fetch response from API");
        callback(await response.json());
    } catch (e) {
        console.log(e)
    }
}
function checkResponse(response) {
    return response && response.status === 200;
}

function getAlerts(params = new URLSearchParams()) {
    getFromAPI('/api/alerts', renderAlerts, params)
}
function getStats() {
    getFromAPI('/api/stats', renderStats)
}

// Fonction pour formater la date correctement (ISO sans 'Z')
function formatDate(dateString) {
    if (!dateString) return ""; // Éviter les erreurs si l'entrée est vide
    const date = new Date(dateString); // Convertir en objet Date
    return date.toISOString().slice(0, -1); // Enlever le 'Z' pour rester en UTC
}
function parseISODate(isoString) {
    if (!isoString) return "";
    const date = new Date(isoString);
    return date.toLocaleString(); // Format selon la locale de l'utilisateur
}

function renderAlerts(json) {
    if (json.alerts === undefined) throw new Error("Response from server is not normal");

    const tableBody = document.querySelector('#alerts tbody');
    tableBody.innerHTML = '';

    json.alerts.forEach(alert => {
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

        // Ajouter la ligne au tbody
        tableBody.appendChild(row);
    });
}
function renderStats(json) {
    console.log(json)
    if (json.alerts_count === undefined || json.agents_count === undefined || json.agents_down_count === undefined) throw new Error("Response from server is not normal");
    const statsSpan = document.querySelectorAll('.stats > span');
    statsSpan.forEach((el) => {
        switch (el.id) {
            case "nb-alerts": el.textContent = json.alerts_count; break;
            case "nb-agents": el.textContent = json.agents_count; break;
            case "nb-agents-down": el.textContent = json.agents_down_count; break;
        }
    })
}