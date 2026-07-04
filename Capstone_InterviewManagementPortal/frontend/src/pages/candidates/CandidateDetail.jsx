import { useState, useEffect } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import candidateService from '../../services/candidateService'
import { ROUTES } from '../../constants/route'
import './Candidates.css'

const STATUS_BADGE = {
    PROFILE_CREATED: 'badge badge-created',
    INTERVIEW_SCHEDULED: 'badge badge-scheduled',
    INTERVIEW_COMPLETED: 'badge badge-completed',
    SELECTED: 'badge badge-selected',
    REJECTED: 'badge badge-rejected',
}

export default function CandidateDetail() {
    const [candidate, setCandidate] = useState(null)
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState('')

    const { id } = useParams()
    const navigate = useNavigate()

    useEffect(() => {
        async function loadCandidate() {
            try {
                const data = await candidateService.getCandidateById(id)
                setCandidate(data)
            } catch {
                setError('Failed to load candidate details.')
            } finally {
                setLoading(false)
            }
        }
        loadCandidate()
    }, [id])

    if (loading) return <p className="loading-text">Loading candidate...</p>
    if (error) return <div className="error-msg">{error}</div>

    return (
        <div>
            <div className="page-header">
                <h2>Candidate Details</h2>
                <div style={{ display: 'flex', gap: '10px' }}>
                    <button
                        className="btn btn-warning"
                        onClick={() => navigate(`/candidates/${id}/edit`)}
                    >
                        Edit
                    </button>

                    <button
                        className="btn btn-secondary"
                        onClick={() => navigate(ROUTES.CANDIDATES)}
                    >
                        Back
                    </button>
                </div>
            </div>

            <div className="detail-card">
                <div className="detail-row">
                    <span className="detail-label">Full Name</span>
                    <span className="detail-value">
                        {candidate.first_name} {candidate.last_name}
                    </span>
                </div>
                <div className="detail-row">
                    <span className="detail-label">Email</span>
                    <span className="detail-value">{candidate.email}</span>
                </div>
                <div className="detail-row">
                    <span className="detail-label">Mobile</span>
                    <span className="detail-value">{candidate.mobile_number}</span>
                </div>
                <div className="detail-row">
                    <span className="detail-label">Current Company</span>
                    <span className="detail-value">{candidate.current_company}</span>
                </div>
                <div className="detail-row">
                    <span className="detail-label">Experience</span>
                    <span className="detail-value">{candidate.total_experience} years</span>
                </div>
                <div className="detail-row">
                    <span className="detail-label">Status</span>
                    <span className="detail-value">
                        <span className={STATUS_BADGE[candidate.status]}>
                            {candidate.status.replace(/_/g, ' ')}
                        </span>
                    </span>
                </div>
                <div className="detail-row">
                    <span className="detail-label">Created By</span>
                    <span className="detail-value">{candidate.created_by}</span>
                </div>
            </div>
        </div>
    )
}