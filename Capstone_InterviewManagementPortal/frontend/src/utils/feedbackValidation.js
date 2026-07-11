/**
 * Validates feedback submission form.
 */

function isNumbersOnly(value) {
    return /^\d+$/.test(value.trim())
}

function validateRating(value, label) {
    if (value === '' || value === null || value === undefined) {
        return `${label} is required.`
    }

    const rating = Number(value)

    if (!Number.isInteger(rating)) {
        return `${label} must be a whole number.`
    }

    if (rating < 1 || rating > 5) {
        return `${label} must be between 1 and 5.`
    }

    return null
}

export function validateFeedback(form) {
    const technicalError = validateRating(form.technical_rating, 'Technical rating')
    if (technicalError) return technicalError

    const communicationError = validateRating(form.communication_rating, 'Communication rating')
    if (communicationError) return communicationError

    const problemSolvingError = validateRating(form.problem_solving, 'Problem solving rating')
    if (problemSolvingError) return problemSolvingError

    if (!form.tech_areas_covered.trim()) {
        return 'Tech areas covered is required.'
    }

    if (isNumbersOnly(form.tech_areas_covered)) {
        return 'Tech areas covered cannot contain only numbers.'
    }

    if (form.tech_areas_covered.trim().length > 500) {
        return 'Tech areas covered must not exceed 500 characters.'
    }

    if (!form.comments.trim()) {
        return 'Comments are required.'
    }

    if (isNumbersOnly(form.comments)) {
        return 'Comments cannot contain only numbers.'
    }

    if (form.comments.trim().length > 1000) {
        return 'Comments must not exceed 1000 characters.'
    }

    if (!form.recommendation) {
        return 'Please select a recommendation.'
    }

    return null
}