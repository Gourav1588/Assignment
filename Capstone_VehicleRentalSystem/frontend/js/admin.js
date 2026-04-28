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

                    const optionsHtml = `<option disabled selected>-- Select --</option>` +
                                        data.map(c => `<option value="${c.id}">${c.name}</option>`).join('');

                    // Populate the "Add" dropdown
                    document.getElementById('vCategory').innerHTML = optionsHtml + `<option value="OTHER">+ Add New</option>`;

                    // Populate the "Edit" dropdown
                    document.getElementById('editVCategory').innerHTML = optionsHtml;
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
            registrationNumber: document.getElementById('regNumber').value,
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

                      const errorData = await res.json();
                      console.log("Raw Add Vehicle Error:", errorData);

                      // Extract the message
                      const realMessage = errorData.message
                                       || "Failed to add vehicle";

                      showToast(realMessage);
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
console.log(res);
    if (res.ok) {
        const data = await res.json();
        const vehicles = data.content || data;

        // Render table rows
        document.getElementById('adminFleetTable').innerHTML =
            vehicles.map(v => {
                const isAvailable = v.active || v.isActive;

                // Status label
                const statusBadge = isAvailable ? 'AVAILABLE' : 'UNAVAILABLE';



                 // Action buttons
                                 const actionButton = `
                                     <button class="action-btn" onclick="openEditModal(${v.id})" style="background: #f59e0b; color: white; border: none; padding: 4px 8px; border-radius: 4px; cursor: pointer; margin-right: 5px;">Edit</button>
                                     ${isAvailable
                                         ? `<button class="action-btn delete" onclick="toggleVehicleStatus(${v.id}, true)">Retire</button>`
                                         : `<button class="action-btn activate" onclick="toggleVehicleStatus(${v.id}, false)">Activate</button>`}
                                 `;

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

// =========================================
// EDIT VEHICLE LOGIC
// =========================================

// 1. Fetch data and open the modal
async function openEditModal(id) {
    try {
        const res = await fetch(`${API_BASE_URL}/vehicles/${id}`, {
            headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
        });

        if (res.ok) {
            const v = await res.json();

            // Populate the form inputs with the existing data
            document.getElementById('editVehicleId').value = v.id;
            document.getElementById('editVName').value = v.name;
            document.getElementById('editRegNumber').value = v.registrationNumber;
            document.getElementById('editVType').value = v.type;
            document.getElementById('editVPrice').value = v.pricePerDay;
            document.getElementById('editVDesc').value = v.description || "";

            if (v.category) {
                document.getElementById('editVCategory').value = v.category.id;
            }

            // Show the modal
            document.getElementById('editVehicleModal').classList.add('active');
        }
    } catch (e) {
        showToast("Error loading vehicle details");
    }
}

// 2. Close the modal
function closeEditModal() {
    document.getElementById('editVehicleModal').classList.remove('active');
}

// 3. Submit the changes to the backend
async function submitEditVehicle(e) {
    e.preventDefault();

    const id = document.getElementById('editVehicleId').value;
    const btn = document.getElementById('updateVehicleBtn');
    btn.textContent = "Updating...";
    btn.disabled = true;

    // Package the updated data
    const vehicleData = {
        name: document.getElementById('editVName').value,
        registrationNumber: document.getElementById('editRegNumber').value,
        type: document.getElementById('editVType').value,
        categoryId: parseInt(document.getElementById('editVCategory').value),
        pricePerDay: parseFloat(document.getElementById('editVPrice').value),
        description: document.getElementById('editVDesc').value
    };

    try {
        const res = await fetch(`${API_BASE_URL}/vehicles/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            },
            body: JSON.stringify(vehicleData)
        });

        if (res.ok) {
            showToast("Vehicle Updated Successfully!");
            closeEditModal();
            loadAdminFleet(); // Refresh the table
        } else {
            const errorData = await res.json();
            console.log(errorData)
            showToast(errorData.message || "Failed to update vehicle");
        }
    } catch (err) {
        showToast("Server connection failed.");
    } finally {
        btn.textContent = "Save Changes";
        btn.disabled = false;
    }
}

// Logout user
function logout() {
    localStorage.clear(); // Remove token
    window.location.href = 'login.html'; // Redirect
}