// Please notice that we generated all "base"-files so we have a starting point to implement our project

document.addEventListener('DOMContentLoaded', function() {

    // 1. Mobile Menu Toggle (Burger Icon)
    const menuToggle = document.querySelector('.mobile-menu-toggle');
    const mainNav = document.querySelector('.main-navigation');
    const icon = menuToggle.querySelector('i');

    if (menuToggle) {
        menuToggle.addEventListener('click', function() {
            // Toggle Klasse 'active' auf der Navigation
            mainNav.classList.toggle('active');

            // Icon ändern (von Burger zu X und zurück)
            if (mainNav.classList.contains('active')) {
                icon.classList.remove('fa-bars');
                icon.classList.add('fa-times');
            } else {
                icon.classList.remove('fa-times');
                icon.classList.add('fa-bars');
            }
        });
    }

    // 2. Mobile Sub-Menu Toggle (Dropdowns)
    // Wir suchen alle Items, die ein Untermenü haben
    const dropdownItems = document.querySelectorAll('.nav-item.has-sub > a');

    dropdownItems.forEach(item => {
        item.addEventListener('click', function(e) {
            // Prüfen, ob wir in der mobilen Ansicht sind (z.B. Fensterbreite < 900px)
            // oder einfach prüfen, ob das Menü "active" ist oder CSS display mode checken.
            // Einfachste Methode: Wenn CSS Media Query greift, verhalten wir uns wie Mobile.

            if (window.innerWidth <= 900) {
                e.preventDefault(); // Verhindert, dass der Link sofort geladen wird

                // Das Elternelement (li) finden
                const parent = this.parentElement;

                // Toggle Klasse 'dropdown-active' für das CSS
                parent.classList.toggle('dropdown-active');
            }
        });
    });

});