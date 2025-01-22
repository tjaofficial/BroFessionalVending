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

// View Tenants Script

document.addEventListener('DOMContentLoaded', () => {
    const propertyAddresses = document.querySelectorAll('.property-address');

    propertyAddresses.forEach(address => {
        const propertyId = address.getAttribute('data-property-id');

        if (!propertyId || propertyId === 'null') {
            // Skip elements with no valid property ID
            return;
        }

        let popup;

        address.addEventListener('mouseenter', async (event) => {
            // Create or fetch the popup element
            popup = document.getElementById(`popup-${propertyId}`);

            if (!popup) {
                popup = document.createElement('div');
                popup.id = `popup-${propertyId}`;
                popup.className = 'property-popup';
                document.body.appendChild(popup);
            }

            if (!popup.dataset.loaded) {
                try {
                    const response = await fetch(`/api/property/${propertyId}/`);
                    if (response.ok) {
                        const data = await response.json();
                        popup.innerHTML = `
                            <p><strong>Property Address:</strong> ${data.address}</p><br>
                            <p><strong>City:</strong> ${data.city}</p><br>
                            <p><strong>State:</strong> ${data.state}</p><br>
                            <p><strong>Sqr Ft.:</strong> ${data.square_footage} sq ft</p><br>
                            <p><strong>Year Built:</strong> ${data.year_built}</p><br>
                            <p><strong>Manager Name:</strong> ${data.manager_name}</p><br>
                            <p><strong>Maintenance Contact:</strong> ${data.maintenance_contact}</p><br>
                            <p><strong>Maintenance Phone:</strong> ${data.maintenance_phone}</p><br>
                            <p><strong>Notes:</strong> ${data.notes}</p>
                        `;
                        popup.dataset.loaded = true;
                    } else {
                        popup.innerHTML = '<p>Failed to load property data.</p>';
                    }
                } catch (error) {
                    popup.innerHTML = '<p>Error fetching property data.</p>';
                }
            }

            // Position the popup and show it
            popup.style.display = 'block';
            popup.style.position = 'absolute';
            popup.style.left = `${event.pageX + 10}px`;
            popup.style.top = `${event.pageY + 10}px`;
        });

        address.addEventListener('mousemove', (event) => {
            if (popup) {
                popup.style.left = `${event.pageX + 10}px`;
                popup.style.top = `${event.pageY + 10}px`;
            }
        });

        address.addEventListener('mouseleave', () => {
            if (popup) {
                popup.style.display = 'none';
            }
        });
    });
});
