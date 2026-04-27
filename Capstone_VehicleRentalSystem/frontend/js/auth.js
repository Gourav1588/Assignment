// =========================================
// AUTH SCRIPT
// =========================================

// ─── LOGIN ───
const loginForm = document.getElementById('loginForm');

if (loginForm) {
    loginForm.addEventListener('submit', async function(e) {
        e.preventDefault(); // Stop page reload

        // Get input values
        const email = document.getElementById('loginEmail').value;
        const password = document.getElementById('loginPassword').value;
        const btn = document.getElementById('loginBtn');

        // Show loading state
        if (btn) {
            btn.textContent = 'Authenticating...';
            btn.disabled = true;
        }

        try {
            // Send login request
            const response = await fetch(`${API_BASE_URL}/auth/login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password })
            });

            if (response.ok) {
                const data = await response.json();

                // Extract token safely
                const token = data.data || data.token || data.jwt;

                // Store token for future requests
                if (window.localStorage) {
                    localStorage.setItem('token', token);
                    localStorage.setItem('userEmail', email);
                }

                showToast('Login successful!');

                // Decode role and redirect accordingly
                const role = getRoleFromToken(token);

                setTimeout(() => {
                    if (role === 'ADMIN' || role === 'ROLE_ADMIN') {
                        window.location.href = 'admin.html';
                    } else {
                        window.location.href = 'vehicles.html';
                    }
                }, 1500);

            } else {
                // Handle invalid credentials
                showToast('Invalid email or password');

                // Reset button
                if (btn) {
                    btn.textContent = 'Sign In';
                    btn.disabled = false;
                }
            }

        } catch (error) {
            // Handle network errors
            console.error(error);
            showToast('Server error');

            // Reset button
            if (btn) {
                btn.textContent = 'Sign In';
                btn.disabled = false;
            }
        }
    });
}


// ─── REGISTER ───
const registerForm = document.getElementById('registerForm');

if (registerForm) {
    registerForm.addEventListener('submit', async function(e) {
        e.preventDefault(); // Stop reload

        // Get input values
        const name = document.getElementById('regName').value;
        const email = document.getElementById('regEmail').value;
        const password = document.getElementById('regPassword').value;
        const btn = document.getElementById('regBtn');

        // Show loading
        if (btn) {
            btn.textContent = 'Creating...';
            btn.disabled = true;
        }

        try {
            // Send register request
            const response = await fetch(`${API_BASE_URL}/auth/register`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name, email, password })
            });

            if (response.ok) {
                // Success → go to login
                showToast('Account created');
                setTimeout(() => window.location.href = 'login.html', 1500);

            } else {
                // Show error message
                showToast('Registration failed');

                // Reset button
                if (btn) {
                    btn.textContent = 'Create Account';
                    btn.disabled = false;
                }
            }

        } catch (error) {
            // Network failure
            console.error(error);
            showToast('Server error');

            // Reset button
            if (btn) {
                btn.textContent = 'Create Account';
                btn.disabled = false;
            }
        }
    });
}


// ─── TOKEN ROLE EXTRACTOR ───
function getRoleFromToken(token) {
    if (!token) return 'USER'; // Default role

    try {
        // Decode JWT payload
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

        // Extract role from payload
        if (payload.role) return payload.role;
        if (payload.roles) return payload.roles[0];
        if (payload.authorities) return payload.authorities[0];

        return 'USER';

    } catch (error) {
        console.error("Token decode error:", error);
        return 'USER'; // Fallback
    }
}