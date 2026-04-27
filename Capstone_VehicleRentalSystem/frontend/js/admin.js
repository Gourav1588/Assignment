// Run after page loads
document.addEventListener('DOMContentLoaded', () => {

    // Check login token → redirect if not logged in
    const token = localStorage.getItem('token');
    if (!token) {
        window.location.href = 'login.html';
        return;
    }

    // Initial data load for dashboard
    loadAdminFleet();
    loadAdminBookings();
    loadCategories();
    loadAdminUsers();
});


// =========================================
// TAB SWITCHING
// =========================================

// Switch between admin tabs (fleet, bookings, users)
function switchTab(tabId, btn) {

    // Hide all sections
    document.querySelectorAll('.admin-tab-section')
        .forEach(t => t.style.display = 'none');

    // Remove active state from buttons
    document.querySelectorAll('.nav-btn')
        .forEach(b => b.classList.remove('active'));

    // Show selected tab
    document.getElementById(tabId).style.display = 'block';

    // Highlight active button
    btn.classList.add('active');

    // Update page title dynamically
    document.getElementById('page-title').textContent = btn.textContent;

    // Load data only when needed
    if (tabId === 'tab-fleet') loadAdminFleet();
    if (tabId === 'tab-bookings') loadAdminBookings();
    if (tabId === 'tab-users') loadAdminUsers();
}


// =========================================
// CATEGORY HANDLING
// =========================================

// Load categories into dropdown
async function loadCategories() {
    try {
        const res = await fetch(`${API_BASE_URL}/categories`, {
            headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
        });

        if (res.ok) {
            const data = await res.json();

            // Populate dropdown options
            const dropdown = document.getElementById('vCategory');
            dropdown.innerHTML =
                `<option disabled selected>-- Select --</option>` +
                data.map(c => `<option value="${c.id}">${c.name}</option>`).join('') +
                `<option value="OTHER">+ Add New</option>`;
        }
    } catch (e) {
        console.error("Category load error", e);
    }
}

// Toggle custom category input when "Other" selected
function toggleCustomCategory() {
    const isOther = document.getElementById('vCategory').value === 'OTHER';

    document.getElementById('customCategoryDiv').style.display =
        isOther ? 'flex' : 'none';

    document.getElementById('vCustomCategory').required = isOther;
}


// =========================================
// ADD VEHICLE
// =========================================

// Submit new vehicle form
async function submitNewVehicle(e) {
    e.preventDefault();

    const btn = document.getElementById('saveVehicleBtn');
    let catId = document.getElementById('vCategory').value;
    const token = localStorage.getItem('token');

    btn.textContent = "Processing...";
    btn.disabled = true;

    try {
        // If "Other" → create category first
        if (catId === "OTHER") {
            const name = document.getElementById('vCustomCategory').value;

            const catRes = await fetch(`${API_BASE_URL}/categories`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({ name })
            });

            const newCat = await catRes.json();
            catId = newCat.id;
        }

        // Prepare vehicle data
        const vehicleData = {
            name: document.getElementById('vName').value,
            type: document.getElementById('vType').value,
            pricePerDay: parseFloat(document.getElementById('vPrice').value),
            description: document.getElementById('vDesc').value,
            categoryId: parseInt(catId)
        };

        // Send API request
        const res = await fetch(`${API_BASE_URL}/vehicles`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(vehicleData)
        });

        if (res.ok) {
            showToast("Vehicle Added!");

            // Refresh UI after success
            closeAddModal();
            loadAdminFleet();
            loadCategories();

        } else {
            showToast("Failed to add vehicle");
        }

    } catch (err) {
        showToast("Server connection failed.");
    } finally {
        btn.textContent = "Save Vehicle";
        btn.disabled = false;
    }
}


// =========================================
// LOAD VEHICLES + STATS
// =========================================

// Fetch vehicles and update dashboard
async function loadAdminFleet() {
    const res = await fetch(`${API_BASE_URL}/vehicles?page=0&size=100`, {
        headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
    });

    if (res.ok) {
        const data = await res.json();
        const vehicles = data.content || data;

        // Render table rows
        document.getElementById('adminFleetTable').innerHTML =
            vehicles.map(v => {
                const isAvailable = v.active || v.isActive;

                // Status label
                const statusBadge = isAvailable ? 'AVAILABLE' : 'UNAVAILABLE';

                // Action button
               // Action button
                  const actionButton = isAvailable
                   ? `<button class="action-btn delete" onclick="toggleVehicleStatus(${v.id}, true)">Retire</button>`
                      : `<button class="action-btn activate" onclick="toggleVehicleStatus(${v.id}, false)">Activate</button>`;

                return `<tr>
                    <td>#${v.id}</td>
                    <td>${v.name}</td>
                    <td>${v.type}</td>
                    <td>₹${v.pricePerDay}</td>
                    <td>${statusBadge}</td>
                    <td>${actionButton}</td>
                </tr>`;
            }).join('');

        // Update stats
        document.getElementById('stat-total-cars').textContent = vehicles.length;
        document.getElementById('stat-available').textContent =
            vehicles.filter(v => v.active || v.isActive).length;
    }
}


// =========================================
// LOAD USERS
// =========================================

// Fetch and display all users
async function loadAdminUsers() {
    const res = await fetch(`${API_BASE_URL}/users`, {
        headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
    });

    if (res.ok) {
        const users = await res.json();

        document.getElementById('adminUsersTable').innerHTML =
            users.map(u =>
                `<tr>
                    <td>#${u.id}</td>
                    <td>${u.name}</td>
                    <td>${u.email}</td>
                    <td>${u.role}</td>
                </tr>`
            ).join('');
    }
}


// =========================================
// LOAD BOOKINGS + STATS
// =========================================

// Fetch bookings and update dashboard stats
async function loadAdminBookings() {
    try {
        const res = await fetch(`${API_BASE_URL}/bookings`, {
            headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
        });

        if (res.ok) {
            const data = await res.json();
            const bookings = data.content || data;

            // Render booking table
            document.getElementById('adminBookingsTable').innerHTML =
                bookings.map(b =>
                    `<tr>
                        <td>#${b.id}</td>
                        <td>${b.vehicleName || `Car #${b.vehicleId}`}</td>
                        <td>${b.startDate}</td>
                        <td>${b.endDate}</td>
                        <td>${b.status}</td>
                    </tr>`
                ).join('');

            // Update active bookings count
            document.getElementById('stat-active-bookings').textContent =
                bookings.filter(b => b.status === 'ACTIVE').length;
        }

    } catch (error) {
        console.error("Booking Fetch Error", error);
    }
}


// =========================================
// TOGGLE VEHICLE STATUS
// =========================================

// Activate / retire vehicle
async function toggleVehicleStatus(id, currentlyAvailable) {

    // Confirm action before API call
    if (!confirm("Are you sure?")) return;

    try {
        const res = await fetch(`${API_BASE_URL}/vehicles/${id}/toggle-status`, {
            method: 'PUT',
            headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
        });

        if (res.ok) {
            showToast("Status updated");

            // Refresh UI
            loadAdminFleet();
            loadAdminBookings();

        } else {
            try {
                    const errorData = await res.json();
                     // Show the specific message from Spring Boot
                      showToast(errorData.message || "Failed to update vehicle status");
                 } catch (parseError) {
                            showToast("Update failed");
                  }
        }

    } catch (error) {
        showToast("Server error");
    }
}


// =========================================
// MODAL + LOGOUT
// =========================================

// Open add vehicle modal
function openAddModal() {
    document.getElementById('addVehicleModal').classList.add('active');
}

// Close modal
function closeAddModal() {
    document.getElementById('addVehicleModal').classList.remove('active');
}

// Logout user
function logout() {
    localStorage.clear(); // Remove token
    window.location.href = 'login.html'; // Redirect
}