const numberOfAlerts = "5"

const params = new URLSearchParams()
params.append('page_size', numberOfAlerts);
getAlerts(params);
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