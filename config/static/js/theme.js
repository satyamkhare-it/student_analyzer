document.addEventListener("DOMContentLoaded", function () {

    // Apply saved theme on page load
    const savedTheme = localStorage.getItem("theme");
    if (savedTheme) {
        document.documentElement.setAttribute("data-bs-theme", savedTheme);
    } else {
        document.documentElement.setAttribute("data-bs-theme", "light");
    }

    // Toggle theme
    window.toggleTheme = function () {
        const html = document.documentElement;
        const currentTheme = html.getAttribute("data-bs-theme");
        const newTheme = currentTheme === "dark" ? "light" : "dark";

        html.setAttribute("data-bs-theme", newTheme);
        localStorage.setItem("theme", newTheme);
    };
});
