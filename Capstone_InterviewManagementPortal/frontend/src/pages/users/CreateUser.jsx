import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import userService from '../../services/userService'
import { ROUTES } from '../../constants/route'
import './Users.css'

export default function CreateUser() {
    const [form, setForm] = useState({
        full_name: '',
        email: '',
        password: '',
        role: 'HR',
    })
    const [error, setError] = useState('')
    const [loading, setLoading] = useState(false)
    const navigate = useNavigate()

    function handleChange(e) {
        setForm({ ...form, [e.target.name]: e.target.value })
    }

    function validate() {
        if (!form.full_name.trim()) return 'Full name is required.'
        if (!form.email.endsWith('@nucleusteq.com')) return 'Email must be a @nucleusteq.com address.'
        if (form.password.length < 6 || form.password.length > 12) return 'Password must be 6-12 characters.'
        return null
    }

    async function handleSubmit(e) {
        e.preventDefault()
        setError('')

        const validationError = validate()
        if (validationError) {
            setError(validationError)
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
                        <label>Password</label>
                        <input
                            name="password"
                            type="password"
                            value={form.password}
                            onChange={handleChange}
                            placeholder="6-12 chars, letter + number + special char"
                            required
                        />
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