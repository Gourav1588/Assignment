import { useState, useEffect } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import candidateService from '../../services/candidateService'
import { ROUTES } from '../../constants/route'
import { validateCandidateUpdate } from '../../utils/candidateValidation'
import './Candidates.css'

const STATUS_BADGE = {
    PROFILE_CREATED: 'badge badge-created',
    INTERVIEW_SCHEDULED: 'badge badge-scheduled',
    INTERVIEW_COMPLETED: 'badge badge-completed',
    SELECTED: 'badge badge-selected',
    REJECTED: 'badge badge-rejected',
}

const DECISION_OPTIONS = ['SELECTED', 'REJECTED']

const STATUS_MESSAGE = {
    PROFILE_CREATED:
        'A decision can be made once this candidate has been interviewed.',
    INTERVIEW_SCHEDULED:
        'An interview is scheduled. A decision can be made once it has taken place and feedback has been submitted.',
    SELECTED:
        'This candidate has been selected. No further changes are allowed.',
    REJECTED:
        'This candidate has been rejected. No further changes are allowed.',
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
    const [lastRecommendation, setLastRecommendation] = useState(null)
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
                setLastRecommendation(candidate.last_recommendation)
                setNewStatus('')
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

    async function handleSubmit(e) {
        e.preventDefault()
        setError('')
        setSuccess('')

        const validationError = validateCandidateUpdate(form)
        if (validationError) {
            setError(validationError)
            return
        }

        setLoading(true)
        try {
            await candidateService.updateCandidate(id, {
                first_name: form.first_name.trim(),
                last_name: form.last_name.trim(),
                mobile_number: form.mobile_number.trim(),
                current_company: form.current_company.trim(),
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

        if (!newStatus) {
            setError('Please select a decision.')
            return
        }

        setStatusLoading(true)
        try {
            await candidateService.updateStatus(id, newStatus)
            setCurrentStatus(newStatus)
            setNewStatus('')
            setSuccess('Decision recorded successfully.')
        } catch (err) {
            const detail = err.response?.data?.detail
            setError(typeof detail === 'string' ? detail : 'Failed to record decision.')
        } finally {
            setStatusLoading(false)
        }
    }

    if (fetching) return <p className="loading-text">Loading candidate...</p>

    const isCompleted = currentStatus === 'INTERVIEW_COMPLETED'
    const needsAnotherRound = isCompleted && lastRecommendation === 'NEXT_ROUND'
    const canDecide = isCompleted && !needsAnotherRound

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
                            minLength={2}
                            maxLength={50}
                            required
                        />
                    </div>

                    <div className="form-group">
                        <label>Last Name</label>
                        <input
                            name="last_name"
                            value={form.last_name}
                            onChange={handleChange}
                            placeholder="Enter last name"
                            minLength={2}
                            maxLength={50}
                            required
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
                            required
                        />
                    </div>

                    <div className="form-group">
                        <label>Current Company</label>
                        <input
                            name="current_company"
                            value={form.current_company}
                            onChange={handleChange}
                            placeholder="Current employer"
                            maxLength={100}
                            required
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
                            required
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
                    Hiring Decision
                </h3>

                <div className="form-group">
                    <label>Current Status</label>
                    <p style={{ fontSize: '13px', color: '#374151', marginTop: '4px' }}>
                        <span className={STATUS_BADGE[currentStatus]}>
                            {currentStatus.replace(/_/g, ' ')}
                        </span>
                    </p>
                </div>

                {canDecide ? (
                    <form onSubmit={handleStatusSubmit}>
                        <div className="form-group">
                            <label>Decision</label>
                            <select
                                value={newStatus}
                                onChange={(e) => setNewStatus(e.target.value)}
                                required
                            >
                                <option value="">Select a decision</option>
                                {DECISION_OPTIONS.map((s) => (
                                    <option key={s} value={s}>{s}</option>
                                ))}
                            </select>
                            <p style={{ fontSize: '12px', color: '#94a3b8', marginTop: '4px' }}>
                                Requires the interviewer to have submitted feedback.
                            </p>
                        </div>
                        <div className="form-actions">
                            <button type="submit" className="btn btn-primary btn-lg" disabled={statusLoading}>
                                {statusLoading ? 'Recording...' : 'Record Decision'}
                            </button>
                        </div>
                    </form>
                ) : needsAnotherRound ? (
                    <p style={{ fontSize: '13px', color: '#374151' }}>
                        The interviewer recommended another round. Schedule the next
                        interview from the Interviews page to continue with this candidate.
                    </p>
                ) : (
                    <p style={{ fontSize: '13px', color: '#94a3b8' }}>
                        {STATUS_MESSAGE[currentStatus]}
                    </p>
                )}
            </div>
        </>
    )
}