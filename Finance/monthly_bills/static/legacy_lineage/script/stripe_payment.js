function toggleDropdown(id) {
    const dropdownContent = document.getElementById(id);
    dropdownContent.style.display =
      dropdownContent.style.display === "block" ? "none" : "block";
  }
  
  async function submitPayment() {
    const stripe = Stripe("your_publishable_key_here"); // Replace with your Stripe publishable key
  
    const response = await fetch("/create-payment-intent/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        amount: 129000, // Replace with the calculated amount
        payment_method: document.querySelector('input[name="payment-method"]:checked').value,
      }),
    });
  
    const { clientSecret } = await response.json();
  
    const result = await stripe.confirmCardPayment(clientSecret, {
      payment_method: {
        card: {
          number: "4242424242424242", // Replace with real card details
          exp_month: 12,
          exp_year: 2024,
          cvc: "123",
        },
      },
    });
  
    if (result.error) {
      console.error(result.error.message);
    } else {
      alert("Payment Successful!");
    }
  }
  

  function toggleDropdown(id) {
    const dropdownContent = document.getElementById(id);
  
    if (dropdownContent.style.display === "block") {
      // Slide up (close)
      dropdownContent.style.maxHeight = "0";
      setTimeout(() => {
        dropdownContent.style.display = "none";
      }, 300); // Match the duration of the transition (300ms)
    } else {
      // Slide down (open)
      dropdownContent.style.display = "block"; // Ensure it's visible for animation
      const contentHeight = dropdownContent.scrollHeight + "px"; // Get full height of the content
      dropdownContent.style.maxHeight = contentHeight;
  
      // Reset height after animation to enable reusability
      setTimeout(() => {
        dropdownContent.style.maxHeight = "auto";
      }, 300); // Match the duration of the transition (300ms)
    }
  }
  