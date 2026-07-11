/**
 * Validates interview scheduling form.
 */

function isNumbersOnly(value) {
    return /^\d+$/.test(value.trim())
}

export function validateInterview(form) {
    if (!form.candidate_id) {
        return 'Please select a candidate.'
    }

    if (!form.job_title.trim()) {
        return 'Job title is required.'
    }

    if (form.job_title.trim().length < 2) {
        return 'Job title must be at least 2 characters.'
    }

    if (isNumbersOnly(form.job_title)) {
        return 'Job title cannot contain only numbers.'
    }

    if (!form.interview_date) {
        return 'Interview date is required.'
    }

    const selectedDate = new Date(form.interview_date)
    const today = new Date()
    today.setHours(0, 0, 0, 0)

    if (selectedDate < today) {
        return 'Interview date cannot be in the past.'
    }

    const maxDate = new Date()
    maxDate.setDate(today.getDate() + 30)
    maxDate.setHours(23, 59, 59, 999)

    if (selectedDate > maxDate) {
        return 'Interview date cannot be more than 1 month in the future.'
    }

    if (!form.interview_time) {
        return 'Interview time is required.'
    }

    const [hour, minute] = form.interview_time.split(':').map(Number)

    if (hour < 9 || hour > 18 || (hour === 18 && minute > 0)) {
        return 'Interview time must be between 09:00 AM and 06:00 PM.'
    }

    if (!form.interviewer_id) {
        return 'Please select an interviewer.'
    }

    if (!form.focus_areas.trim()) {
        return 'Focus areas are required.'
    }

    if (form.focus_areas.trim().length < 2) {
        return 'Focus areas must be at least 2 characters.'
    }

    if (isNumbersOnly(form.focus_areas)) {
        return 'Focus areas cannot contain only numbers.'
    }

    return null
}