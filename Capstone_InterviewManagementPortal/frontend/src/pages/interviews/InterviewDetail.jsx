import { useState, useEffect } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import interviewService from '../../services/interviewService'
import { ROUTES } from '../../constants/route'
import './Interviews.css'

const RECOMMENDATION_BADGE = {
    SELECT: 'badge badge-select',
    REJECT: 'badge badge-reject',
    NEXT_ROUND: 'badge badge-next-round',
}

export default function InterviewDetail() {
    const [interview, setInterview] = useState(null)
    const [feedback, setFeedback] = useState(null)
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState('')
    const { id } = useParams()
    const navigate = useNavigate()


    useEffect(() => {
        async function load() {
            try {
                const interviewData = await interviewService.getInterviewById(id)
                setInterview(interviewData)

                const feedbackData = await interviewService.getFeedback(id)
                setFeedback(feedbackData)
            } catch {
                setError('Failed to load interview details.')
            } finally {
                setLoading(false)
            }
        }
        load()
    }, [id])

    if (loading) return <p className="loading-text">Loading interview...</p>
    if (error) return <div className="error-msg">{error}</div>

    return (
        <div>
            <div className="page-header">
                <h2>Interview Details</h2>
                <button
                    className="btn btn-secondary"
                    onClick={() => navigate(ROUTES.INTERVIEWS)}
                >
                    Back
                </button>
            </div>

            <div className="detail-card">
                <div className="detail-row">
                    <span className="detail-label">Candidate ID</span>
                    <span className="detail-value">{interview.candidate_id}</span>
                </div>
                <div className="detail-row">
                    <span className="detail-label">Job Title</span>
                    <span className="detail-value">{interview.job_title}</span>
                </div>
                <div className="detail-row">
                    <span className="detail-label">Date</span>
                    <span className="detail-value">{interview.interview_date}</span>
                </div>
                <div className="detail-row">
                    <span className="detail-label">Time</span>
                    <span className="detail-value">{interview.interview_time}</span>
                </div>
                <div className="detail-row">
                    <span className="detail-label">Interviewer ID</span>
                    <span className="detail-value">{interview.interviewer_id}</span>
                </div>
                <div className="detail-row">
                    <span className="detail-label">Focus Areas</span>
                    <span className="detail-value">{interview.focus_areas}</span>
                </div>
                <div className="detail-row">
                    <span className="detail-label">Scheduled By</span>
                    <span className="detail-value">{interview.scheduled_by}</span>
                </div>
            </div>

            <h3 style={{ fontSize: '16px', color: '#1e293b', marginBottom: '12px' }}>
                Feedback
            </h3>

            {!feedback ? (
                <p style={{ color: '#94a3b8', fontSize: '14px' }}>
                    No feedback submitted yet.
                </p>
            ) : (
                <div className="detail-card">
                    <div className="detail-row">
                        <span className="detail-label">Technical Rating</span>
                        <span className="detail-value">{feedback.technical_rating} / 5</span>
                    </div>
                    <div className="detail-row">
                        <span className="detail-label">Communication</span>
                        <span className="detail-value">{feedback.communication_rating} / 5</span>
                    </div>
                    <div className="detail-row">
                        <span className="detail-label">Problem Solving</span>
                        <span className="detail-value">{feedback.problem_solving} / 5</span>
                    </div>
                    <div className="detail-row">
                        <span className="detail-label">Tech Areas Covered</span>
                        <span className="detail-value">{feedback.tech_areas_covered}</span>
                    </div>
                    <div className="detail-row">
                        <span className="detail-label">Comments</span>
                        <span className="detail-value">{feedback.comments}</span>
                    </div>
                    <div className="detail-row">
                        <span className="detail-label">Recommendation</span>
                        <span className="detail-value">
                            <span className={RECOMMENDATION_BADGE[feedback.recommendation]}>
                                {feedback.recommendation.replace('_', ' ')}
                            </span>
                        </span>
                    </div>
                </div>
            )}
        </div>
    )
}