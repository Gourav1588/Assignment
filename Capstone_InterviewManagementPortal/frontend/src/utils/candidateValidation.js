/**
 * Validates candidate create and edit forms.
 
 */

const MAX_RESUME_BYTES = 10 * 1024 * 1024
const MIN_RESUME_BYTES = 100

function isLettersOnly(value) {
    return /^[A-Za-z ]+$/.test(value.trim())
}

function validateName(value, label) {
    if (!value.trim()) {
        return `${label} is required.`
    }

    if (!isLettersOnly(value)) {
        return `${label} must contain only letters.`
    }

    if (value.trim().length > 50) {
        return `${label} must not exceed 50 characters.`
    }

    return null
}

function validateMobile(value) {
    if (!value.trim()) {
        return 'Mobile number is required.'
    }

    if (!/^[6-9]\d{9}$/.test(value.trim())) {
        return 'Mobile number must be exactly 10 digits and start with 6, 7, 8, or 9.'
    }

    return null
}

function validateCompany(value) {
    if (!value.trim()) {
        return 'Current company is required.'
    }

    if (!/[A-Za-z]/.test(value)) {
        return 'Current company must contain at least one letter.'
    }

    if (value.trim().length > 100) {
        return 'Current company must not exceed 100 characters.'
    }

    return null
}

function validateExperience(value) {
    if (value === '' || value === null || value === undefined) {
        return 'Total experience is required.'
    }

    const experience = Number(value)

    if (Number.isNaN(experience)) {
        return 'Total experience must be a valid number.'
    }

    if (experience < 0 || experience > 50) {
        return 'Total experience must be between 0 and 50 years.'
    }

    return null
}

function validateResume(file) {
    if (!file) {
        return 'Resume is required.'
    }

    if (file.type !== 'application/pdf') {
        return 'Resume must be a PDF file.'
    }

    if (file.size < MIN_RESUME_BYTES) {
        return 'Resume file appears to be empty or corrupted.'
    }

    if (file.size > MAX_RESUME_BYTES) {
        return 'Resume must not exceed 10MB.'
    }

    return null
}

/** Validates the candidate registration form. */
export function validateCandidateCreate(form, resumeFile) {
    const firstNameError = validateName(form.first_name, 'First name')
    if (firstNameError) return firstNameError

    const lastNameError = validateName(form.last_name, 'Last name')
    if (lastNameError) return lastNameError

    const email = form.email.trim()

    if (!email) {
        return 'Email is required.'
    }

    const emailRegex = /^[A-Za-z0-9]+([._-][A-Za-z0-9]+)*@[A-Za-z0-9-]+(\.[A-Za-z0-9-]+)+$/

    if (!emailRegex.test(email)) {
        return 'Enter a valid email address.'
    }

    const mobileError = validateMobile(form.mobile_number)
    if (mobileError) return mobileError

    const companyError = validateCompany(form.current_company)
    if (companyError) return companyError

    const experienceError = validateExperience(form.total_experience)
    if (experienceError) return experienceError

    if (!form.applied_job) {
        return 'Please select an applied job.'
    }

    const resumeError = validateResume(resumeFile)
    if (resumeError) return resumeError

    return null
}

/** Validates the candidate profile edit form. Resume and email are not editable. */
export function validateCandidateUpdate(form) {
    const firstNameError = validateName(form.first_name, 'First name')
    if (firstNameError) return firstNameError

    const lastNameError = validateName(form.last_name, 'Last name')
    if (lastNameError) return lastNameError

    const mobileError = validateMobile(form.mobile_number)
    if (mobileError) return mobileError

    const companyError = validateCompany(form.current_company)
    if (companyError) return companyError

    const experienceError = validateExperience(form.total_experience)
    if (experienceError) return experienceError

    return null
}