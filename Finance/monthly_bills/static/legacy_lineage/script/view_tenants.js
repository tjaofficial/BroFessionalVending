document.addEventListener('DOMContentLoaded', () => {
    const searchName = document.getElementById('search-name');
    const searchCity = document.getElementById('search-city');
    const searchState = document.getElementById('search-state');
    const filterBtn = document.getElementById('filter-btn');
    const tenantCards = document.querySelectorAll('.tenant-card');

    filterBtn.addEventListener('click', () => {
        const nameValue = searchName.value.toLowerCase();
        const cityValue = searchCity.value.toLowerCase();
        const stateValue = searchState.value.toLowerCase();

        tenantCards.forEach(card => {
            const name = card.querySelector('.tenant-name').textContent.toLowerCase();
            const city = card.querySelector('.tenant-address').textContent.toLowerCase();
            const state = card.querySelector('.tenant-address').textContent.toLowerCase();

            if (
                (name.includes(nameValue) || !nameValue) &&
                (city.includes(cityValue) || !cityValue) &&
                (state.includes(stateValue) || !stateValue)
            ) {
                card.style.display = 'block';
            } else {
                card.style.display = 'none';
            }
        });
    });
});
