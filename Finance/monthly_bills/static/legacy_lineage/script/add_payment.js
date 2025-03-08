document.addEventListener("DOMContentLoaded", function() {
    if (typeof Stripe === "undefined") {
        console.error("Stripe.js failed to load. Make sure the Stripe script is included in the HTML.");
        return;
    }

    // Initialize Stripe with your publishable key
    const stripe = Stripe("pk_test_51QkiJCFYAt9hUnLyyJEtsQMStjSgXhJJIRPaR3k7NBEg87S9glv91OftfT4MNSPAJwxwmIOUQg80deNqv29Revel00uxErFLM6");

    // Create Stripe Elements instance
    const elements = stripe.elements();

    // Create a Card Element
    const cardElement = elements.create("card", {
        hidePostalCode: true,
        style: {
            base: {
                fontSize: "16px",
                color: "#32325d",
                fontFamily: "Arial, sans-serif",
                '::placeholder': {
                    color: "#aab7c4"
                }
            },
            invalid: {
                color: "#fa755a",
                iconColor: "#fa755a"
            }
        }
    });

    cardElement.mount("#card-element");

    // Handle form submission
    document.getElementById("add-card-btn").addEventListener("click", async function(event) {
        event.preventDefault();
        
        const cardholderName = document.getElementById("cardholder-name").value;
        if (!cardholderName) {
            alert("Please enter the cardholder's name.");
            return;
        }

        // Create a Payment Method
        const { paymentMethod, error } = await stripe.createPaymentMethod({
            type: "card",
            card: cardElement,
            billing_details: {
                name: cardholderName
            }
        });

        if (error) {
            console.error(error.message);
            alert("Error adding payment method: " + error.message);
        } else {
            // Send payment method ID to Django backend
            const response = await fetch("/save-payment-method/", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    payment_method_id: paymentMethod.id,
                    name: cardholderName
                })
            });

            const result = await response.json();
            if (result.success) {
                alert("Payment method added successfully!");
                window.location.href = "/tenant/make-payments/"; // Redirect to payment center
            } else {
                alert("Error: " + result.error);
            }
        }
    });
});
