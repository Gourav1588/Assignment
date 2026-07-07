import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import candidateService from '../../services/candidateService'
import { ROUTES } from '../../constants/route'
import './Candidates.css'

const STATUS_OPTIONS = [
    'PROFILE_CREATED',
    'INTERVIEW_SCHEDULED',
    'INTERVIEW_COMPLETED',
    'SELECTED',
    'REJECTED',
]

const STATUS_BADGE = {
    PROFILE_CREATED: 'badge badge-created',
    INTERVIEW_SCHEDULED: 'badge badge-scheduled',
    INTERVIEW_COMPLETED: 'badge badge-completed',
    SELECTED: 'badge badge-selected',
    REJECTED: 'badge badge-rejected',
}

export default function CandidateList() {
    const [candidates, setCandidates] = useState([])
    const [statusFilter, setStatusFilter] = useState('')
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState('')
    const [resumeLoadingId, setResumeLoadingId] = useState(null)
    const navigate = useNavigate()

    useEffect(() => {
        fetchCandidates()
    }, [statusFilter])

    async function fetchCandidates() {
        setLoading(true)
        try {
            const data = await candidateService.getAllCandidates(statusFilter || null)
            setCandidates(data)
        } catch {
            setError('Failed to load candidates.')
        } finally {
            setLoading(false)
        }
    }

    async function handleViewResume(id) {
        setResumeLoadingId(id)
        try {
            await candidateService.viewResume(id)
        } catch {
            setError('Failed to open resume.')
        } finally {
            setResumeLoadingId(null)
        }
    }

    if (loading) return <p className="loading-text">Loading candidates...</p>

    return (
        <div>
            <div className="page-header">
                <h2>Candidates</h2>
                <button
                    className="btn btn-primary"
                    onClick={() => navigate(ROUTES.CANDIDATE_CREATE)}
                >
                    + Register Candidate
                </button>
            </div>

            <div className="filter-bar">
                <label style={{ fontSize: '13px', fontWeight: 600, color: '#374151' }}>
                    Filter by Status:
                </label>
                <select
                    value={statusFilter}
                    onChange={(e) => setStatusFilter(e.target.value)}
                >
                    <option value="">All</option>
                    {STATUS_OPTIONS.map((s) => (
                        <option key={s} value={s}>{s.replace(/_/g, ' ')}</option>
                    ))}
                </select>
            </div>

            {error && <div className="error-msg">{error}</div>}

            <div className="table-wrapper">
                <table>
                    <thead>
                        <tr>
                            <th>Name</th>
                            <th>Email</th>
                            <th>Mobile</th>
                            <th>Company</th>
                            <th>Experience</th>
                            <th>Status</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {candidates.length === 0 ? (
                            <tr>
                                <td colSpan="7" style={{ textAlign: 'center', color: '#94a3b8' }}>
                                    No candidates found
                                </td>
                            </tr>
                        ) : (
                            candidates.map((c) => (
                                <tr key={c.id}>
                                    <td>{c.first_name} {c.last_name}</td>
                                    <td>{c.email}</td>
                                    <td>{c.mobile_number}</td>
                                    <td>{c.current_company}</td>
                                    <td>{c.total_experience} yrs</td>
                                    <td>
                                        <span className={STATUS_BADGE[c.status]}>
                                            {c.status.replace(/_/g, ' ')}
                                        </span>
                                    </td>
                                    <td>
                                        <div className="actions-cell">
                                            <button
                                                className="btn btn-secondary"
                                                style={{ padding: '6px 12px', fontSize: '12px' }}
                                                onClick={() => navigate(`/candidates/${c.id}`)}
                                            >
                                                View
                                            </button>
                                            <button
                                                className="btn btn-warning"
                                                onClick={() => navigate(`/candidates/${c.id}/edit`)}
                                            >
                                                Edit
                                            </button>
                                            <button
                                                className="btn btn-purple"
                                                onClick={() => navigate(`/candidates/${c.id}/history`)}
                                            >
                                                History
                                            </button>
                                            <button
                                                className="btn btn-green"
                                                disabled={resumeLoadingId === c.id}
                                                onClick={() => handleViewResume(c.id)}
                                            >
                                                {resumeLoadingId === c.id ? '...' : 'Resume'}
                                            </button>
                                        </div>
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