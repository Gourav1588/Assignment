import { useState, useEffect } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import jobService from '../../services/jobService'
import { ROUTES } from '../../constants/route'
import './Jobs.css'

export default function JobDetail() {
    const [job, setJob] = useState(null)
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState('')

    const { id } = useParams()
    const navigate = useNavigate()

    useEffect(() => {
        async function loadJob() {
            try {
                const data = await jobService.getJobById(id)
                setJob(data)
            } catch {
                setError('Failed to load job details.')
            } finally {
                setLoading(false)
            }
        }
        loadJob()
    }, [id])

    if (loading) return <p className="loading-text">Loading job details...</p>
    if (error) return <div className="error-msg">{error}</div>

    return (
        <div>
            <div className="page-header">
                <h2>Job Details</h2>
                <div style={{ display: 'flex', gap: '10px' }}>
                    <button
                        className="btn btn-warning"
                        onClick={() => navigate(`/jobs/${id}/edit`)}
                    >
                        Edit
                    </button>
                    <button
                        className="btn btn-secondary"
                        onClick={() => navigate(ROUTES.JOBS)}
                    >
                        Back
                    </button>
                </div>
            </div>

            <div className="detail-card">
                <div className="detail-row">
                    <span className="detail-label">Job Title</span>
                    <span className="detail-value">{job.title}</span>
                </div>
                <div className="detail-row">
                    <span className="detail-label">Job Role</span>
                    <span className="detail-value">{job.role}</span>
                </div>
                <div className="detail-row">
                    <span className="detail-label">Job Details</span>
                    <span className="detail-value">{job.details}</span>
                </div>
                <div className="detail-row">
                    <span className="detail-label">Required Skills</span>
                    <span className="detail-value">{job.required_skills}</span>
                </div>
                <div className="detail-row">
                    <span className="detail-label">Experience Required</span>
                    <span className="detail-value">{job.experience_required} years</span>
                </div>
                <div className="detail-row">
                    <span className="detail-label">Employment Type</span>
                    <span className="detail-value">
                        <span className="badge">{job.employment_type}</span>
                    </span>
                </div>
                <div className="detail-row">
                    <span className="detail-label">Location</span>
                    <span className="detail-value">{job.location}</span>
                </div>
                <div className="detail-row">
                    <span className="detail-label">Posted By</span>
                    <span className="detail-value">{job.created_by}</span>
                </div>
            </div>
        </div>
    )
}