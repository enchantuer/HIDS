document.addEventListener('DOMContentLoaded', function () {
    attachActionButtonListeners();
    updateUserCounts();

    // Écouteur de soumission du formulaire
    document.getElementById('userForm').addEventListener('submit', async function (e) {
        console.log("Form submitted");
        e.preventDefault();

        const form = e.target;
        const formData = new FormData(form);
        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        // formData.set('is_staff', document.getElementById('is_staff').checked);

        const response = await fetch(ADD_USER_URL, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
            },
            body: formData,
        });

        const data = await response.json();

        if (response.ok) {
            console.log("User added/edited successfully");
            const table = document.querySelector('#userTable tbody');
            let row = table.querySelector(`tr[data-id="${data.id}"]`);

            const rowHTML = `
                <td class="id">${data.id}</td>
                <td class="firstname">${data.firstname}</td>
                <td class="lastname">${data.lastname}</td>
                <td class="email">${data.email}</td>
                <td class="is_staff">${data.is_staff ? "Oui" : "Non"}</td>
                <td class="actions">
                    <div class="dropdown">
                        <p class="dropbtn">
                            <iconify-icon icon="fluent:more-horizontal-32-filled" width="15" height="15"></iconify-icon>
                        </p>
                        <div class="dropdown-content">
                            <a href="#" class="edit-user" data-id="${data.id}">Éditer</a>
                            <a href="#" class="delete-user" data-id="${data.id}">Supprimer</a>
                        </div>
                    </div>
                </td>
            `;

            if (row) {
                row.innerHTML = rowHTML;
            } else {
                row = document.createElement('tr');
                row.setAttribute('data-id', data.id);
                row.setAttribute('data-is-staff', data.is_staff ? "true" : "false");
                row.innerHTML = rowHTML;
                table.appendChild(row);
            }

            form.reset();
            form.dataset.userId = '';
            attachActionButtonListeners();
            updateUserCounts();
            alert(`L'utilisateur a été ${data.action}.`);
        } else {
            alert(data.error || "Erreur lors de l’ajout ou modification de l’utilisateur");
        }
    });
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

// Attache les clics aux boutons d'action
function attachActionButtonListeners() {
    console.log("Attaching action button listeners");
    // Gestion des dropdowns
    const actionButtons = document.querySelectorAll('.dropbtn');
    actionButtons.forEach(button => {
        button.addEventListener('click', function (e) {
            e.stopPropagation();
            this.parentElement.classList.toggle('show');
        });
    });

    // Fermer dropdown si on clique ailleurs
    window.addEventListener('click', function () {
        document.querySelectorAll('.dropdown').forEach(d => d.classList.remove('show'));
    });

    // Édition utilisateur
    const editLinks = document.querySelectorAll('.edit-user');
    editLinks.forEach(link => {
        link.addEventListener('click', function (e) {
            e.preventDefault();
            const row = this.closest('tr');
            const userId = row.dataset.id;
            editUser(row);
        });
    });

    // Suppression utilisateur
    const deleteLinks = document.querySelectorAll('.delete-user');
    deleteLinks.forEach(link => {
        link.addEventListener('click', function (e) {
            e.preventDefault();
            const row = this.closest('tr');
            const userId = row.dataset.id;
            deleteUser(userId, row);
        });
    });
}

// Fonction d'édition d'un utilisateur
function editUser(row) {
    console.log("Editing user");
    const userId = row.dataset.id;
    const firstname = row.querySelector('.firstname').textContent;
    const lastname = row.querySelector('.lastname').textContent;
    const email = row.querySelector('.email').textContent;
    const isStaff = row.dataset.isStaff === "true";

    document.getElementById('firstname').value = firstname;
    document.getElementById('lastname').value = lastname;
    document.getElementById('email').value = email;
    document.getElementById('id').value = userId;
    document.getElementById('is_staff').checked = isStaff;
}

// Fonction de suppression d'un utilisateur
async function deleteUser(userId) {
    console.log("Deleting user");
    if (confirm("Êtes-vous sûr de vouloir supprimer cet utilisateur ?")) {
        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        const response = await fetch(`${DELETE_USER_BASE_URL}${userId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
            },
        });

        const data = await response.json();

        if (response.ok) {
            const row = document.querySelector(`#userTable tr[data-id="${userId}"]`);
            if (row) row.remove();
            updateUserCounts();
            alert("Utilisateur supprimé avec succès.");
        } else {
            alert(data.error || "Erreur lors de la suppression.");
        }
    }
}

