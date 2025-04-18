document.addEventListener('DOMContentLoaded', function () {
    attachAgentActionListeners();
    updateAgentCounts();

    document.getElementById('agentForm').addEventListener('submit', async function (e) {
        e.preventDefault();
        const form = e.target;
        const formData = new FormData(form);
        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        const response = await fetch(ADD_AGENT_URL, {
            method: 'POST',
            headers: { 'X-CSRFToken': csrftoken },
            body: formData
        });

        const data = await response.json();

        if (response.ok) {
            const table = document.querySelector('#agentTable tbody');
            let row = table.querySelector(`tr[data-id="${data.id}"]`);

            const rowHTML = `
                <td>${data.id}</td>
                <td class="name">${data.name}</td>
                <td class="system">${data.system}</td>
                <td class="adresse">${data.adresse}</td>
                <td class="statut">${data.down ? "Non" : "Oui"}</td>
                <td>
                    <a href="#" class="edit-agent" data-id="${data.id}">Éditer</a> |
                    <a href="#" class="delete-agent" data-id="${data.id}">Supprimer</a>
                </td>
            `;

            if (row) {
                row.innerHTML = rowHTML;
            } else {
                row = document.createElement('tr');
                row.setAttribute('data-id', data.id);
                row.setAttribute('data-statut', data.down ? "true" : "false");
                row.innerHTML = rowHTML;
                table.appendChild(row);
            }

            form.reset();
            form.dataset.agentId = '';
            attachAgentActionListeners();
            updateAgentCounts();
            alert(`Agent ${data.action} avec succès.`);
        } else {
            alert(data.error || "Erreur lors de l’ajout/modification de l’agent.");
        }
    });
});

function updateAgentCounts() {
    fetch('/admin_panel/get_agent_counts/')
        .then(response => response.json())
        .then(data => {
            document.getElementById('actifCount').textContent = data.actifCount;
            document.getElementById('inactifCount').textContent = data.inactifCount;
            console.log("Response: ", data);
        });


}

function attachAgentActionListeners() {
    document.querySelectorAll('.edit-agent').forEach(link => {
        link.addEventListener('click', function (e) {
            e.preventDefault();
            const row = this.closest('tr');
            document.getElementById('name').value = row.querySelector('.name').textContent;
            document.getElementById('system').value = row.querySelector('.system').textContent;
            document.getElementById('adresse').value = row.querySelector('.adresse').textContent;
            document.getElementById('is_up').checked = row.dataset.statut === "true";
            document.getElementById('id').value = row.dataset.id;
        });
    });

    document.querySelectorAll('.delete-agent').forEach(link => {
        link.addEventListener('click', async function (e) {
            e.preventDefault();
            const row = this.closest('tr');
            const agentId = row.dataset.id;
            if (confirm("Supprimer cet agent ?")) {
                const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
                const response = await fetch(`${DELETE_AGENT_BASE_URL}${agentId}/`, {
                    method: 'POST',
                    headers: { 'X-CSRFToken': csrftoken }
                });
                if (response.ok) {
                    row.remove();
                    updateAgentCounts();
                    alert("Agent supprimé.");
                } else {
                    const data = await response.json();
                    alert(data.error || "Erreur lors de la suppression.");
                }
            }
        });
    });
}