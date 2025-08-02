// static/js/scripts.js

document.addEventListener('DOMContentLoaded', function() {
    const themeToggle = document.getElementById('theme-toggle');
    const body = document.body;

    // Load saved theme from localStorage
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        body.classList.add(savedTheme);
        updateToggleIcon(savedTheme);
    } else {
        // Default to light theme
        body.classList.add('light-theme');
        updateToggleIcon('light-theme');
    }

    themeToggle.addEventListener('click', function() {
        if (body.classList.contains('light-theme')) {
            body.classList.replace('light-theme', 'dark-theme');
            localStorage.setItem('theme', 'dark-theme');
            updateToggleIcon('dark-theme');
        } else {
            body.classList.replace('dark-theme', 'light-theme');
            localStorage.setItem('theme', 'light-theme');
            updateToggleIcon('light-theme');
        }
    });

    function updateToggleIcon(theme) {
        const icon = themeToggle.querySelector('.icon');
        if (theme === 'dark-theme') {
            icon.style.maskImage = `url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24'%3E%3Cpath fill='currentColor' d='M12 2A10 10 0 0 0 2 12a10 10 0 0 0 10 10A10 10 0 0 0 12 2m0 1.5c4.76 0 8.71 3.51 9.4 8.16C21.1 11.2 21 11.6 21 12c0 5.52-4.48 10-10 10c-1.12 0-2.19-.2-3.19-.57C8.16 20.71 12 16.76 12 12V3.5Z'/%3E%3C/svg%3E")`;
        } else {
            icon.style.maskImage = `url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24'%3E%3Cpath fill='currentColor' d='M12 2A10 10 0 0 0 2 12a10 10 0 0 0 10 10A10 10 0 0 0 12 2m0 1.5c4.76 0 8.71 3.51 9.4 8.16C21.1 11.2 21 11.6 21 12c0 5.52-4.48 10-10 10c-1.12 0-2.19-.2-3.19-.57C8.16 20.71 12 16.76 12 12V3.5Z'/%3E%3C/svg%3E")`;
        }
    }
});