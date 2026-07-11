import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import userService from '../../services/userService'
import { ROUTES } from '../../constants/route'
import './Users.css'
import {
    validateEmail,
    validatePassword,
} from '../../utils/validation'

function generateTempPassword() {
    return Math.random().toString(36).slice(2, 8) + '@1A'
}

export default function CreateUser() {
    const [form, setForm] = useState({
        full_name: '',
        email: '',
        password: generateTempPassword(),
        role: 'HR',
    })
    const [error, setError] = useState('')
    const [loading, setLoading] = useState(false)
    const [showPassword, setShowPassword] = useState(false)
    const navigate = useNavigate()

    function handleChange(e) {
        setForm({ ...form, [e.target.name]: e.target.value })
    }



    async function handleSubmit(e) {
        e.preventDefault()
        setError('')

        const fullName = form.full_name.trim()

        if (!fullName) {
            setError('Full name is required.')
            return
        }

        if (fullName.length < 2 || fullName.length > 50) {
            setError('Full name must be between 2 and 50 characters.')
            return
        }

        if (!/^[A-Za-z ]+$/.test(fullName)) {
            setError('Full name can only contain letters and spaces.')
            return
        }

        const emailError = validateEmail(form.email)
        if (emailError) {
            setError(emailError)
            return
        }

        const passwordError = validatePassword(form.password)
        if (passwordError) {
            setError(passwordError)
            return
        }

        setLoading(true)

        try {
            await userService.createUser(form)
            navigate(ROUTES.USERS)
        } catch (err) {
            const errors = err.response?.data?.errors
            const detail = err.response?.data?.detail
            if (errors?.length) {
                setError(errors[0].message)
            } else if (typeof detail === 'string') {
                setError(detail)
            } else {
                setError('Failed to create user.')
            }
        } finally {
            setLoading(false)
        }
    }

    return (
        <div>
            <div className="page-header">
                <h2>Create User</h2>
            </div>

            <div className="form-card">
                {error && <div className="error-msg">{error}</div>}

                <form onSubmit={handleSubmit}>
                    <div className="form-group">
                        <label>Full Name</label>
                        <input
                            name="full_name"
                            value={form.full_name}
                            onChange={handleChange}
                            placeholder="Enter full name"
                            required
                        />
                    </div>

                    <div className="form-group">
                        <label>Email</label>
                        <input
                            name="email"
                            type="email"
                            value={form.email}
                            onChange={handleChange}
                            placeholder="name@nucleusteq.com"
                            required
                        />
                    </div>

                    <div className="form-group">
                        <label>Temporary Password</label>
                        <div style={{ display: 'flex', gap: '8px' }}>
                            <input
                                name="password"
                                type={showPassword ? 'text' : 'password'}
                                value={form.password}
                                onChange={handleChange}
                                style={{ flex: 1 }}
                            />
                            <button
                                type="button"
                                className="btn btn-secondary"
                                onClick={() => setShowPassword(!showPassword)}
                            >
                                {showPassword ? 'Hide' : 'Show'}
                            </button>
                        </div>
                        <p style={{ fontSize: '12px', color: '#94a3b8', marginTop: '4px' }}>
                            Share this with the user. They must change it on first login.
                        </p>
                    </div>

                    <div className="form-group">
                        <label>Role</label>
                        <select name="role" value={form.role} onChange={handleChange}>
                            <option value="HR">HR</option>
                            <option value="Interviewer">Interviewer</option>
                        </select>
                    </div>

                    <div className="form-actions">
                        <button type="submit" className="btn btn-primary" disabled={loading}>
                            {loading ? 'Creating...' : 'Create User'}
                        </button>
                        <button
                            type="button"
                            className="btn btn-secondary"
                            onClick={() => navigate(ROUTES.USERS)}
                        >
                            Cancel
                        </button>
                    </div>
                </form>
            </div>
        </div>
    )
}