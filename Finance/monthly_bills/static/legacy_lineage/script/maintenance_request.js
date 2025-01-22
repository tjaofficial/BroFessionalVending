// JavaScript for Maintenance Request Form Validation

document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('form');
    form.addEventListener('submit', (event) => {
        const category = document.getElementById('id_category').value;
        const description = document.getElementById('id_description').value;

        if (!category) {
            alert('Please select a category.');
            event.preventDefault();
            return;
        }

        if (!description.trim()) {
            alert('Please provide a description for the maintenance request.');
            event.preventDefault();
        }
    });
});
