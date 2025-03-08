function toggleDropdown(id) {
    const dropdownContent = document.getElementById(id);
    dropdownContent.style.display =
      dropdownContent.style.display === "block" ? "none" : "block";
  }
  
document.addEventListener("DOMContentLoaded", function () {
  const reviewBtn = document.getElementById("review-payment-btn");

  reviewBtn.addEventListener("click", function (event) {
      event.preventDefault(); // Prevent default link behavior

      let selectedAmount = document.querySelector('input[name="payment-amount"]:checked').value;
      let selectedMethod = document.querySelector('input[name="payment-method"]:checked').value;
      let selectedDate = document.getElementById("payment-date-input").value;

      if (selectedAmount === "other") {
          selectedAmount = document.querySelector('input[name="other-amount"]').value;
      }

      if (!selectedAmount || parseFloat(selectedAmount) <= 0) {
          alert("Please enter a valid payment amount.");
          return;
      }

      // Redirect to the review payment page with amount, method, and date
      window.location.href = `/tenant/review-payment/?amount=${selectedAmount}&method=${selectedMethod}&date=${selectedDate}`;
  });
});


async function submitPayment() {
  // Initialize Stripe (Make sure to use the correct publishable key)
  const stripe = Stripe("pk_test_51QkiJCFYAt9hUnLyyJEtsQMStjSgXhJJIRPaR3k7NBEg87S9glv91OftfT4MNSPAJwxwmIOUQg80deNqv29Revel00uxErFLM6");

  // Get the payment amount
  let paymentAmount = document.querySelector('input[name="payment-amount"]:checked').value;
  if (paymentAmount === "other") {
      paymentAmount = document.querySelector('input[type="number"]').value * 100; // Convert to cents
  } else {
      paymentAmount = 129000; // Example: $1,290.00 in cents
  }

  // Call Django Backend to Create a Stripe Checkout Session
  const response = await fetch("/create-checkout-session/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
          amount: paymentAmount,
          email: "customer@example.com", // Replace with actual tenant email
      }),
  });

  const { sessionId, error } = await response.json();
  if (error) {
      console.error("Error creating checkout session:", error);
      return;
  }

  // Redirect to Stripe Checkout
  stripe.redirectToCheckout({ sessionId: sessionId }).then((result) => {
      if (result.error) {
          console.error(result.error.message);
      }
  });
}


function toggleDropdown(id) {
  const dropdownContent = document.getElementById(id);

  if (dropdownContent.style.display === "flex") {
    // Slide up (close)
    dropdownContent.style.maxHeight = "0";

    setTimeout(() => {
      dropdownContent.style.display = "none";
    }, 300); // Match the duration of the transition (300ms)
  } else {
    // Slide down (open)
    dropdownContent.style.display = "flex"; // Ensure it's visible for animation
    dropdownContent.style.flexDirection = "column";
    dropdownContent.style.padding = "20px";
    const contentHeight = dropdownContent.scrollHeight + "px"; // Get full height of the content
    dropdownContent.style.maxHeight = contentHeight;

    // Reset height after animation to enable reusability
    setTimeout(() => {
      dropdownContent.style.maxHeight = "auto";
    }, 300); // Match the duration of the transition (300ms)
  }
}

document.addEventListener("DOMContentLoaded", function () {
  // Select all radio buttons with name 'payment-amount'
  const paymentOptions = document.querySelectorAll('input[name="payment-amount"]');
  const selectedAmountDisplay = document.getElementById("selected_amount");
  const selectedFeeDisplay = document.getElementById("stripe_fees");

  // Function to update selected amount
  function updateSelectedAmount() {
      let selectedValue = document.querySelector('input[name="payment-amount"]:checked').value;
      let amountText = "";
      console.log(selectedValue)
      function calc_process_fees(total_amount){
        console.log(total_amount)
        let feeRate = 0.029;
        let fixedFee = 0.30;
        let totalCharge = (parseFloat(total_amount) + parseFloat(fixedFee)) / (1 - parseFloat(feeRate));
        console.log(totalCharge-parseFloat(total_amount))
        console.log((1 - feeRate))
        return Math.round((totalCharge-parseFloat(total_amount)) * 100) / 100;
      }
      if (selectedValue === "full") {
          amountText = document.getElementById("full-amount").innerText;
      } else if (selectedValue === "full_pre") {
          amountText = document.getElementById("prepay-amount").innerText;
      } else {
          // Get value from custom input field for "Other Amount"
          let otherAmount = document.querySelector('input[name="other-amount"]').value;
          amountText = otherAmount ? `$${otherAmount}` : "$0.00";
      }

      // Update the selected amount display
      selectedAmountDisplay.innerText = amountText;
      selectedFeeDisplay.innerText = `+$${parseFloat(calc_process_fees(amountText.substring(1))).toFixed(2)} Convience Fee`
  }
  console.log(paymentOptions);
  // Add event listener to each radio button
  paymentOptions.forEach(option => {
      option.addEventListener("change", updateSelectedAmount);
  });

  // Add event listener to "Other Amount" input for live updates
  document.querySelector('input[name="other-amount"]').addEventListener("input", updateSelectedAmount);
});
