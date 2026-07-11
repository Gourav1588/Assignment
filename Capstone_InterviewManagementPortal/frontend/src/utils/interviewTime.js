/**
 * Helpers for reasoning about whether an interview has taken place.
 * Date is stored as "YYYY-MM-DD" and time as "HH:MM".
 */

export function interviewDateTime(interviewDate, interviewTime) {
    return new Date(`${interviewDate}T${interviewTime}`)
}

export function hasInterviewPassed(interviewDate, interviewTime) {
    return new Date() > interviewDateTime(interviewDate, interviewTime)
}