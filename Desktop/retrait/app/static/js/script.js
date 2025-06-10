// JS de base pour interactions (sidebar, confirmation, etc.)

document.addEventListener('DOMContentLoaded', function () {
    // Confirmation de suppression
    const confirmDeleteButtons = document.querySelectorAll('.confirm-delete');
    confirmDeleteButtons.forEach(function (btn) {
        btn.addEventListener('click', function (e) {
            if (!confirm("Es-tu sûr de vouloir supprimer cet élément ?")) {
                e.preventDefault();
            }
        });
    });

    // Affichage masqué d'une sidebar (si existante)
    const toggleBtn = document.querySelector('.sidebar-toggle');
    const sidebar = document.querySelector('.sidebar');
    if (toggleBtn && sidebar) {
        toggleBtn.addEventListener('click', () => {
            sidebar.classList.toggle('active');
        });
    }
});





