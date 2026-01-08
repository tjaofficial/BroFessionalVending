// rent_overview.js
document.addEventListener("DOMContentLoaded", () => {
  const tenantFilter = document.getElementById("filter-tenant");
  const monthFilter = document.getElementById("filter-month");
  const statusFilter = document.getElementById("filter-status");
  const clearBtn = document.getElementById("clear-filters");

  const rows = Array.from(document.querySelectorAll("#rent-table tbody tr"));

  function applyFilters() {
    const tVal = (tenantFilter.value || "").toLowerCase().trim();
    const mVal = (monthFilter.value || "").trim(); // "2026-01"
    const sVal = (statusFilter.value || "").trim();

    rows.forEach((row) => {
      const tenant = row.dataset.tenant || "";
      const month = row.dataset.month || "";
      const status = row.dataset.status || "";

      const okTenant = !tVal || tenant.includes(tVal);
      const okMonth = !mVal || month === mVal;
      const okStatus = !sVal || status === sVal;

      row.style.display = (okTenant && okMonth && okStatus) ? "" : "none";
    });
  }

  [tenantFilter, monthFilter, statusFilter].forEach(el => el.addEventListener("input", applyFilters));

  clearBtn.addEventListener("click", () => {
    tenantFilter.value = "";
    monthFilter.value = "";
    statusFilter.value = "";
    applyFilters();
  });

  // Modal logic
  const modal = document.getElementById("payment-modal");
  const closeBtn = document.getElementById("close-payment");
  const title = document.getElementById("payment-title");
  const tenantIdInput = document.getElementById("payment-tenant-id");

  document.querySelectorAll(".open-payment").forEach(btn => {
    btn.addEventListener("click", () => {
      const tenantId = btn.dataset.tenantId;
      const tenantName = btn.dataset.tenantName;
      title.textContent = `Record Payment — ${tenantName}`;
      tenantIdInput.value = tenantId;
      modal.style.display = "flex";
    });
  });

  closeBtn.addEventListener("click", () => modal.style.display = "none");
  window.addEventListener("click", (e) => {
    if (e.target === modal) modal.style.display = "none";
  });
});
