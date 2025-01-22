// Dashboard Script

// Chart.js Setup
const expenseChartCtx = document.getElementById('expense-chart').getContext('2d');
const growthChartCtx = document.getElementById('growth-chart').getContext('2d');
const expenseDataKeys = Object.keys(expenseData);
const expenseDataValues = Object.values(expenseData);

new Chart(expenseChartCtx, {
    type: 'pie',
    data: {
        labels: expenseDataKeys,
        datasets: [{
            data: expenseDataValues,
            backgroundColor: ['#ff6384', '#36a2eb', '#cc65fe', '#ffce56', '#4bc0c0'],
        }],
    },
    options: { responsive: true },
});

const labels = growthData.map(item => item.year);
const data = growthData.map(item => item.total);

new Chart(growthChartCtx, {
    type: 'line',
    data: {
        labels: labels,
        datasets: [{
            label: 'Yearly Revenue',
            data: data,
            borderColor: '#4a67d8',
            backgroundColor: 'rgba(74, 103, 216, 0.2)',
            fill: true,
        }],
    },
    options: { responsive: true },
});

// Drag and Drop for Tiles
const tiles = document.querySelectorAll('.tile');
const dashboard = document.querySelector('.dashboard-container');

let draggedTile = null;

tiles.forEach(tile => {
    tile.addEventListener('dragstart', (e) => {
        draggedTile = tile;
        setTimeout(() => {
            tile.style.display = 'none';
        }, 0);
    });

    tile.addEventListener('dragend', () => {
        setTimeout(() => {
            draggedTile.style.display = 'block';
            draggedTile = null;
        }, 0);
    });
});

dashboard.addEventListener('dragover', (e) => {
    e.preventDefault();
    const afterElement = getDragAfterElement(dashboard, e.clientY);
    if (afterElement == null) {
        dashboard.appendChild(draggedTile);
    } else {
        dashboard.insertBefore(draggedTile, afterElement);
    }
});

function getDragAfterElement(container, y) {
    const draggableElements = [...container.querySelectorAll('.tile:not(.dragging)')];

    return draggableElements.reduce((closest, child) => {
        const box = child.getBoundingClientRect();
        const offset = y - box.top - box.height / 2;
        if (offset < 0 && offset > closest.offset) {
            return { offset: offset, element: child };
        } else {
            return closest;
        }
    }, { offset: Number.NEGATIVE_INFINITY }).element;
}
