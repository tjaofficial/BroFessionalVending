document.addEventListener('DOMContentLoaded', () => {
    const searchCity = document.getElementById('search-city');
    const searchState = document.getElementById('search-state');
    const searchTenant = document.getElementById('search-tenant');
    const filterBtn = document.getElementById('filter-btn');
    const propertyCards = document.querySelectorAll('.property-card');

    filterBtn.addEventListener('click', () => {
        const cityValue = searchCity.value.toLowerCase();
        const stateValue = searchState.value.toLowerCase();
        const tenantValue = searchTenant.value.toLowerCase();

        propertyCards.forEach(card => {
            const city = card.querySelector('.property-address').textContent.toLowerCase();
            const state = card.querySelector('.property-address').textContent.toLowerCase();
            const tenants = Array.from(card.querySelectorAll('.tenants-list li')).map(li => li.textContent.toLowerCase());

            if (
                (city.includes(cityValue) || !cityValue) &&
                (state.includes(stateValue) || !stateValue) &&
                (tenants.some(tenant => tenant.includes(tenantValue)) || !tenantValue)
            ) {
                card.style.display = 'block';
            } else {
                card.style.display = 'none';
            }
        });
    });
});
