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