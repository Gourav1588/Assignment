/**
 * Global Configuration & Core Utilities
 * Centralizes backend communication, session management, and shared UI components.
 * This file must be loaded BEFORE any feature-specific scripts.
 */

/* =========================================================================
   1. NETWORK & API CONFIGURATION
   ========================================================================= */

const API_BASE_URL = "http://localhost:8080/api";

/**
 * apiFetch - A standardized wrapper for the native Fetch API.
 * Automatically handles JWT injection, Base URL, and session expiration.
 * * @param {string} endpoint - The target API route (e.g., '/vehicles').
 * @param {Object} options - Standard fetch options (method, body, headers).
 * @returns {Promise<Response>} The raw response from the server.
 */
async function apiFetch(endpoint, options = {}) {
    const token = localStorage.getItem('token');

    // Set default headers and merge with custom options
    const headers = {
        'Content-Type': 'application/json',
        ...(options.headers || {})
    };

    // Inject Bearer token if user session exists
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }

    const config = {
        ...options,
        headers
    };

    const response = await fetch(`${API_BASE_URL}${endpoint}`, config);

    // Global session handling: Redirect to login if token is expired
    if (response.status === 401 && !endpoint.includes('/auth')) {
        console.warn("Session expired. Clearing credentials.");
        localStorage.clear();
        window.location.href = 'login.html';
    }

    return response;
}

/* =========================================================================
   2. GLOBAL UI COMPONENTS
   ========================================================================= */

/**
 * Displays a temporary feedback notification (Toast) to the user.
 * * @param {string} message - The text content to display.
 */
function showToast(message) {
    const toast = document.getElementById('toast');
    if (!toast) {
        console.warn("Toast element not found in the DOM.");
        return;
    }

    toast.textContent = message;
    toast.classList.add('show');

    // Auto-hide after 3 seconds
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}