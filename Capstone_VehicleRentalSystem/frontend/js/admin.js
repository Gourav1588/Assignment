/* =========================================================================
   DriveEasy - Administrator Dashboard Core Logic
   ========================================================================= */

/**
 * INITIALIZATION
 * Validates administrative session and hydrates initial dashboard state.
 */
document.addEventListener('DOMContentLoaded', () => {
    const token = localStorage.getItem('token');

    if (!token) {
        window.location.href = 'login.html';
        return;
    }

    // Trigger parallel data fetching for dashboard statistics
    loadAdminFleet();
    loadAdminBookings();
    loadCategories();
    loadAdminUsers();
});

/* =========================================================================
   TAB NAVIGATION
   ========================================================================= */

/**
 * Manages the visibility of administrative interface sections.
 * @param {string} tabId - The DOM ID of the target section to display.
 * @param {HTMLElement} btn - The navigation button element that triggered the switch.
 */
function switchTab(tabId, btn) {
    // Hide all sections and reset navigation states
    document.querySelectorAll('.admin-tab-section').forEach(t => t.style.display = 'none');
    document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));

    // Activate selected section and update typography
    document.getElementById(tabId).style.display = 'block';
    btn.classList.add('active');
    document.getElementById('page-title').textContent = btn.textContent;

    // Conditionally fetch data based on active view to optimize performance
    if (tabId === 'tab-fleet') loadAdminFleet();
    if (tabId === 'tab-bookings') loadAdminBookings();
    if (tabId === 'tab-users') loadAdminUsers();
}

/* =========================================================================
   DATA FETCHING (READ OPERATIONS)
   ========================================================================= */

/**
 * Retrieves category metadata to populate dropdown select menus.
 */
async function loadCategories() {
    try {
        const res = await apiFetch('/categories');

        if (res.ok) {
            const data = await res.json();
            const optionsHtml = `<option disabled selected>-- Select --</option>` +
                                data.map(c => `<option value="${c.id}">${c.name}</option>`).join('');

            document.getElementById('vCategory').innerHTML = optionsHtml + `<option value="OTHER">+ Add New</option>`;
            document.getElementById('editVCategory').innerHTML = optionsHtml;
        }
    } catch (e) {
        console.error("Category fetch error:", e);
    }
}

/**
 * Fetches the entire vehicle fleet and updates overview statistics.
 * CRITICAL FIX: Now points to the secure /admin endpoint to fetch both Active and Retired vehicles.
 */
async function loadAdminFleet() {
    try {
        // Points to the "Admin Door" we built in the backend
        const res = await apiFetch('/vehicles/admin?page=0&size=100');

        if (res.ok) {
            const data = await res.json();
            const vehicles = data.content || data;

            document.getElementById('adminFleetTable').innerHTML = vehicles.map(v => {
                const isAvailable = v.active || v.isActive;
                const statusBadge = isAvailable ? 'AVAILABLE' : 'UNAVAILABLE';

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

            // Update dashboard metric cards
            document.getElementById('stat-total-cars').textContent = vehicles.length;
            document.getElementById('stat-available').textContent = vehicles.filter(v => v.active || v.isActive).length;
        }
    } catch (e) {
        console.error("Fleet fetch error:", e);
    }
}

/**
 * Fetches the directory of registered users.
 */
async function loadAdminUsers() {
    try {
        const res = await apiFetch('/users');

        if (res.ok) {
            const users = await res.json();
            document.getElementById('adminUsersTable').innerHTML = users.map(u =>
                `<tr>
                    <td>#${u.id}</td>
                    <td>${u.name}</td>
                    <td>${u.email}</td>
                    <td>${u.role}</td>
                </tr>`
            ).join('');
        }
    } catch (e) {
        console.error("User fetch error:", e);
    }
}

/**
 * Fetches global transaction history and active booking statistics.
 */

async function loadAdminBookings() {
    try {
        const res = await apiFetch('/bookings');

        if (res.ok) {
            const data = await res.json();
            const bookings = data.content || data;

            document.getElementById('adminBookingsTable').innerHTML = bookings.map(b =>
                `<tr>
                    <td>#${b.id}</td>
                    <td>${b.vehicleName || `Car #${b.vehicleId}`}</td>

                    <td>${b.startTime}</td>
                    <td>${b.endTime}</td>

                    <td>${b.status}</td>
                </tr>`
            ).join('');

            document.getElementById('stat-active-bookings').textContent = bookings.filter(b => b.status === 'ACTIVE').length;
        }
    } catch (error) {
        console.error("Booking fetch error:", error);
    }
}

/* =========================================================================
   DATA MUTATION (WRITE OPERATIONS)
   ========================================================================= */

/**
 * Processes the creation of a new vehicle entry, handling dynamic category creation if requested.
 * @param {Event} e - The form submission event.
 */
async function submitNewVehicle(e) {
    e.preventDefault();
    const btn = document.getElementById('saveVehicleBtn');
    let catId = document.getElementById('vCategory').value;

    btn.textContent = "Processing...";
    btn.disabled = true;

    try {
        // Resolve dynamic category creation
        if (catId === "OTHER") {
            const name = document.getElementById('vCustomCategory').value;
            const catRes = await apiFetch('/categories', {
                method: 'POST',
                body: JSON.stringify({ name })
            });
            const newCat = await catRes.json();
            catId = newCat.id;
        }

        const vehicleData = {
            name: document.getElementById('vName').value,
            registrationNumber: document.getElementById('regNumber').value,
            type: document.getElementById('vType').value,
            pricePerDay: parseFloat(document.getElementById('vPrice').value),
            description: document.getElementById('vDesc').value,
            categoryId: parseInt(catId)
        };

        const res = await apiFetch('/vehicles', {
            method: 'POST',
            body: JSON.stringify(vehicleData)
        });

        if (res.ok) {
            showToast("Vehicle Added!");
            closeAddModal();
            loadAdminFleet();
            loadCategories();
        } else {
            const errorData = await res.json();
            showToast(errorData.message || "Failed to add vehicle");
        }
    } catch (err) {
        showToast("Server connection failed.");
    } finally {
        btn.textContent = "Save Vehicle";
        btn.disabled = false;
    }
}

/**
 * Modifies an existing vehicle entry.
 * @param {Event} e - The form submission event.
 */
async function submitEditVehicle(e) {
    e.preventDefault();
    const id = document.getElementById('editVehicleId').value;
    const btn = document.getElementById('updateVehicleBtn');

    btn.textContent = "Updating...";
    btn.disabled = true;

    const vehicleData = {
        name: document.getElementById('editVName').value,
        registrationNumber: document.getElementById('editRegNumber').value,
        type: document.getElementById('editVType').value,
        categoryId: parseInt(document.getElementById('editVCategory').value),
        pricePerDay: parseFloat(document.getElementById('editVPrice').value),
        description: document.getElementById('editVDesc').value
    };

    try {
        const res = await apiFetch(`/vehicles/${id}`, {
            method: 'PUT',
            body: JSON.stringify(vehicleData)
        });

        if (res.ok) {
            showToast("Vehicle Updated Successfully!");
            closeEditModal();
            loadAdminFleet();
        } else {
            const errorData = await res.json();
            showToast(errorData.message || "Failed to update vehicle");
        }
    } catch (err) {
        showToast("Server connection failed.");
    } finally {
        btn.textContent = "Save Changes";
        btn.disabled = false;
    }
}

/**
 * Alters the operational status of a vehicle (Active vs Retired).
 * @param {number} id - The vehicle identifier.
 * @param {boolean} currentlyAvailable - The current state.
 */
async function toggleVehicleStatus(id, currentlyAvailable) {
    if (!confirm("Are you sure you wish to modify this vehicle's operational status?")) return;

    try {
        const res = await apiFetch(`/vehicles/${id}/toggle-status`, { method: 'PUT' });

        if (res.ok) {
            showToast("Status updated");
            loadAdminFleet();
            loadAdminBookings();
        } else {
            const errorData = await res.json();
            showToast(errorData.message || "Failed to update vehicle status");
        }
    } catch (error) {
        showToast("Server error execution action.");
    }
}

/* =========================================================================
   UI MODALS & UTILITIES
   ========================================================================= */

function toggleCustomCategory() {
    const isOther = document.getElementById('vCategory').value === 'OTHER';
    document.getElementById('customCategoryDiv').style.display = isOther ? 'flex' : 'none';
    document.getElementById('vCustomCategory').required = isOther;
}

function openAddModal() {
    document.getElementById('addVehicleModal').classList.add('active');
}

function closeAddModal() {
    document.getElementById('addVehicleModal').classList.remove('active');
}

/**
 * Hydrates the edit modal with the targeted vehicle's existing properties.
 * @param {number} id - The vehicle identifier.
 */
async function openEditModal(id) {
    try {
        const res = await apiFetch(`/vehicles/${id}`);

        if (res.ok) {
            const v = await res.json();
            document.getElementById('editVehicleId').value = v.id;
            document.getElementById('editVName').value = v.name;
            document.getElementById('editRegNumber').value = v.registrationNumber;
            document.getElementById('editVType').value = v.type;
            document.getElementById('editVPrice').value = v.pricePerDay;
            document.getElementById('editVDesc').value = v.description || "";

            if (v.category) {
                document.getElementById('editVCategory').value = v.category.id;
            }
            document.getElementById('editVehicleModal').classList.add('active');
        }
    } catch (e) {
        showToast("Error loading vehicle parameters.");
    }
}

function closeEditModal() {
    document.getElementById('editVehicleModal').classList.remove('active');
}

function logout() {
    localStorage.clear();
    window.location.href = 'login.html';
}