// JavaScript for Write-Off Pages
document.addEventListener('DOMContentLoaded', () => {
    // Delete Confirmation Modal
    const deleteButtons = document.querySelectorAll('.btn-delete');
    deleteButtons.forEach(button => {
        button.addEventListener('click', (event) => {
            if (!confirm('Are you sure you want to delete this write-off?')) {
                event.preventDefault();
            }
        });
    });

    // Dynamic Form Validation (Optional)
    const form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', (event) => {
            const amountInput = form.querySelector('input[name="amount"]');
            const dateInput = form.querySelector('input[name="date"]');
            let isValid = true;

            if (!amountInput.value || parseFloat(amountInput.value) <= 0) {
                alert('Please enter a valid amount.');
                isValid = false;
            }

            if (!dateInput.value) {
                alert('Please select a valid date.');
                isValid = false;
            }

            if (!isValid) {
                event.preventDefault();
            }
        });
    }

    // Highlight Row on Hover
    const rows = document.querySelectorAll('.writeoff-table tr');
    rows.forEach(row => {
        row.addEventListener('mouseenter', () => {
            row.style.backgroundColor = '#f5e6d3';
        });

        row.addEventListener('mouseleave', () => {
            row.style.backgroundColor = '';
        });
    });
});

// JavaScript for Write-Off Modals and Actions
document.addEventListener('DOMContentLoaded', () => {
    // Get buttons and modals
    const addWriteoffBtn = document.getElementById('add-writeoff-btn');
    const addWriteoffModal = document.getElementById('add-writeoff-modal');
    const addIncomeBtn = document.getElementById('add-income-btn');
    const addIncomeModal = document.getElementById('add-income-modal');
    const deleteButtons = document.querySelectorAll('.btn-delete');

    // Open Add Modal
    addWriteoffBtn.addEventListener('click', () => {
        addWriteoffModal.style.display = "block";
    });
    addIncomeBtn.addEventListener('click', () => {
        addIncomeModal.style.display = "block";
    });

    // Open Delete Modal
    deleteButtons.forEach(button => {
        button.addEventListener('click', (event) => {
            const writeoffId = event.target.getAttribute('data-id');
            const deleteWriteoffModal = document.getElementById('delete-writeoff-modal'+writeoffId);
            // You can confirm delete action here using the writeoffId
            deleteWriteoffModal.style.display = "block";
        });
    });
});

document.addEventListener('DOMContentLoaded', () => {
    const editButtons1 = document.querySelectorAll('.btn-edit');

    editButtons1.forEach(button => {
        button.addEventListener('click', async (event) => {
            const writeoffId = event.target.getAttribute('data-id');
            console.log(writeoffId)
            const editWriteoffModal1 = document.getElementById('edit-writeoff-modal'+writeoffId);
            const editForm = editWriteoffModal1.querySelector('form');
            const modalCloseButton = editWriteoffModal1.querySelector('.close-modal');
            // Fetch write-off data from the server
            const response = await fetch(`/api/writeoff/${writeoffId}/`);
            if (response.ok) {
                const data = await response.json();
                console.log(data.category)
                console.log(editForm)
                // Populate the form with the fetched data
                editForm.querySelector('#id_category').value = data.category;
                editForm.querySelector('#id_amount').value = data.amount;
                editForm.querySelector('#id_description').value = data.description;
                editForm.querySelector('#id_date').value = data.date;

                // Show the modal
                editWriteoffModal1.style.display = "block";
            } else {
                alert('Failed to fetch data for the selected write-off.');
            }
            // Close the modal
            modalCloseButton.addEventListener('click', () => {
                editWriteoffModal1.style.display = "none";
                console.log('whatevr')
        });
    });

    });
    // Close Modal on Outside Click
    const modals = document.querySelectorAll('.modal');
    modals.forEach(modal => {
        modal.addEventListener('click', (event) => {
            if (event.target === modal) {
                modal.style.display = "none";
            }
        });
    });
});