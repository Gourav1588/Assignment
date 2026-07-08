import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import userService from '../../services/userService'
import { ROUTES } from '../../constants/route'
import './Users.css'

export default function UserList() {
    const [users, setUsers] = useState([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState('')
    const [page, setPage] = useState(1)
    const [totalPages, setTotalPages] = useState(1)

    const PAGE_SIZE = 10

    const navigate = useNavigate()

    useEffect(() => {
        fetchUsers()
    }, [page])

    async function fetchUsers() {
        setLoading(true)
        try {
            const data = await userService.getAllUsers(page, PAGE_SIZE)
            setUsers(data.items)
            setTotalPages(data.total_pages)
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
                                        {user.role !== 'Admin' && (
                                            user.is_active ? (
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
                                            )
                                        )}
                                    </td>
                                </tr>
                            ))
                        )}
                    </tbody>
                </table>
            </div>
            {totalPages > 1 && (
                <div className="pagination">
                    <button
                        className="btn btn-secondary"
                        onClick={() => setPage((p) => p - 1)}
                        disabled={page === 1}
                    >
                        ← Prev
                    </button>

                    <span style={{ fontSize: '13px', color: '#374151', padding: '0 12px' }}>
                        Page {page} of {totalPages}
                    </span>

                    <button
                        className="btn btn-secondary"
                        onClick={() => setPage((p) => p + 1)}
                        disabled={page === totalPages}
                    >
                        Next →
                    </button>

                </div>
            )}

        </div>
    )
}