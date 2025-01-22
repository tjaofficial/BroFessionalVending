// script.js

document.addEventListener('DOMContentLoaded', () => {
    // Toggle Profile Dropdown
    const profileBtn = document.getElementById('profile-btn');
    const profileDropdown = document.getElementById('profile-dropdown');
    profileBtn.addEventListener('click', () => {
        let profDisp = profileDropdown.style.display;
        if (profDisp == "none"){
            var setting = "block";
        } else {
            var setting = "none";
        }
        profileDropdown.style.display = setting;
    });

    // Toggle Notifications Dropdown
    const notificationsBtn = document.getElementById('notifications-btn');
    const notificationsDropdown = document.getElementById('notifications-dropdown');
    notificationsBtn.addEventListener('click', () => {
        let notifDisp = notificationsDropdown.style.display;
        if (notifDisp == "none"){
            var setting = "block";
        } else {
            var setting = "none";
        }
        notificationsDropdown.style.display = setting;
    });

    // Toggle Sidebar Submenus
    window.toggleSubmenu = (submenuId) => {
        const submenu = document.getElementById(submenuId);
        let subMenuDisp = submenu.style.display;
        if (subMenuDisp == "none"){
            var setting = "block";
        } else {
            var setting = "none";
        }
        submenu.style.display = setting;
    };

    // Close dropdowns when clicking outside
    document.addEventListener('click', (event) => {
        if (!profileBtn.contains(event.target) && !profileDropdown.contains(event.target)) {
            profileDropdown.classList.add('hidden');
        }
        if (!notificationsBtn.contains(event.target) && !notificationsDropdown.contains(event.target)) {
            notificationsDropdown.classList.add('hidden');
        }
    });
});