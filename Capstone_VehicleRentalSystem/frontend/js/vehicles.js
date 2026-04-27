    // ===============================
    // FLEET & BOOKING SCRIPT (vehicles.js)
    // ===============================

    // 1. STATE VARIABLES
    let allVehicles = [];
    let filteredFleet = [];
    let currentPage = 1;
    const itemsPerPage = 6;
    let activeVehicle = null;

    // 2. FETCH DATA FROM BACKEND
    async function loadFleet() {
        try {
            const response = await fetch(`${API_BASE_URL}/vehicles?page=0&size=50`);

            if (response.ok) {
                const pageData = await response.json();
                console.log(pageData);
                // Spring Data Page puts the list inside 'content'
                allVehicles = pageData.content || [];
                filteredFleet = [...allVehicles];
                renderGrid();
            } else {
                showToast('Failed to load fleet.');
            }
        } catch (error) {
            console.error("Connection Error:", error);
            showToast('Server is offline.');
        }
    }

    // 3. RENDER THE GRID
    function renderGrid() {
        const grid = document.getElementById('fleetGrid');
        if (!grid) return;

        grid.innerHTML = '';
        const start = 0;
        const end = currentPage * itemsPerPage;
        const visibleVehicles = filteredFleet.slice(start, end);

        visibleVehicles.forEach(v => {
            let icon;

            // Custom SUV Icon for Fortuner
            if (v.name.toLowerCase().includes('fortuner')) {
                icon = `<path d="M2 14.5c0-1.5 1-2.5 3-3l1.5-4.5c.3-1 1.2-1.5 2.2-1.5h6.6c1 0 1.9.5 2.2 1.5l1.5 4.5c2 .5 3 1.5 3 3v3h-2M2 14.5v3h2"/><path d="M6.5 11.5l1.2-3.8c.1-.4.5-.7.9-.7h6.8c.4 0 .8.3.9.7l1.2 3.8"/><path d="M12 7v4.5"/><circle cx="6.5" cy="17.5" r="2.5"/><circle cx="17.5" cy="17.5" r="2.5"/><path d="M9 17.5h6"/><path d="M2 14.5h20"/>`;
            }
            else if (v.type === 'CAR') {
                icon = `<path d="M14 16H9m10 0h3v-3.15a1 1 0 0 0-.84-.99L16 11l-2.7-3.6a1 1 0 0 0-.8-.4H5.24a2 2 0 0 0-1.8 1.1l-1.4 3.1A1.5 1.5 0 0 0 2 12v4h3"/><circle cx="6.5" cy="16.5" r="2.5"/><circle cx="16.5" cy="16.5" r="2.5"/>`;
            }
            else {
                icon = `<circle cx="5.5" cy="16.5" r="3.5"/><circle cx="18.5" cy="16.5" r="3.5"/><path d="M15 6h3.5L22 12v3M9 16.5h6M11 11.5l3 5M8.5 11.5 5 13M15 6a3.5 3.5 0 1 0-7 0"/>`;
            }

            // --- THE AVAILABILITY FIX ---
            // Checks both variations to ensure it catches the Spring Boot response
            const isAvailable = (v.active === true );

            const statusText = isAvailable ? 'Available' : 'Unavailable';
            const statusClass = isAvailable ? 'status-available' : 'status-booked';

            const card = document.createElement('div');
            card.className = `vehicle-card ${isAvailable ? '' : 'unavailable'}`;

            // Disable click if not available
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

    // 4. FILTERING LOGIC
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

    function loadMore() {
        currentPage++;
        renderGrid();
    }

    // 5. BOOKING MODAL LOGIC
    function openModal(vehicle) {
        const token = localStorage.getItem('token');
        if (!token) {
            showToast('Please sign in to book a vehicle.');
            setTimeout(() => window.location.href = 'login.html', 1500);
            return;
        }

        activeVehicle = vehicle;
        document.getElementById('modalVehicleName').textContent = vehicle.name;
        document.getElementById('modalPricePerDay').textContent = `₹${vehicle.pricePerDay} / day`;

        document.getElementById('bookStart').value = '';
        document.getElementById('bookEnd').value = '';
        document.getElementById('summaryDays').textContent = '0 days';
        document.getElementById('summaryTotal').textContent = '₹0';

        const today = new Date().toISOString().split('T')[0];
        document.getElementById('bookStart').min = today;
        document.getElementById('bookingModal').classList.add('active');
    }

    function closeModal() {
        document.getElementById('bookingModal').classList.remove('active');
        activeVehicle = null;
    }

    function updateSummary() {
        const startStr = document.getElementById('bookStart').value;
        const endStr = document.getElementById('bookEnd').value;

        if(startStr) { document.getElementById('bookEnd').min = startStr; }

        if (startStr && endStr && activeVehicle) {
            const start = new Date(startStr);
            const end = new Date(endStr);

            if (end >= start) {
                const diffTime = Math.abs(end - start);
                const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24)) +1;
                const totalCost = diffDays * activeVehicle.pricePerDay;

                document.getElementById('summaryDays').textContent = `${diffDays} day${diffDays > 1 ? 's' : ''}`;
                document.getElementById('summaryTotal').textContent = `₹${totalCost.toLocaleString()}`;
            }
        }
    }


    /* =========================================
       6. CONFIRM BOOKING FUNCTION
       ========================================= */

    // Asynchronous function to handle the booking submission process
    async function confirmBooking() {

        // 1. Gather input data from the frontend UI
        const start = document.getElementById('bookStart').value;
        const end = document.getElementById('bookEnd').value;

        // Retrieve the user's authentication token to prove they are logged in
        const token = localStorage.getItem('token');

        // 2. Validate inputs: Ensure both dates are selected before proceeding
        if (!start || !end) {
            showToast("Please select your rental dates.");
            return; // Stop the function from running further
        }

        // 3. Update UI state: Disable the button to prevent double-clicking/spamming
        const btn = document.getElementById('confirmBtn');
        btn.textContent = 'Processing...';
        btn.disabled = true;

        try {
            // ==========================================
            // API CALL 1: CREATE THE BOOKING (PENDING STATUS)
            // ==========================================
            const createResponse = await fetch(`${API_BASE_URL}/bookings`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}` // Pass the secure token
                },
                body: JSON.stringify({
                    vehicleId: activeVehicle.id, // The ID of the car selected in the modal
                    startDate: start,
                    endDate: end
                })
            });

            // If the creation was successful (HTTP 200-299)
            if (createResponse.ok) {

                // Parse the backend response to get the newly generated Booking Object
                // We need this because it contains the new 'id' generated by the database
                const newBooking = await createResponse.json();

                // ==========================================
                // API CALL 2: AUTO-CONFIRM THE BOOKING (ACTIVE STATUS)
                // ==========================================
                // Immediately hit the confirm endpoint using the newly acquired Booking ID
                const confirmResponse = await fetch(`${API_BASE_URL}/bookings/${newBooking.id}/confirm`, {
                    method: 'PUT', // PUT is used for updates/modifications
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });

                // If the confirmation (activation) was successful
                if (confirmResponse.ok) {
                    showToast(`Booking Confirmed Successfully!`);
                    closeModal(); // Hide the popup

                    // Redirect the user to their profile page to see their new booking
                    setTimeout(() => window.location.href = 'profile.html', 1500);
                } else {
                    // Failsafe: The booking was created in the DB, but failed to activate
                    showToast('Booking created, but failed to activate.');
                }

            } else {
                // Handle errors from the FIRST step (e.g., car is already booked for those dates)
                try {
                    // Attempt to read the specific error message sent by Spring Boot
                    const errorData = await createResponse.json();
                    showToast(errorData.message || 'Failed to create booking.');
                } catch(e) {
                    // Fallback generic error if backend didn't send JSON
                    showToast('Failed to create booking.');
                }
            }

        } catch (error) {
            // Handle severe network errors (e.g., backend server is turned off / no internet)
            showToast('Server error during booking.');
        } finally {
            // 4. Reset UI state: Always turn the button back on, regardless of success or failure
            btn.textContent = 'Confirm Booking';
            btn.disabled = false;
        }
    }

    // 7. EVENT LISTENERS
    document.addEventListener('DOMContentLoaded', () => {
        if (document.getElementById('fleetGrid')) {
            loadFleet();
        }

        document.getElementById('searchName')?.addEventListener('input', applyFilters);
        document.getElementById('filterType')?.addEventListener('change', applyFilters);
        document.getElementById('filterCat')?.addEventListener('change', applyFilters);
        document.getElementById('bookStart')?.addEventListener('change', updateSummary);
        document.getElementById('bookEnd')?.addEventListener('change', updateSummary);
    });