document.addEventListener("DOMContentLoaded", function() {
    // Add hover effects to cards
    let cards = document.querySelectorAll(".card");
    cards.forEach(card => {
        card.addEventListener("mouseover", () => {
            card.style.transform = "scale(1.03)";
        });
        card.addEventListener("mouseleave", () => {
            card.style.transform = "scale(1)";
        });
    });

    // Smooth scroll effect for navigation links
    document.querySelectorAll("a[href^='#']").forEach(anchor => {
        anchor.addEventListener("click", function(e) {
            e.preventDefault();
            document.querySelector(this.getAttribute("href")).scrollIntoView({
                behavior: "smooth"
            });
        });
    });

    // Dark mode toggle
    const toggleDarkMode = document.createElement("button");
    toggleDarkMode.innerText = "Toggle Dark Mode";
    toggleDarkMode.style.position = "fixed";
    toggleDarkMode.style.top = "20px";
    toggleDarkMode.style.right = "20px";
    toggleDarkMode.style.padding = "10px";
    toggleDarkMode.style.background = "#007BFF";
    toggleDarkMode.style.color = "#fff";
    toggleDarkMode.style.border = "none";
    toggleDarkMode.style.borderRadius = "5px";
    toggleDarkMode.style.cursor = "pointer";
    document.body.appendChild(toggleDarkMode);

    toggleDarkMode.addEventListener("click", () => {
        document.body.classList.toggle("dark-mode");
        if (document.body.classList.contains("dark-mode")) {
            document.body.style.background = "#1e1e1e";
            document.body.style.color = "#e0e0e0";
        } else {
            document.body.style.background = "#f8f9fa";
            document.body.style.color = "#333";
        }
    });

    // Button interaction
    document.querySelectorAll(".button").forEach(button => {
        button.addEventListener("mousedown", () => {
            button.style.transform = "scale(0.97)";
        });
        button.addEventListener("mouseup", () => {
            button.style.transform = "scale(1)";
        });
    });
});