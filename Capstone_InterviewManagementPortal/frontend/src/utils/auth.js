const STORAGE_KEY = 'imp_user'

export function buildBasicAuthHeader(email, password) {
  const encoded = btoa(`${email}:${password}`)
  return `Basic ${encoded}`
}

export function saveSession(user, email, password) {
  sessionStorage.setItem(STORAGE_KEY, JSON.stringify({ user, email, password }))
}

export function loadSession() {
  try {
    const raw = sessionStorage.getItem(STORAGE_KEY)
    return raw ? JSON.parse(raw) : null
  } catch {
    return null
  }
}

export function clearSession() {
  sessionStorage.removeItem(STORAGE_KEY)
}