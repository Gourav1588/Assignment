import { useState } from 'react'
import authService from '../../services/authService'
import { useAuth } from '../../context/AuthContext'
import { useNavigate } from 'react-router-dom'
import { loadSession } from '../../utils/auth'
import { ROUTES } from '../../constants/route'
import './Auth.css'
import { validatePassword } from '../../utils/validation'

export default function ChangePassword() {
    const [oldPassword, setOldPassword] = useState('')
    const [newPassword, setNewPassword] = useState('')
    const [confirmPassword, setConfirmPassword] = useState('')
    const [error, setError] = useState('')
    const [success, setSuccess] = useState('')
    const [loading, setLoading] = useState(false)

    const { login } = useAuth()
    const navigate = useNavigate()


    async function handleSubmit(e) {
        e.preventDefault()
        setError('')
        setSuccess('')

        if (newPassword === oldPassword) {
            setError('New password cannot be the same as current password.')
            return
        }

        if (newPassword !== confirmPassword) {
            setError('New passwords do not match.')
            return
        }

        const validationError = validatePassword(newPassword)

        if (validationError) {
            setError(validationError)
            return
        }

        setLoading(true)
        try {
            await authService.changePassword(oldPassword, newPassword)

            // update session with new password so api.js keeps working
            const session = loadSession()
            if (session?.user?.email) {
                await login(session.user.email, newPassword)
            }

            setSuccess('Password changed successfully.')
            setOldPassword('')
            setNewPassword('')
            setConfirmPassword('')

            navigate(ROUTES.DASHBOARD)

        } catch (err) {
            const errors = err.response?.data?.errors
            const detail = err.response?.data?.detail
            if (errors?.length) {
                setError(errors[0].message)
            } else if (typeof detail === 'string') {
                setError(detail)
            } else {
                setError('Failed to change password.')
            }
        } finally {
            setLoading(false)
        }
    }

    return (
        <div>
            <div style={{ marginBottom: '20px' }}>
                <h2 style={{ fontSize: '20px', color: '#1e293b' }}>Change Password</h2>
            </div>

            <div className="form-card">
                <form onSubmit={handleSubmit}>
                    <div className="form-group">
                        <label>Current Password</label>
                        <input
                            type="password"
                            value={oldPassword}
                            onChange={(e) => setOldPassword(e.target.value)}
                            placeholder="Enter current password"
                            required
                        />
                    </div>

                    <div className="form-group">
                        <label>New Password</label>
                        <input
                            type="password"
                            value={newPassword}
                            onChange={(e) => setNewPassword(e.target.value)}
                            placeholder="6-12 chars, letter + number + special char"
                            required
                        />
                    </div>

                    <div className="form-group">
                        <label>Confirm New Password</label>
                        <input
                            type="password"
                            value={confirmPassword}
                            onChange={(e) => setConfirmPassword(e.target.value)}
                            placeholder="Repeat new password"
                            required
                        />
                    </div>

                    {error && <div className="error-msg">{error}</div>}
                    {success && <div className="success-msg">{success}</div>}

                    <button type="submit" className="btn-primary" disabled={loading}>
                        {loading ? 'Updating...' : 'Change Password'}
                    </button>
                </form>
            </div>
        </div>
    )
}