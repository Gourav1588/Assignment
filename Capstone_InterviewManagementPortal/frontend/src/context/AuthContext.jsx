import { createContext, useContext, useState, useEffect } from 'react'
import authService from '../services/authService'
import { saveSession, loadSession, clearSession ,buildBasicAuthHeader} from '../utils/auth'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser]               = useState(null)
  const [pendingUser, setPendingUser] = useState(null)
  const [loading, setLoading]         = useState(true)

  useEffect(() => {
    const session = loadSession()
    if (session?.user) {
      if (session.user.is_password_reset_pending) {
        setPendingUser(session.user)
      } else {
        setUser(session.user)
      }
    }
    setLoading(false)
  }, [])

  async function login(email, password) {
    const userData = await authService.login(email, password)
      const authHeader = buildBasicAuthHeader(email, password)
       saveSession(userData, authHeader)

    if (userData.is_password_reset_pending) {
      setPendingUser(userData)
      setUser(null)
    } else {
      setUser(userData)
      setPendingUser(null)
    }

    return userData
  }

  function logout() {
    clearSession()
    setUser(null)
    setPendingUser(null)
  }

  return (
    <AuthContext.Provider value={{ user, pendingUser, login, logout, loading }}>
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