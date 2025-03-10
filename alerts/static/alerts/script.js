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