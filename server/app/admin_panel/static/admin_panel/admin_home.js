document.addEventListener('DOMContentLoaded', function () {
    updateUserCounts();
    updateAgentCounts();
});

// Met à jour le compteur d'admins et non-admins
function updateUserCounts() {
    console.log("Updating user counts");

    // Effectuer la requête AJAX pour récupérer les comptes depuis la base de données
    fetch('/admin_panel/get_user_counts/')
        .then(response => response.json())
        .then(data => {
            // Mettre à jour les compteurs avec les données de la réponse
            document.getElementById('adminCount').textContent = data.adminCount;
            document.getElementById('userCount').textContent = data.userCount;
        })
        .catch(error => {
            console.error('Error fetching user counts:', error);
        });
}

function updateAgentCounts() {
    console.log("Updating agent counts");

    fetch('/api/stats/')
        .then(response => response.json())
        .then(data => {
            document.getElementById('agentCount').textContent = data.agents_count;
            document.getElementById('agentDownCount').textContent = data.agents_down_count;
    })
}
