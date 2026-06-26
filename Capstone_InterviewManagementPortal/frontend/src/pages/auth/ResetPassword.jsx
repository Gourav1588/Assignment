import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import authService from '../../services/authService'
import { useAuth } from '../../context/AuthContext'
import { loadSession } from '../../utils/auth'
import { ROUTES } from '../../constants/route'
import './Auth.css'

export default function ResetPassword() {
  const [newPassword, setNewPassword]         = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [error, setError]                     = useState('')
  const [loading, setLoading]                 = useState(false)

  const navigate  = useNavigate()
  const { login } = useAuth()

  async function handleSubmit(e) {
    e.preventDefault()
    setError('')

    if (newPassword !== confirmPassword) {
      setError('Passwords do not match.')
      return
    }

    setLoading(true)
    try {
   
      await authService.resetPassword(newPassword)

     
      const session = loadSession()
      if (session?.email) {
        await login(session.email, newPassword)
      }

      
      navigate(ROUTES.DASHBOARD)

    } catch (err) {
      const errors = err.response?.data?.errors
      if (errors?.length) {
        setError(errors[0].message)
      } else {
        setError(err.response?.data?.detail || 'Something went wrong.')
      }
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="auth-container">
      <div className="auth-card">
        <h2 className="auth-title">Set New Password</h2>
        <p className="auth-subtitle">
          First login detected. Please set a new password to continue.
        </p>

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>New Password</label>
            <input
              type="password"
              value={newPassword}
              onChange={(e) => setNewPassword(e.target.value)}
              placeholder="Min 6 chars, letter + number + special char"
              required
            />
          </div>

          <div className="form-group">
            <label>Confirm Password</label>
            <input
              type="password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              placeholder="Repeat new password"
              required
            />
          </div>

          {error && <div className="error-msg">{error}</div>}

          <button type="submit" className="btn-primary" disabled={loading}>
            {loading ? 'Saving...' : 'Set Password'}
          </button>
        </form>
      </div>
    </div>
  )
}