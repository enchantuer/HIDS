document.addEventListener("DOMContentLoaded", function () {
    const tabs = document.querySelectorAll(".navbar-admin-tabs-bloc");

    tabs.forEach(tab => {
        if (tab.dataset.page === activePage) {
            tab.classList.add("active");
            tab.setAttribute("aria-current", "page");
        } else {
            tab.classList.remove("active");
            tab.removeAttribute("aria-current");
        }
    });
});