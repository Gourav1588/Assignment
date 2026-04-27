// js/profile.js

// 1. DASHBOARD INITIALIZATION
document.addEventListener('DOMContentLoaded', () => {
    const token = localStorage.getItem('token');

    // Safety check: redirect if user is not logged in
    if (!token) {
        window.location.href = 'login.html';
        return;
    }

    // Set welcome name (extracting from JWT subject if possible)
    try {
        const payload = JSON.parse(atob(token.split('.')[1]));
        document.getElementById('userNameDisplay').textContent = payload.sub.split('@')[0];
    } catch (e) {
        document.getElementById('userNameDisplay').textContent = "User";
    }

    loadUserBookings();
});

// 2. FETCH DATA FROM BOOKING SERVICE
async function loadUserBookings() {
    const token = localStorage.getItem('token');
    const container = document.getElementById('bookingsContainer');

    try {
        // Targets /api/bookings/my as defined in your BookingController
        const response = await fetch(`${API_BASE_URL}/bookings/my?page=0&size=10`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`, // Pass JWT for security
                'Content-Type': 'application/json'
            }
        });

        if (response.ok) {
            const pageData = await response.json();
            // Spring Data Page puts the list inside 'content'
            const bookings = pageData.content || [];
            renderBookings(bookings);
        } else {
            console.error("Fetch Error:", response.status);
            showToast("Failed to load your booking history.");
        }
    } catch (error) {
        console.error("Dashboard Connection Error:", error);
        showToast("Unable to connect to the server.");
    }
}

// 3. DYNAMIC UI RENDERING
function renderBookings(bookings) {
    const container = document.getElementById('bookingsContainer');

    if (bookings.length === 0) {
        container.innerHTML = `
            <div style="text-align:center; padding: 40px; color: var(--muted);">
                <p>You haven't made any bookings yet.</p>
                <a href="vehicles.html" class="btn-accent" style="display:inline-block; margin-top:15px; text-decoration:none;">Explore Vehicles</a>
            </div>`;
        return;
    }

    // Maps BookingResponse fields: vehicleName, id, startDate, endDate, status, totalCost
    container.innerHTML = bookings.map(b => {
        const statusClass = b.status ? b.status.toLowerCase() : 'pending';

        return `
            <div class="booking-card">
                <div class="booking-details">
                    <div class="booking-icon">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <path d="M14 16H9m10 0h3v-3.15a1 1 0 0 0-.84-.99L16 11l-2.7-3.6a1 1 0 0 0-.8-.4H5.24a2 2 0 0 0-1.8 1.1l-1.4 3.1A1.5 1.5 0 0 0 2 12v4h3"/>
                            <circle cx="6.5" cy="16.5" r="2.5"/><circle cx="16.5" cy="16.5" r="2.5"/>
                        </svg>
                    </div>
                    <div class="booking-info">
                        <h4>${b.vehicleName}</h4>
                        <p>Booking ID: #BK-${b.id}</p>
                        <div class="dates">${b.startDate} ➔ ${b.endDate}</div>
                    </div>
                </div>
                <div class="booking-status">
                    <div class="status-badge status-${statusClass}">${b.status}</div>
                    <div class="booking-price">₹${b.totalCost.toLocaleString()}</div>
                </div>
            </div>
        `;
    }).join('');
}

// 4. TAB NAVIGATION
function switchTab(tabId) {
    // 1. Reset: Turn OFF the active class on ALL buttons and tabs
    document.querySelectorAll('.dash-link').forEach(btn => btn.classList.remove('active'));
    document.querySelectorAll('.tab-pane').forEach(pane => pane.classList.remove('active'));

    // 2. Apply: Turn ON the active class for the specific button and tab
    document.getElementById('btn-' + tabId).classList.add('active');
    document.getElementById(tabId).classList.add('active');
}

// 5. LOGOUT
function handleLogout() {
    localStorage.removeItem('token');
    showToast("Logging out...");
    setTimeout(() => window.location.href = 'index.html', 1000);
}