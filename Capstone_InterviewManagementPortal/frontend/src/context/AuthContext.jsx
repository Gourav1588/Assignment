import { createContext, useContext, useState, useEffect } from 'react'
import authService from '../services/authService'
import { saveSession, loadSession, clearSession, buildBasicAuthHeader } from '../utils/auth'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const session = loadSession()

    if (session?.user) {
      setUser(session.user)
    }

    setLoading(false)
  }, [])

  async function login(email, password) {
    const userData = await authService.login(email, password)
    const authHeader = buildBasicAuthHeader(email, password)
    saveSession(userData, authHeader)
    setUser(userData)

    return userData
  }

  function logout() {
    clearSession()
    setUser(null)

  }

  return (
    <AuthContext.Provider value={{ user, login, logout, loading }}>
      {children}
    </AuthContext.Provider>
  )
}

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used inside AuthProvider')
  }
  return context
}