/* =========================================================================
   DriveEasy - Fleet Management & Booking Engine
   ========================================================================= */

/** * Global State Management for the Fleet Grid
 */
let allVehicles = [];
let filteredFleet = [];
let currentPage = 1;
const itemsPerPage = 6;
let activeVehicle = null;

/* =========================================================================
   INITIALIZATION
   ========================================================================= */

/**
 * Initializes DOM elements, applies date constraints, and triggers initial data fetch.
 */
document.addEventListener('DOMContentLoaded', () => {
  const now = new Date();
      now.setMinutes(now.getMinutes() - now.getTimezoneOffset());
      const currentDateTime = now.toISOString().slice(0, 16);

      const startInput = document.getElementById('searchStart');
      const endInput = document.getElementById('searchEnd');

      // Apply strict chronological constraints to time pickers
      if (startInput && endInput) {
          startInput.setAttribute('min', currentDateTime);
          startInput.addEventListener('change', function() {
              endInput.setAttribute('min', this.value);
          });
      }

    // Bind filter event listeners
    document.getElementById('searchName')?.addEventListener('input', applyFilters);
    document.getElementById('filterType')?.addEventListener('change', applyFilters);
    document.getElementById('filterCat')?.addEventListener('change', applyFilters);

    // Bind modal calculation listeners
    document.getElementById('bookStart')?.addEventListener('change', updateSummary);
    document.getElementById('bookEnd')?.addEventListener('change', updateSummary);

    // =====================================================================
    //  Check for dates passed from the Landing Page
    // =====================================================================
    if (document.getElementById('fleetGrid')) {
        const urlParams = new URLSearchParams(window.location.search);
        const passedStart = urlParams.get('start');
        const passedEnd = urlParams.get('end');

        if (passedStart && passedEnd && startInput && endInput) {
            // 1. Fill the inputs with the passed dates
            startInput.value = passedStart;
            endInput.value = passedEnd;

            // 2. Automatically trigger the availability search
            searchVehicles();
        } else {
            // Otherwise, load the default entire fleet
            loadFleet();
        }
    }
});

/* =========================================================================
   DATA FETCHING (API INTEGRATION)
   ========================================================================= */

/**
 * Fetches the complete, unfiltered vehicle catalog from the backend.
 * Resets search constraints and initializes the global state arrays.
 */
async function loadFleet() {
    const searchStart = document.getElementById('searchStart');
    if (searchStart) searchStart.value = '';
    const searchEnd = document.getElementById('searchEnd');
    if (searchEnd) searchEnd.value = '';

    try {
        const response = await apiFetch('/vehicles?page=0&size=50');

        if (response.ok) {
            const pageData = await response.json();
            allVehicles = pageData.content || [];
            filteredFleet = [...allVehicles];
            currentPage = 1;
            renderGrid();
        } else {
            showToast('Failed to load fleet data.');
        }
    } catch (error) {
        console.error("Connection Error:", error);
        showToast('Server connection failed.');
    }
}

/**
 * Queries the backend for vehicles specifically available between requested dates.
 * Overwrites the global dataset with the filtered results.
 */
async function searchVehicles() {
    const startDate = document.getElementById('searchStart').value;
    const endDate = document.getElementById('searchEnd').value;

    if (!startDate || !endDate) {
        alert("Please select both a Pick-up and Drop-off date.");
        return;
    }

    try {

        const response = await apiFetch(`/vehicles/search?startTime=${startDate}&endTime=${endDate}`);

        if (response.ok) {
            const availableCars = await response.json();
            filteredFleet = availableCars;
            currentPage = 1;
            renderGrid();

            // Handle zero-state
            if (availableCars.length === 0) {
                document.getElementById('fleetGrid').innerHTML =
                    "<h3 style='grid-column: 1/-1; text-align: center; color: var(--red); padding: 40px;'>No vehicles available for these dates.</h3>";
            }
        }
    } catch (error) {
        console.error("Search failed:", error);
        showToast("Error executing availability search.");
    }
}

/* =========================================================================
   UI RENDERING & FILTERING
   ========================================================================= */

/**
 * Evaluates local filter parameters and mutates the display array.
 * Resets pagination upon execution.
 */
function applyFilters() {
    const searchTerm = document.getElementById('searchName')?.value.toLowerCase() || "";
    const typeFilter = document.getElementById('filterType')?.value || "";
    const catFilter = document.getElementById('filterCat')?.value || "";

    filteredFleet = allVehicles.filter(v => {
        const matchesName = v.name.toLowerCase().includes(searchTerm);
        const matchesType = typeFilter === '' || v.type === typeFilter;
        const matchesCat = catFilter === '' ||
            (v.categoryName && v.categoryName.toLowerCase() === catFilter.toLowerCase());
        return matchesName && matchesType && matchesCat;
    });

    currentPage = 1;
    renderGrid();
}

/**
 * Constructs and injects HTML elements for the vehicle grid.
 * Applies visual indicators based on vehicle availability.
 */
function renderGrid() {
    const grid = document.getElementById('fleetGrid');
    if (!grid) return;

    grid.innerHTML = '';
    const start = 0;
    const end = currentPage * itemsPerPage;
    const visibleVehicles = filteredFleet.slice(start, end);

    visibleVehicles.forEach(v => {
        let icon;

        // Determine appropriate SVG iconography based on vehicle properties
        if (v.name.toLowerCase().includes('fortuner')) {
            icon = `<path d="M2 14.5c0-1.5 1-2.5 3-3l1.5-4.5c.3-1 1.2-1.5 2.2-1.5h6.6c1 0 1.9.5 2.2 1.5l1.5 4.5c2 .5 3 1.5 3 3v3h-2M2 14.5v3h2"/><path d="M6.5 11.5l1.2-3.8c.1-.4.5-.7.9-.7h6.8c.4 0 .8.3.9.7l1.2 3.8"/><path d="M12 7v4.5"/><circle cx="6.5" cy="17.5" r="2.5"/><circle cx="17.5" cy="17.5" r="2.5"/><path d="M9 17.5h6"/><path d="M2 14.5h20"/>`;
        } else if (v.type === 'CAR') {
            icon = `<path d="M14 16H9m10 0h3v-3.15a1 1 0 0 0-.84-.99L16 11l-2.7-3.6a1 1 0 0 0-.8-.4H5.24a2 2 0 0 0-1.8 1.1l-1.4 3.1A1.5 1.5 0 0 0 2 12v4h3"/><circle cx="6.5" cy="16.5" r="2.5"/><circle cx="16.5" cy="16.5" r="2.5"/>`;
        } else {
            icon = `<circle cx="5.5" cy="16.5" r="3.5"/><circle cx="18.5" cy="16.5" r="3.5"/><path d="M15 6h3.5L22 12v3M9 16.5h6M11 11.5l3 5M8.5 11.5 5 13M15 6a3.5 3.5 0 1 0-7 0"/>`;
        }

        const isAvailable = (v.active === true);
        const statusText = isAvailable ? 'Available' : 'Unavailable';
        const statusClass = isAvailable ? 'status-available' : 'status-booked';

        const card = document.createElement('div');
        card.className = `vehicle-card ${isAvailable ? '' : 'unavailable'}`;
        card.onclick = isAvailable ? () => openModal(v) : null;

        card.innerHTML = `
            <div class="vehicle-img">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    ${icon}
                </svg>
                <div class="status-badge ${statusClass}">${statusText}</div>
            </div>
            <div class="vehicle-info">
                <div class="vehicle-cat">${v.categoryName || 'Standard'}</div>
                <div class="vehicle-name">${v.name}</div>
                <div class="vehicle-plate"># ${v.registrationNumber}</div>
                <div class="vehicle-tags">
                    <span class="tag">${v.type}</span>
                </div>
                <div class="vehicle-footer">
                    <div class="vehicle-price">₹${v.pricePerDay.toLocaleString()} <span>/ day</span></div>
                    <button class="btn-outline" ${isAvailable ? '' : 'disabled'}>
                        ${isAvailable ? 'Book Now' : 'Not Available'}
                    </button>
                </div>
            </div>
        `;
        grid.appendChild(card);
    });

    const loadMoreBtn = document.getElementById('loadMoreBtn');
    if (loadMoreBtn) {
        loadMoreBtn.style.display = end >= filteredFleet.length ? 'none' : 'block';
    }
}

/**
 * Increments the pagination counter and renders the next subset of vehicles.
 */
function loadMore() {
    currentPage++;
    renderGrid();
}

/* =========================================================================
   TRANSACTION LOGIC & MODALS
   ========================================================================= */

/**
 * Opens the booking modal and populates it with the selected vehicle's data.
 * Validates active session presence before allowing interaction.
 *
 * @param {Object} vehicle - The vehicle object selected from the grid.
 */
/**
 * Opens the booking modal and populates it with the selected vehicle's data.
 * Validates active session presence before allowing interaction.
 */
function openModal(vehicle) {
    if (!localStorage.getItem('token')) {
        showToast('Authentication required to process booking.');
        setTimeout(() => window.location.href = 'login.html', 1500);
        return;
    }

    activeVehicle = vehicle;
    document.getElementById('modalVehicleName').textContent = vehicle.name;

    // Updated to show the price of the clicked vehicle
    document.getElementById('modalPricePerDay').textContent = `₹${vehicle.pricePerDay.toLocaleString()} / day`;

    // Reset fields for the new selection
    document.getElementById('bookStart').value = '';
    document.getElementById('bookEnd').value = '';

    // Match the IDs in your HTML
    if (document.getElementById('summaryDuration')) {
        document.getElementById('summaryDuration').textContent = '0 hours';
    }
    document.getElementById('summaryTotal').textContent = '₹0';

    // Set the minimum pick-up time to 'now'
    const now = new Date();
    now.setMinutes(now.getMinutes() - now.getTimezoneOffset());
    document.getElementById('bookStart').min = now.toISOString().slice(0, 16);

    document.getElementById('bookingModal').classList.add('active');
}

/**
 * Closes the active booking modal and clears the selected vehicle state.
 */
function closeModal() {
    document.getElementById('bookingModal').classList.remove('active');
    activeVehicle = null;
}

/**
 * Dynamically calculates and updates the total duration and cost in the UI.
 * Mirrors the backend Math.ceil(hours / 24) pricing logic.
 */
function updateSummary() {
    const startStr = document.getElementById('bookStart').value;
    const endStr = document.getElementById('bookEnd').value;

    if(startStr) {
        document.getElementById('bookEnd').min = startStr;
    }

    if (startStr && endStr && activeVehicle) {
        const start = new Date(startStr);
        const end = new Date(endStr);

        if (end > start) {
            const diffTime = Math.abs(end - start);

            // Calculate total hours
            let totalHours = Math.floor(diffTime / (1000 * 60 * 60));
            if (totalHours < 1) totalHours = 1;

            // Calculate billable 24-hour blocks
            const billedDays = Math.ceil(totalHours / 24.0);
            const totalCost = billedDays * activeVehicle.pricePerDay;

            // Update the UI elements
            const durationEl = document.getElementById('summaryDuration');
            if (durationEl) {
                durationEl.textContent = `${totalHours} hr${totalHours > 1 ? 's' : ''} (${billedDays} day${billedDays > 1 ? 's' : ''} billed)`;
            }

            document.getElementById('summaryTotal').textContent = `₹${totalCost.toLocaleString()}`;
        } else {
            // Reset if dates are invalid
            if (document.getElementById('summaryDuration')) {
                document.getElementById('summaryDuration').textContent = '0 hours';
            }
            document.getElementById('summaryTotal').textContent = '₹0';
        }
    }
}

/**
 * Submits the finalized booking request to the server.
 * Manages the transition from PENDING -> ACTIVE status.
 */
async function confirmBooking() {
    const start = document.getElementById('bookStart').value;
    const end = document.getElementById('bookEnd').value;

    if (!start || !end) {
        showToast("Date parameters are required.");
        return;
    }

    const btn = document.getElementById('confirmBtn');
    btn.textContent = 'Processing...';
    btn.disabled = true;

    try {
        const createResponse = await apiFetch('/bookings', {
                    method: 'POST',
                    body: JSON.stringify({
                        vehicleId: activeVehicle.id,
                        startTime: start,
                        endTime: end
                    })
                });

        if (createResponse.ok) {
            const newBooking = await createResponse.json();

            // Execute immediate confirmation protocol
            const confirmResponse = await apiFetch(`/bookings/${newBooking.id}/confirm`, {
                method: 'PUT'
            });

            if (confirmResponse.ok) {
                showToast(`Transaction successful.`);
                closeModal();
                setTimeout(() => window.location.href = 'profile.html', 1500);
            } else {
                showToast('Booking created but failed to activate.');
            }
        } else {
            const errorData = await createResponse.json();
            showToast(errorData.message || 'Transaction failed.');
        }
    } catch (error) {
        showToast('Network error during transaction processing.');
    } finally {
        btn.textContent = 'Confirm Booking';
        btn.disabled = false;
    }
}