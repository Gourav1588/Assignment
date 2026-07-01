import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import userService from '../../services/userService'
import { ROUTES } from '../../constants/route'
import './Users.css'

export default function UserList() {
    const [users, setUsers] = useState([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState('')
    const navigate = useNavigate()

    useEffect(() => {
        fetchUsers()
    }, [])

    async function fetchUsers() {
        try {
            const data = await userService.getAllUsers()
            setUsers(data)
        } catch {
            setError('Failed to load users.')
        } finally {
            setLoading(false)
        }
    }

    async function handleDisable(id) {
        if (!window.confirm('Are you sure you want to disable this user?')) return
        try {
            await userService.disableUser(id)
            // refresh list after disable
            fetchUsers()
        } catch {
            setError('Failed to disable user.')
        }
    }
    async function handleActivate(id) {
        if (!window.confirm('Are you sure you want to active this user?')) return
        try {
            await userService.activateUser(id)
            // refresh list after disable
            fetchUsers()
        } catch {
            setError('Failed to activate user.')
        }
    }

    if (loading) return <p className="loading-text">Loading users...</p>

    return (
        <div>
            <div className="page-header">
                <h2>User Management</h2>
                <button
                    className="btn btn-primary"
                    onClick={() => navigate(ROUTES.USER_CREATE)}
                >
                    + Create User
                </button>
            </div>

            {error && <div className="error-msg">{error}</div>}

            <div className="table-wrapper">
                <table>
                    <thead>
                        <tr>
                            <th>Full Name</th>
                            <th>Email</th>
                            <th>Role</th>
                            <th>Status</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {users.length === 0 ? (
                            <tr>
                                <td colSpan="5" style={{ textAlign: 'center', color: '#94a3b8' }}>
                                    No users found
                                </td>
                            </tr>
                        ) : (
                            users.map((user) => (
                                <tr key={user.id}>
                                    <td>{user.full_name}</td>
                                    <td>{user.email}</td>
                                    <td>{user.role}</td>
                                    <td>
                                        <span className={`badge ${user.is_active ? 'badge-active' : 'badge-inactive'}`}>
                                            {user.is_active ? 'Active' : 'Disabled'}
                                        </span>
                                    </td>
                                    <td style={{ display: 'flex', gap: '8px' }}>
                                        <button
                                            className="btn btn-warning"
                                            onClick={() => navigate(`/users/${user.id}/edit`)}
                                        >
                                            Edit
                                        </button>
                                        {user.is_active ? (
                                            <button
                                                className="btn btn-danger"
                                                onClick={() => handleDisable(user.id)}
                                            >
                                                Disable
                                            </button>
                                        ) : (
                                            <button className="btn btn-success" onClick={() => handleActivate((user.id))}>
                                                Activate
                                            </button>
                                        )}
                                    </td>
                                </tr>
                            ))
                        )}
                    </tbody>
                </table>
            </div>
        </div>
    )
}