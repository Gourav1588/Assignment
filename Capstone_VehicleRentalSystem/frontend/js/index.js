/* =========================================================================
   DriveEasy - Landing Page Logic
   ========================================================================= */

/**
 * Initializes chronological constraints on DOM load to prevent past-date selections.
 */
document.addEventListener('DOMContentLoaded', () => {
    const startDateInput = document.getElementById('startDate');
    const endDateInput = document.getElementById('endDate');

    if (startDateInput && endDateInput) {
        const today = new Date().toISOString().split('T')[0];
        startDateInput.min = today;
        endDateInput.min = today;

        startDateInput.addEventListener('change', function() {
            endDateInput.min = this.value;
        });
    }
});

/* =========================================================================
   USER ACTIONS & REDIRECTIONS
   ========================================================================= */

/**
 * Validates search inputs from the hero section and redirects the user
 * to the fleet inventory page.
 */
function handleSearch() {
    const start = document.getElementById('startDate').value;
    const end = document.getElementById('endDate').value;

    if (!start || !end) {
        showToast('Both pickup and return dates are required.');
        return;
    }

    if (new Date(end) <= new Date(start)) {
        showToast('Return date must follow the pickup date.');
        return;
    }

    showToast('Locating available fleet...');
    setTimeout(() => {
        window.location.href = 'vehicles.html';
    }, 1000);
}

/**
 * Verifies session authorization prior to executing a booking request.
 * Redirects unauthenticated users to the login portal.
 *
 * @param {string} name - The identifier of the vehicle being requested.
 */
function handleBook(name) {
    const token = localStorage.getItem('token');

    if (!token) {
        showToast(`Authentication required for ${name}.`);
        setTimeout(() => {
            window.location.href = 'login.html';
        }, 1500);
        return;
    }

    window.location.href = 'vehicles.html';
}

/**
 * Simulates category filtering and redirects to the main inventory page.
 *
 * @param {string} category - The specific vehicle classification to filter.
 */
function filterCategory(category) {
    showToast(`Applying ${category} filters...`);

    setTimeout(() => {
        window.location.href = 'vehicles.html';
    }, 800);
}