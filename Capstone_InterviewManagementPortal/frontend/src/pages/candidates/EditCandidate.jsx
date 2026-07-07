import { useState, useEffect } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import candidateService from '../../services/candidateService'
import './Candidates.css'
import { ROUTES } from '../../constants/route'

const VALID_NEXT_STATUSES = {
    PROFILE_CREATED: ['INTERVIEW_SCHEDULED'],
    INTERVIEW_SCHEDULED: ['INTERVIEW_COMPLETED'],
    INTERVIEW_COMPLETED: ['SELECTED', 'REJECTED'],
    SELECTED: [],
    REJECTED: [],
}

export default function EditCandidate() {
    const [form, setForm] = useState({
        first_name: '',
        last_name: '',
        mobile_number: '',
        current_company: '',
        total_experience: '',
    })
    const [currentStatus, setCurrentStatus] = useState('')
    const [newStatus, setNewStatus] = useState('')
    const [success, setSuccess] = useState('')
    const [error, setError] = useState('')
    const [loading, setLoading] = useState(false)
    const [fetching, setFetching] = useState(true)
    const [statusLoading, setStatusLoading] = useState(false)

    const { id } = useParams()
    const navigate = useNavigate()

    useEffect(() => {
        async function loadCandidate() {
            try {
                const candidate = await candidateService.getCandidateById(id)
                setForm({
                    first_name: candidate.first_name,
                    last_name: candidate.last_name,
                    mobile_number: candidate.mobile_number,
                    current_company: candidate.current_company,
                    total_experience: candidate.total_experience,
                })
                setCurrentStatus(candidate.status)
                setNewStatus(candidate.status)
            } catch {
                setError('Failed to load candidate.')
            } finally {
                setFetching(false)
            }
        }
        loadCandidate()
    }, [id])

    function handleChange(e) {
        setForm({ ...form, [e.target.name]: e.target.value })
    }

    function validate() {
        if (!form.first_name.trim()) return 'First name is required.'
        if (!form.last_name.trim()) return 'Last name is required.'
        if (!form.mobile_number.trim()) return 'Mobile number is required.'
        if (!/^\d{10}$/.test(form.mobile_number)) return 'Mobile must be exactly 10 digits.'
        if (!form.current_company.trim()) return 'Current company is required.'
        if (form.total_experience === '') return 'Total experience is required.'
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
            await candidateService.updateCandidate(id, {
                ...form,
                total_experience: parseFloat(form.total_experience),
            })
            setSuccess('Profile updated successfully.')
        } catch (err) {
            const errors = err.response?.data?.errors
            const detail = err.response?.data?.detail
            if (errors?.length) {
                setError(errors[0].message)
            } else if (typeof detail === 'string') {
                setError(detail)
            } else {
                setError('Failed to update profile.')
            }
        } finally {
            setLoading(false)
        }
    }

    async function handleStatusSubmit(e) {
        e.preventDefault()
        setError('')
        setSuccess('')

        if (newStatus === currentStatus) {
            setError('Please select a different status.')
            return
        }

        setStatusLoading(true)
        try {
            await candidateService.updateStatus(id, newStatus)
            setCurrentStatus(newStatus)
            setSuccess('Status updated successfully.')
        } catch (err) {
            const detail = err.response?.data?.detail
            setError(typeof detail === 'string' ? detail : 'Failed to update status.')
        } finally {
            setStatusLoading(false)
        }
    }

    if (fetching) return <p className="loading-text">Loading candidate...</p>
    const nextOptions = VALID_NEXT_STATUSES[currentStatus] || []
    const isTerminal = nextOptions.length === 0
    return (
        <>
            <div className="page-header">
                <h2>Edit Candidate</h2>
                <button
                    className="btn btn-secondary btn-lg"
                    onClick={() => navigate(ROUTES.CANDIDATES)}
                >
                    Back
                </button>
            </div>

            {error && <div className="error-msg">{error}</div>}
            {success && <div className="success-msg">{success}</div>}

            <div className="detail-card">
                <h3 style={{ fontSize: '15px', color: '#1e293b', marginBottom: '16px' }}>
                    Profile Information
                </h3>
                <form onSubmit={handleSubmit}>
                    <div className="form-group">
                        <label>First Name</label>
                        <input
                            name="first_name"
                            value={form.first_name}
                            onChange={handleChange}
                            placeholder="Enter first name"

                        />
                    </div>

                    <div className="form-group">
                        <label>Last Name</label>
                        <input
                            name="last_name"
                            value={form.last_name}
                            onChange={handleChange}
                            placeholder="Enter last name"

                        />
                    </div>

                    <div className="form-group">
                        <label>Mobile Number</label>
                        <input
                            name="mobile_number"
                            value={form.mobile_number}
                            onChange={handleChange}
                            placeholder="10 digit mobile number"
                            maxLength={10}

                        />
                    </div>

                    <div className="form-group">
                        <label>Current Company</label>
                        <input
                            name="current_company"
                            value={form.current_company}
                            onChange={handleChange}
                            placeholder="Current employer"

                        />
                    </div>

                    <div className="form-group">
                        <label>Total Experience (years)</label>
                        <input
                            name="total_experience"
                            type="number"
                            min="0"
                            max="50"
                            step="0.5"
                            value={form.total_experience}
                            onChange={handleChange}
                            placeholder="e.g. 3"

                        />
                    </div>

                    <div className="form-actions">
                        <button type="submit" className="btn btn-primary" disabled={loading}>
                            {loading ? 'Saving...' : 'Save Changes'}
                        </button>
                    </div>
                </form>
            </div>


            <div className="detail-card">
                <h3 style={{ fontSize: '15px', color: '#1e293b', marginBottom: '16px' }}>
                    Update Status
                </h3>
                {isTerminal ? (
                    <p style={{ fontSize: '13px', color: '#94a3b8' }}>
                        Current status <strong>{currentStatus.replace(/_/g, ' ')}</strong> is final — no further changes allowed.
                    </p>
                ) : (
                    <form onSubmit={handleStatusSubmit}>
                        <div className="form-group">
                            <label>Current Status</label>
                            <p style={{ fontSize: '13px', color: '#374151', marginTop: '4px' }}>
                                <span className={`badge badge-${currentStatus.toLowerCase().replace(/_/g, '-').replace('profile-created', 'created').replace('interview-scheduled', 'scheduled').replace('interview-completed', 'completed')}`}>
                                    {currentStatus.replace(/_/g, ' ')}
                                </span>
                            </p>
                        </div>
                        <div className="form-group">
                            <label>Change To</label>
                            <select value={newStatus} onChange={(e) => setNewStatus(e.target.value)}>
                                <option value={currentStatus}>{currentStatus.replace(/_/g, ' ')} (current)</option>
                                {nextOptions.map((s) => (
                                    <option key={s} value={s}>{s.replace(/_/g, ' ')}</option>
                                ))}
                            </select>
                        </div>
                        <div className="form-actions">
                            <button type="submit" className="btn btn-primary btn-lg" disabled={statusLoading}>
                                {statusLoading ? 'Updating...' : 'Update Status'}
                            </button>
                        </div>
                    </form>
                )}
            </div>
        </>
    )
}