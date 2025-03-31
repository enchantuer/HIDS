const numberOfAlerts = 5

function getAlerts() {
    const params = new URLSearchParams()
    params.append('page_size', numberOfAlerts);

    getFromAPI('/api/alerts', renderAlerts, params)
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

function getStats() {
    getFromAPI('/api/stats', renderStats)
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

getAlerts();
getStats();

const socketStats = new WebSocket("/ws/stats/");
socketStats.onmessage = function (event) {
    console.log('New stats received');
    const stats = JSON.parse(event.data);
    renderStats(stats);
};

const socketAlerts = new WebSocket("/ws/alerts/");
socketAlerts.onmessage = function (event) {
    console.log('New alert received');
    const json = JSON.parse(event.data);
    updateAlerts(json);
};

function updateAlerts(json) {
    if (json.operation === 'create') {
        const alert = json.alert;
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

        if (tableBody.children.length >= numberOfAlerts) {
            tableBody.removeChild(tableBody.lastChild);
        }
        tableBody.insertBefore(row, tableBody.firstChild);
    }
}