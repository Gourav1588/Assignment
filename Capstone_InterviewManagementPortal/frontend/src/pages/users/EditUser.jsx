import { useState, useEffect } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import userService from '../../services/userService'
import { ROUTES } from '../../constants/route'
import './Users.css'

export default function EditUser() {
    const [form, setForm] = useState({ full_name: '', role: '' })
    const [error, setError] = useState('')
    const [loading, setLoading] = useState(false)
    const [fetching, setFetching] = useState(true)

    const { id } = useParams()
    const navigate = useNavigate()

    useEffect(() => {
        async function loadUser() {
            try {
                const user = await userService.getUserById(id)
                setForm({ full_name: user.full_name, role: user.role })
            } catch {
                setError('Failed to load user.')
            } finally {
                setFetching(false)
            }
        }
        loadUser()
    }, [id])

    function handleChange(e) {
        setForm({ ...form, [e.target.name]: e.target.value })
    }

    async function handleSubmit(e) {
        e.preventDefault()
        setError('')

        if (!form.full_name.trim()) {
            setError('Full name is required.')
            return
        }

        setLoading(true)
        try {
            await userService.updateUser(id, form)
            navigate(ROUTES.USERS)
        } catch (err) {
            const errors = err.response?.data?.errors
            const detail = err.response?.data?.detail
            if (errors?.length) {
                setError(errors[0].message)
            } else if (typeof detail === 'string') {
                setError(detail)
            } else {
                setError('Failed to update user.')
            }
        } finally {
            setLoading(false)
        }
    }

    if (fetching) return <p className="loading-text">Loading user...</p>

    return (
        <div>
            <div className="page-header">
                <h2>Edit User</h2>
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
                        <label>Role</label>
                        <select name="role" value={form.role} onChange={handleChange}>
                            <option value="HR">HR</option>
                            <option value="Interviewer">Interviewer</option>
                        </select>
                    </div>

                    <div className="form-actions">
                        <button type="submit" className="btn btn-primary" disabled={loading}>
                            {loading ? 'Saving...' : 'Save Changes'}
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