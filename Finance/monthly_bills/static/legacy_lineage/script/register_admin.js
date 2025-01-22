// Register Admin Form Validation

document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('form');
    form.addEventListener('submit', (event) => {
        const password1 = document.getElementById('id_password1').value;
        const password2 = document.getElementById('id_password2').value;

        if (password1 !== password2) {
            event.preventDefault();
            alert('Passwords do not match. Please try again.');
        }
    });
});