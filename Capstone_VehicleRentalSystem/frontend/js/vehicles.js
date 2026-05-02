// =========================================================================
// DriveEasy - Fleet Management & Booking Engine
// =========================================================================

// Stores the ID of the currently pending booking slot
let activeBookingId = null;

// The complete, unfiltered catalog of all vehicles from the server
let allVehicles = [];

// The current subset of vehicles matching active search or filter criteria
let filteredFleet = [];

// Tracks the current page for grid pagination
let currentPage = 1;

// The maximum number of vehicle cards to display per page load
const itemsPerPage = 6;

// The specific vehicle currently selected by the user for booking
let activeVehicle = null;

// Initializes dashboard routing, date constraints, and filter listeners upon DOM load
document.addEventListener('DOMContentLoaded', () => {

    // Dynamically route the dashboard button based on the user's role
    const currentRole = getUserRole();
    const dashboardBtn = document.getElementById('dashboardBtn');

    if (dashboardBtn) {
        if (currentRole === 'ADMIN' || currentRole === 'ROLE_ADMIN') {
            dashboardBtn.href = 'admin.html';
            dashboardBtn.textContent = 'Admin Panel';
            dashboardBtn.style.borderColor = 'var(--accent)';
            dashboardBtn.style.color = 'var(--accent)';
        } else {
            dashboardBtn.href = 'profile.html';
            dashboardBtn.textContent = 'My Dashboard';
        }
    }

    // Set up date pickers constraints to prevent selecting past dates
    const now = new Date();
    now.setMinutes(now.getMinutes() - now.getTimezoneOffset());
    const currentDateTime = now.toISOString().slice(0, 16);

    const startInput = document.getElementById('searchStart');
    const endInput = document.getElementById('searchEnd');

    if (startInput && endInput) {
        startInput.setAttribute('min', currentDateTime);
        startInput.addEventListener('change', function() {
            endInput.setAttribute('min', this.value);
        });
    }

    // Bind events for filtering the fleet grid
    document.getElementById('searchName')?.addEventListener('input', applyFilters);
    document.getElementById('filterType')?.addEventListener('change', applyFilters);
    document.getElementById('filterCat')?.addEventListener('change', applyFilters);

    // Bind events for booking summary calculation in the modal
    document.getElementById('bookStart')?.addEventListener('change', updateSummary);
    document.getElementById('bookEnd')?.addEventListener('change', updateSummary);

    // ─────────────────────────────────────────────────────────────────────
    // FIX: Smart overlay click handler
    //
    // PROBLEM BEFORE:
    // Clicking anywhere on the dark overlay area closed the modal
    // immediately — even after the user selected dates and a PENDING
    // booking was already created in the database. This caused the slot
    // to be silently cancelled and confused the user.
    //
    // ROOT CAUSE:
    // The modal overlay div was either:
    // 1. Listening to all clicks and calling closeModal()
    // 2. Clicks inside the card were bubbling up to the overlay
    //
    // FIX IN JS:
    // We attach a click listener only on the overlay itself.
    // e.target === modalOverlay makes sure we only react when the
    // dark background is clicked directly — not when inner card
    // elements bubble up.
    //
    // FIX IN HTML:
    // modal-content has onclick="event.stopPropagation()" which
    // stops ANY click inside the white card from reaching the overlay.
    //
    // TWO CASES HANDLED:
    // 1. activeBookingId = null  → no slot reserved → safe to close
    // 2. activeBookingId is SET  → PENDING booking exists in DB →
    //    show toast, block close, force user to click Cancel or Confirm
    // ─────────────────────────────────────────────────────────────────────
    const modalOverlay = document.getElementById('bookingModal');
    if (modalOverlay) {
        modalOverlay.addEventListener('click', function(e) {
            if (e.target === modalOverlay) {
                if (activeBookingId) {
                    showToast('Please confirm or cancel your booking first.');
                } else {
                    closeModal();
                }
            }
        });
    }

    // Check URL parameters for dates passed from the landing page
    if (document.getElementById('fleetGrid')) {
        const urlParams = new URLSearchParams(window.location.search);
        const passedStart = urlParams.get('start');
        const passedEnd = urlParams.get('end');

        if (passedStart && passedEnd && startInput && endInput) {
            startInput.value = passedStart;
            endInput.value = passedEnd;
            searchVehicles();
        } else {
            loadFleet();
        }
    }
});

// Fetches the entire vehicle catalog from the API and renders the initial grid
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

// Queries the backend for vehicles available strictly between the selected dates
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

// Applies local text and dropdown filters to the global vehicle array
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

// Clears the grid container and builds DOM elements for the currently visible vehicles
function renderGrid() {
    const grid = document.getElementById('fleetGrid');
    if (!grid) return;

    grid.innerHTML = '';
    const start = 0;
    const end = currentPage * itemsPerPage;
    const visibleVehicles = filteredFleet.slice(start, end);

    visibleVehicles.forEach(v => {
        let icon;

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

// Increments the pagination counter and renders the next set of vehicles
function loadMore() {
    currentPage++;
    renderGrid();
}

// Opens the booking modal, enforces role rules, and pre-fills vehicle data
async function openModal(vehicle) {
    const token = localStorage.getItem('token');
    if (!token) {
        showToast('Authentication required.');
        setTimeout(() => window.location.href = 'login.html', 1500);
        return;
    }

    const role = getUserRole();
    if (role === 'ADMIN' || role === 'ROLE_ADMIN') {
        showToast('Admins cannot make customer bookings.');
        return;
    }

    document.getElementById('modalVehicleName').textContent = vehicle.name;

    if (document.getElementById('modalPricePerDay')) {
        document.getElementById('modalPricePerDay').textContent = `₹${vehicle.pricePerDay.toLocaleString()} / day`;
    }

    if (document.getElementById('summaryDuration')) {
        document.getElementById('summaryDuration').textContent = '0 hours';
    }
    if (document.getElementById('summaryTotal')) {
        document.getElementById('summaryTotal').textContent = '₹0';
    }

    // Reset date inputs every time modal opens fresh
    const bookStart = document.getElementById('bookStart');
    const bookEnd = document.getElementById('bookEnd');
    if (bookStart) bookStart.value = '';
    if (bookEnd) bookEnd.value = '';

    activeVehicle = vehicle;
    activeBookingId = null;

    document.getElementById('bookingModal').classList.add('active');
}

// Closes the booking modal and cancels any unconfirmed PENDING booking
// Only called by X button or Cancel button — never triggered by overlay
// click when a PENDING booking exists
async function closeModal() {
    if (activeBookingId) {
        await apiFetch(`/bookings/${activeBookingId}/cancel`, { method: 'PUT' });
        activeBookingId = null;
    }

    document.getElementById('bookingModal').classList.remove('active');
    activeVehicle = null;
}

// Dynamically calculates duration and total cost when the user selects dates
// Also triggers PENDING booking creation to reserve the slot immediately
async function updateSummary() {
    const startStr = document.getElementById('bookStart').value;
    const endStr = document.getElementById('bookEnd').value;

    if (startStr) {
        document.getElementById('bookEnd').min = startStr;
    }

    if (startStr && endStr && activeVehicle) {
        const start = new Date(startStr);
        const end = new Date(endStr);

        if (end > start) {
            const diffTime = Math.abs(end - start);
            let totalHours = Math.floor(diffTime / (1000 * 60 * 60));
            if (totalHours < 1) totalHours = 1;
            const billedDays = Math.ceil(totalHours / 24.0);
            const totalCost = billedDays * activeVehicle.pricePerDay;

            document.getElementById('summaryDuration').textContent =
                `${totalHours} hr${totalHours > 1 ? 's' : ''} (${billedDays} day${billedDays > 1 ? 's' : ''} billed)`;
            document.getElementById('summaryTotal').textContent =
                `₹${totalCost.toLocaleString()}`;

            await createPendingBooking(startStr, endStr);
        }
    }
}

// Creates a PENDING booking to lock the time slot as soon as dates are selected
async function createPendingBooking(start, end) {

    // If user changed dates, cancel the previous PENDING booking first
    if (activeBookingId) {
        await apiFetch(`/bookings/${activeBookingId}/cancel`, { method: 'PUT' });
        activeBookingId = null;
    }

    try {
        const response = await apiFetch('/bookings', {
            method: 'POST',
            body: JSON.stringify({
                vehicleId: activeVehicle.id,
                startTime: start,
                endTime: end
            })
        });

        if (response.ok) {
            const booking = await response.json();
            activeBookingId = booking.id;
            showToast('Slot reserved. Click confirm to finalize.');
        } else {
            const err = await response.json();
            showToast(err.message || 'Slot not available.');
            closeModal();
        }
    } catch (error) {
        showToast('Network error reserving slot.');
    }
}

// Finalizes the booking by promoting the PENDING status to ACTIVE
async function confirmBooking() {
    if (!activeBookingId) {
        showToast('Please select dates first.');
        return;
    }

    const btn = document.getElementById('confirmBtn');
    btn.textContent = 'Processing...';
    btn.disabled = true;

    try {
        const confirmResponse = await apiFetch(
            `/bookings/${activeBookingId}/confirm`,
            { method: 'PUT' }
        );

        if (confirmResponse.ok) {
            showToast('Transaction successful.');

            // Clear ID before closeModal so confirmed booking is NOT cancelled
            activeBookingId = null;

            closeModal();
            setTimeout(() => window.location.href = 'profile.html', 1500);
        } else {
            showToast('Failed to confirm booking.');
        }
    } catch (error) {
        showToast('Network error.');
    } finally {
        btn.textContent = 'Confirm Booking';
        btn.disabled = false;
    }
}

// Decodes the stored JWT to extract and return the user's role
function getUserRole() {
    const token = localStorage.getItem('token');
    if (!token || token === 'undefined') return null;

    try {
        const payload = JSON.parse(atob(token.split('.')[1]));
        const roleData = payload.role || 'USER';
        const normalizedRole = String(roleData).toUpperCase();

        if (normalizedRole === 'ADMIN') {
            return 'ADMIN';
        }

        return 'USER';
    } catch(e) {
        console.error("Token decoding failed:", e);
        return 'USER';
    }
}