/* =========================================================================
   DriveEasy - Identity & Access Management
   ========================================================================= */

const loginForm = document.getElementById('loginForm');
const registerForm = document.getElementById('registerForm');

/* =========================================================================
   AUTHENTICATION WORKFLOWS
   ========================================================================= */

/**
 * Processes authentication credentials and initiates user sessions.
 * Decodes access tokens to route users to context-appropriate dashboards.
 */
if (loginForm) {
    loginForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        const btn = document.getElementById('loginBtn');

        const credentials = {
            email: document.getElementById('loginEmail').value,
            password: document.getElementById('loginPassword').value
        };

        if (btn) {
            btn.textContent = 'Authenticating...';
            btn.disabled = true;
        }

        try {
            // Utilizing global apiFetch utility
            const response = await apiFetch('/auth/login', {
                method: 'POST',
                body: JSON.stringify(credentials)
            });

            if (response.ok) {
                const data = await response.json();
                const token = data.data || data.token || data.jwt;

                if (window.localStorage) {
                    localStorage.setItem('token', token);
                    localStorage.setItem('userEmail', credentials.email);
                }

                showToast('Authentication successful.');
                const role = getRoleFromToken(token);

                // Conditional routing based on authorization level
                setTimeout(() => {
                    if (role === 'ADMIN' || role === 'ROLE_ADMIN') {
                        window.location.href = 'admin.html';
                    } else {
                        window.location.href = 'vehicles.html';
                    }
                }, 1500);

            } else {
                showToast('Invalid credentials provided.');
                if (btn) {
                    btn.textContent = 'Sign In';
                    btn.disabled = false;
                }
            }
        } catch (error) {
            console.error("Authentication Service Error:", error);
            showToast('Service currently unavailable.');
            if (btn) {
                btn.textContent = 'Sign In';
                btn.disabled = false;
            }
        }
    });
}

/**
 * Processes new identity registration requests.
 */
if (registerForm) {
    registerForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        const btn = document.getElementById('regBtn');

        const registrationPayload = {
            name: document.getElementById('regName').value,
            email: document.getElementById('regEmail').value,
            password: document.getElementById('regPassword').value
        };

        if (btn) {
            btn.textContent = 'Provisioning...';
            btn.disabled = true;
        }

        try {
            const response = await apiFetch('/auth/register', {
                method: 'POST',
                body: JSON.stringify(registrationPayload)
            });

            if (response.ok) {
                showToast('Identity successfully provisioned.');
                setTimeout(() => window.location.href = 'login.html', 1500);
            } else {
                showToast('Registration failed to process.');
                if (btn) {
                    btn.textContent = 'Create Account';
                    btn.disabled = false;
                }
            }
        } catch (error) {
            console.error("Registration Service Error:", error);
            showToast('Service currently unavailable.');
            if (btn) {
                btn.textContent = 'Create Account';
                btn.disabled = false;
            }
        }
    });
}

/* =========================================================================
   SECURITY UTILITIES
   ========================================================================= */

/**
 * Extracts and decodes authorization roles directly from the JWT payload.
 * Provides a synchronous mechanism for routing decisions prior to backend validation.
 *
 * @param {string} token - The raw JSON Web Token string.
 * @returns {string} The parsed operational role (e.g., 'ADMIN', 'USER').
 */
function getRoleFromToken(token) {
    if (!token) return 'USER';

    try {
        const base64 = token.split('.')[1]
            .replace(/-/g, '+')
            .replace(/_/g, '/');

        const payload = JSON.parse(
            decodeURIComponent(
                atob(base64).split('').map(c =>
                    '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2)
                ).join('')
            )
        );

        if (payload.role) return payload.role;
        if (payload.roles) return payload.roles[0];
        if (payload.authorities) return payload.authorities[0];

        return 'USER';
    } catch (error) {
        console.error("Token decode sequence failure:", error);
        return 'USER';
    }
}

/* =========================================================================
   REVERSE AUTH GUARD
   Immediately redirects logged-in users away from auth pages.
   ========================================================================= */
(function redirectIfLoggedIn() {
    const token = localStorage.getItem('token');

    if (token) {
        // Since we already have the getRoleFromToken function in this file,
        // we can use it to send Admins and Users to their correct dashboards.
        const role = getRoleFromToken(token);

        if (role === 'ADMIN' || role === 'ROLE_ADMIN') {
            window.location.replace('admin.html');
        } else {
            window.location.replace('vehicles.html');
        }
    }
})();