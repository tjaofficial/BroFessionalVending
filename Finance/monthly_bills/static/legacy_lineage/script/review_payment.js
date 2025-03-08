document.addEventListener("DOMContentLoaded", function () {
    const confirmButton = document.getElementById("confirm-payment-btn");
    
    confirmButton.addEventListener("click", function () {
        document.getElementById("payment-form").submit();
    });
});
