document.addEventListener('DOMContentLoaded', async () => {
    const tenantId = '2'; // Replace with actual tenant ID
    const response = await fetch(`/get-tenant-payment-info/${tenantId}`);
    const tenantInfo = await response.json();

    if (response.ok) {
        // Populate tenant details
        document.getElementById('tenant-name').textContent = tenantInfo.name;
        document.getElementById('tenant-email').textContent = tenantInfo.email;
        document.getElementById('tenant-rent').textContent = `$${tenantInfo.rent_amount}`;
        document.getElementById('tenant-due-date').textContent = tenantInfo.due_date;

        // Handle Payment
        const stripe = Stripe('pk_test_51QkiJCFYAt9hUnLyyJEtsQMStjSgXhJJIRPaR3k7NBEg87S9glv91OftfT4MNSPAJwxwmIOUQg80deNqv29Revel00uxErFLM6'); // Replace with actual publishable key
        const elements = stripe.elements();
        const cardElement = elements.create('card');
        cardElement.mount('#card-element');

        document.getElementById('payment-form').addEventListener('submit', async (e) => {
            e.preventDefault();

            // Create a Payment Intent
            const paymentIntent = await fetch('/create-rent-payment-intent/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ tenant_id: tenantId }),
            }).then((res) => res.json());

            const { error, paymentIntent: confirmedPaymentIntent } = await stripe.confirmCardPayment(
                paymentIntent.clientSecret,
                {
                    payment_method: {
                        card: cardElement,
                        billing_details: {
                            name: tenantInfo.name,
                            email: tenantInfo.email,
                        },
                    },
                }
            );

            if (error) {
                document.getElementById('payment-result').textContent = `Error: ${error.message}`;
            } else {
                document.getElementById('payment-result').textContent = 'Payment successful!';
                if (document.getElementById('autopay').checked) {
                    // Save the card for future payments (auto-pay setup)
                    console.log('Auto-pay enabled');
                }
            }
        });
    } else {
        console.error(tenantInfo.error);
    }
});
