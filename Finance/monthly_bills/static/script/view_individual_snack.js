function openExpiredStockModal() {
    document.getElementById("expiredStockModal").style.display = "flex";
}

function closeExpiredStockModal() {
    document.getElementById("expiredStockModal").style.display = "none";
}

// Close modal when clicking outside of it
window.onclick = function(event) {
    let modal = document.getElementById("expiredStockModal");
    if (event.target === modal) {
        modal.style.display = "none";
    }
};
