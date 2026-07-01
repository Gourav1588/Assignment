import axios from 'axios'
import { loadSession, clearSession, buildBasicAuthHeader } from '../utils/auth'

const api = axios.create({
  baseURL: '/api/v1',
  headers: { 'Content-Type': 'application/json' },
})

// Attach Basic Auth header on every request automatically
api.interceptors.request.use((config) => {
  const session = loadSession()
  if (session?.email && session?.password) {
    config.headers['Authorization'] = buildBasicAuthHeader(
      session.email,
      session.password
    )
  }
  return config
})

// Handle 401 globally — clear session and redirect to login
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      clearSession()
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export default api