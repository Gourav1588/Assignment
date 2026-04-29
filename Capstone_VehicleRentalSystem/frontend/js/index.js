/* =========================================================================
   DriveEasy - Landing Page Logic
   ========================================================================= */

/**
 * Initializes chronological constraints on DOM load to prevent past-time selections.
 * Ensures the date picker minimum is set to the current local time.
 */
document.addEventListener('DOMContentLoaded', () => {
    const startDateInput = document.getElementById('startDate');
    const endDateInput = document.getElementById('endDate');

    if (startDateInput && endDateInput) {
        // Calculate current local time in YYYY-MM-DDTHH:mm format
        const now = new Date();
        now.setMinutes(now.getMinutes() - now.getTimezoneOffset());
        const currentDateTime = now.toISOString().slice(0, 16);

        // Apply constraints to prevent booking in the past
        startDateInput.min = currentDateTime;
        endDateInput.min = currentDateTime;

        // Dynamically update the return time minimum based on pickup selection
        startDateInput.addEventListener('change', function() {
            endDateInput.min = this.value;
        });
    }
});

/* =========================================================================
   USER ACTIONS & REDIRECTIONS
   ========================================================================= */

/**
 * Validates search inputs and redirects the user to the fleet inventory page.
 * Passes exact time strings as URL parameters for the vehicles page to process.
 */
function handleSearch() {
    const start = document.getElementById('startDate').value;
    const end = document.getElementById('endDate').value;

    // Validation: Ensure both fields are populated
    if (!start || !end) {
        showToast('Both pickup and return times are required.');
        return;
    }

    const startTime = new Date(start);
    const endTime = new Date(end);

    // Validation: Ensure duration is logical
    if (endTime <= startTime) {
        showToast('Return time must be after the pickup time.');
        return;
    }

    showToast('Locating available fleet...');

    // Redirect to vehicles page with time parameters in the URL
    setTimeout(() => {
        window.location.href = `vehicles.html?start=${start}&end=${end}`;
    }, 1000);
}

/**
 * Verifies session authorization prior to redirecting to the booking flow.
 * @param {string} name - The identifier of the vehicle.
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
 * @param {string} category - The vehicle classification.
 */
function filterCategory(category) {
    showToast(`Applying ${category} filters...`);
    setTimeout(() => {
        window.location.href = 'vehicles.html';
    }, 800);
}