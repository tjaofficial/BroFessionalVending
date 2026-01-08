(function () {
  function $(sel) { return document.querySelector(sel); }
  function $all(sel) { return Array.from(document.querySelectorAll(sel)); }

  const modalId = "dues-payment-modal";

  function openModal() {
    const modal = document.getElementById(modalId);
    if (modal) modal.style.display = "flex";
  }

  function closeModal() {
    const modal = document.getElementById(modalId);
    if (modal) modal.style.display = "none";
  }

  function setFieldValueByName(name, value) {
    const field = document.querySelector(`[name="${name}"]`);
    if (!field) return;
    field.value = value;
    field.dispatchEvent(new Event("change", { bubbles: true }));
  }

  function setSuggestedAmount(paidSoFar, dues) {
    const amountField = document.querySelector(`[name="amount"]`);
    if (!amountField) return;

    const paid = parseFloat(paidSoFar || "0");
    const due = parseFloat(dues || "0");
    const remaining = Math.max(due - paid, 0);

    // If they already paid >= dues, default to 0 or leave existing value
    if (remaining > 0) {
      amountField.value = remaining.toFixed(2);
    }
  }

  function todayISO() {
    const d = new Date();
    const mm = String(d.getMonth() + 1).padStart(2, "0");
    const dd = String(d.getDate()).padStart(2, "0");
    return `${d.getFullYear()}-${mm}-${dd}`;
  }

  // Click outside modal to close
  document.addEventListener("click", function (e) {
    const modal = document.getElementById(modalId);
    if (!modal) return;
    if (e.target === modal) closeModal();
  });

  // Hook close X if present
  document.addEventListener("click", function (e) {
    if (e.target.classList.contains("close-modal")) {
      closeModal();
    }
  });

  // Main click handler: open modal and prefill fields
  document.addEventListener("click", function (e) {
    const btn = e.target.closest(".open-dues-modal");
    if (!btn) return;

    const memberId = btn.dataset.memberId;
    const month = btn.dataset.month;      // YYYY-MM-01 (first of month) if clicked on pill
    const total = btn.dataset.total || "0";
    const dues = btn.dataset.dues || "100";

    // Prefill member
    if (memberId) setFieldValueByName("member", memberId);

    // Prefill date:
    // - if they clicked a month pill, set paid_date to that month’s first day
    // - else default to today
    // Apply-to-month should match the clicked month (if provided)
    if (month) {
    setFieldValueByName("apply_month", monthInputValueFromYYYYMM01(month));
    } else {
    // default apply month to current month
    const t = todayISO();
    setFieldValueByName("apply_month", t.slice(0, 7));
    }

    // Payment date defaults to today (real payment date)
    setFieldValueByName("paid_date", todayISO());


    // Smart amount suggestion = remaining for that month
    setSuggestedAmount(total, dues);

    openModal();
  });

  // Optional: ESC closes modal
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") closeModal();
  });
})();

function monthInputValueFromYYYYMM01(ymd) {
  // ymd like "2026-01-01" -> "2026-01" for <input type="month">
  if (!ymd) return "";
  return ymd.slice(0, 7);
}
