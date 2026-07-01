const STORAGE_KEY = 'imp_user'

export function buildBasicAuthHeader(email, password) {
  const encoded = btoa(`${email}:${password}`)
  return `Basic ${encoded}`
}

export function saveSession(user, authHeader) {
  sessionStorage.setItem(STORAGE_KEY, JSON.stringify({
    user,
    authHeader   
  }))
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