/**
 * Validates job creation/update form.
 * Rules:
 * - Title is required and must be at least 2 characters
 * - Role is required and must be at least 2 characters
 * - Details are required and must be at least 10 characters
 * - Required skills are required and must be at least 2 characters
 * - Experience is required and must be a non-negative number
 * - Location is required and must be at least 2 characters
 *
 * @param {Object} form Job form data.
 * @returns {string|null} Validation error message or null if valid.
 */


export function validateJob(form) {
    if (!form.title.trim()) {
        return 'Job title is required.'
    }

    if (form.title.trim().length < 2) {
        return 'Job title must be at least 2 characters.'
    }

    if (!form.role.trim()) {
        return 'Job role is required.'
    }

    if (form.role.trim().length < 2) {
        return 'Job role must be at least 2 characters.'
    }

    if (!form.details.trim()) {
        return 'Job details are required.'
    }

    if (form.details.trim().length < 10) {
        return 'Job details must be at least 10 characters.'
    }

    if (!form.required_skills.trim()) {
        return 'Required skills are required.'
    }

    if (form.required_skills.trim().length < 2) {
        return 'Required skills must be at least 2 characters.'
    }

    if (form.experience_required === '') {
        return 'Experience required is required.'
    }

    const experience = Number(form.experience_required)

    if (Number.isNaN(experience) || experience < 0) {
        return 'Experience required must be a valid positive number.'
    }

    if (experience < 0 || experience > 50) {
        return 'Experience required must be between 0 and 50 years.'
    }

    if (!form.location.trim()) {
        return 'Location is required.'
    }

    if (form.location.trim().length < 2) {
        return 'Location must be at least 2 characters.'
    }

    return null
}