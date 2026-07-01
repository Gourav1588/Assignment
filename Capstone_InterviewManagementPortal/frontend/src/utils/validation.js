/**
 * Validates password complexity.
 * Rules:
 * - 6 to 12 characters
 * - At least one letter
 * - At least one number
 * - At least one special character (@$!%*#?&)
 *
 * @param {string} password
 * @returns {string|null} Validation error message or null if valid.
 */
export function validatePassword(password) {
    if (!password) {
        return 'Password is required.'
    }

    if (password.length < 6 || password.length > 12) {
        return 'Password must be between 6 and 12 characters long.'
    }

    if (!/[A-Za-z]/.test(password)) {
        return 'Password must contain at least one letter.'
    }

    if (!/\d/.test(password)) {
        return 'Password must contain at least one number.'
    }

    if (!/[@$!%*#?&]/.test(password)) {
        return 'Password must contain at least one special character (@$!%*#?&).'
    }

    return null
}