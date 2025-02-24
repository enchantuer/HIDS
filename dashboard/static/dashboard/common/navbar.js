// Navbar buttons
const navbarDashboard = document.querySelector('.navbar-Dashboard');
const navbarButtons = document.querySelectorAll('.navbar-onglets-bloc');
const pageNow = navbarDashboard

navbarButtons.forEach(button => {
        button.addEventListener('mousedown', function () {
            // Appliquer le style actif au bouton cliqué
            this.style.backgroundColor = "white";
            this.style.color = "black";
            location.reload();

            console.log(this.textContent.trim() + " sélectionné !");
        });

        button.addEventListener('mouseover', function () {
            this.style.backgroundColor = "#1E5EBC";
            this.style.color = "white";
        });

        button.addEventListener('mouseout', function () {
            if (this !== pageNow) {
                this.style.backgroundColor = "#f0f0f0";
                this.style.color = "black";
            }else {
                this.style.backgroundColor = "#3585F9";
                this.style.color = "white";
            }

        });
    });

// Navbar burger
const navbarBurger = document.querySelector('.navbar-burger');
const dropdownMenu = document.querySelector('.dropdown-menu');

navbarBurger.addEventListener('click', function () {
    dropdownMenu.classList.toggle('dropdown-active');
});

// Close dropdown when clicking outside
document.addEventListener('click', function (event) {
    if (!navbarBurger.contains(event.target) && !dropdownMenu.contains(event.target)) {
        dropdownMenu.classList.remove('dropdown-active');
    }
});