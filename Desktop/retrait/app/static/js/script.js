console.log("Script chargé !");

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

    // Sidebar toggle
    const toggleBtn = document.querySelector('.sidebar-toggle');
    const sidebar = document.querySelector('.sidebar');
    if (toggleBtn && sidebar) {
        toggleBtn.addEventListener('click', () => {
            sidebar.classList.toggle('active');
        });
    }

    // 👁️ Mot de passe principal
    const password = document.getElementById("password");
    const toggleIcon = document.getElementById("togglePassword");

    if (password && toggleIcon) {
        toggleIcon.addEventListener("click", function () {
            if (password.type === "password") {
                password.type = "text";
                toggleIcon.classList.remove("bi-eye");
                toggleIcon.classList.add("bi-eye-slash");
            } else {
                password.type = "password";
                toggleIcon.classList.remove("bi-eye-slash");
                toggleIcon.classList.add("bi-eye");
            }
        });
    }

    // 👁️ Confirmation mot de passe
    const confirmPassword = document.getElementById("confirm_password");
    const toggleConfirmIcon = document.getElementById("toggleConfirmPassword");

    if (confirmPassword && toggleConfirmIcon) {
        toggleConfirmIcon.addEventListener("click", function () {
            const isPassword = confirmPassword.getAttribute("type") === "password";
            confirmPassword.setAttribute("type", isPassword ? "text" : "password");
            toggleConfirmIcon.classList.toggle("bi-eye");
            toggleConfirmIcon.classList.toggle("bi-eye-slash");
        });
    }
});
