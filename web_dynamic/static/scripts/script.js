document.addEventListener('DOMContentLoaded', function () {
    const menuToggle = document.querySelector('.menu-toggle');
    const navLinks = document.querySelector('.nav-links');
    const searchIcon = document.querySelector('.mobile-search-icon');
    const searchBar = document.querySelector('.search-bar');

    if (menuToggle && navLinks) {
        menuToggle.addEventListener('click', function () {
            navLinks.classList.toggle('active');
        });
    }

    if (searchIcon && searchBar) {
        searchIcon.addEventListener('click', function () {
            searchBar.classList.toggle('active');
        });
    }
});
