document.addEventListener('DOMContentLoaded', function () {
    updateUserCounts();
});

// Met à jour le compteur d'admins et non-admins
function updateUserCounts() {
    console.log("Updating user counts");

    // Effectuer la requête AJAX pour récupérer les comptes depuis la base de données
    fetch('get_user_counts/')
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

