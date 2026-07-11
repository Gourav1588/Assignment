import { useState, useEffect } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import interviewService from '../../services/interviewService'
import { ROUTES } from '../../constants/route'
import { validateFeedback } from '../../utils/feedbackValidation'
import { hasInterviewPassed } from '../../utils/interviewTime'
import './Interviews.css'

const RECOMMENDATION_BADGE = {
    SELECT: 'badge badge-select',
    REJECT: 'badge badge-reject',
    NEXT_ROUND: 'badge badge-next-round',
}

export default function SubmitFeedback() {
    const [interview, setInterview] = useState(null)
    const [feedback, setFeedback] = useState(null)
    const [form, setForm] = useState({
        technical_rating: '',
        communication_rating: '',
        problem_solving: '',
        tech_areas_covered: '',
        comments: '',
        recommendation: '',
    })
    const [error, setError] = useState('')
    const [loading, setLoading] = useState(false)
    const [fetching, setFetching] = useState(true)
    const { id } = useParams()
    const navigate = useNavigate()

    useEffect(() => {
        async function load() {
            try {
                const interviewData = await interviewService.getInterviewById(id)
                setInterview(interviewData)

                const feedbackData = await interviewService.getFeedback(id)
                setFeedback(feedbackData)
            } catch (err) {
                const detail = err.response?.data?.detail
                setError(typeof detail === 'string' ? detail : 'Failed to load interview details')
            } finally {
                setFetching(false)
            }
        }
        load()
    }, [id])

    function handleChange(e) {
        setForm({ ...form, [e.target.name]: e.target.value })
    }

    async function handleSubmit(e) {
        e.preventDefault()
        setError('')

        const validationError = validateFeedback(form)
        if (validationError) {
            setError(validationError)
            return
        }

        setLoading(true)
        try {
            await interviewService.submitFeedback(id, {
                ...form,
                technical_rating: parseInt(form.technical_rating),
                communication_rating: parseInt(form.communication_rating),
                problem_solving: parseInt(form.problem_solving),
            })
            navigate(ROUTES.MY_INTERVIEWS)
        } catch (err) {
            const detail = err.response?.data?.detail
            setError(typeof detail === 'string' ? detail : 'Failed to submit feedback.')
        } finally {
            setLoading(false)
        }
    }

    if (fetching) return <p className="loading-text">Loading interview...</p>
    if (error && !interview) return <div className="error-msg">{error}</div>

    const passed = interview
        ? hasInterviewPassed(interview.interview_date, interview.interview_time)
        : false

    return (
        <div>
            <div className="page-header">
                <h2>{feedback ? 'Interview Feedback' : 'Submit Feedback'}</h2>
                <button
                    className="btn btn-secondary"
                    onClick={() => navigate(ROUTES.MY_INTERVIEWS)}
                >
                    Back
                </button>
            </div>

            {interview && (
                <div className="detail-card">
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
                        <span className="detail-label">Focus Areas</span>
                        <span className="detail-value">{interview.focus_areas}</span>
                    </div>
                </div>
            )}

            {feedback ? (
                <div className="detail-card">
                    <p style={{ fontSize: '13px', color: '#64748b', marginBottom: '16px' }}>
                        Feedback already submitted for this interview.
                    </p>
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
                        <span className="detail-label">Tech Areas</span>
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
                                {feedback.recommendation.replace(/_/g, ' ')}
                            </span>
                        </span>
                    </div>
                </div>
            ) : !passed ? (
                <div className="detail-card">
                    <p style={{ fontSize: '14px', color: '#64748b' }}>
                        <span className="badge badge-scheduled">Upcoming</span>
                        &nbsp; Feedback can be submitted once this interview has taken place.
                    </p>
                </div>
            ) : (
                <div className="form-card">
                    {error && <div className="error-msg">{error}</div>}

                    <form onSubmit={handleSubmit}>
                        <div className="form-group">
                            <label>Technical Rating (1-5)</label>
                            <input
                                name="technical_rating"
                                type="number"
                                min="1"
                                max="5"
                                value={form.technical_rating}
                                onChange={handleChange}
                                placeholder="1 to 5"
                                required
                            />
                        </div>

                        <div className="form-group">
                            <label>Communication Rating (1-5)</label>
                            <input
                                name="communication_rating"
                                type="number"
                                min="1"
                                max="5"
                                value={form.communication_rating}
                                onChange={handleChange}
                                placeholder="1 to 5"
                                required
                            />
                        </div>

                        <div className="form-group">
                            <label>Problem Solving (1-5)</label>
                            <input
                                name="problem_solving"
                                type="number"
                                min="1"
                                max="5"
                                value={form.problem_solving}
                                onChange={handleChange}
                                placeholder="1 to 5"
                                required
                            />
                        </div>

                        <div className="form-group">
                            <label>Tech Areas Covered</label>
                            <input
                                name="tech_areas_covered"
                                value={form.tech_areas_covered}
                                minLength={2}
                                maxLength={500}
                                onChange={handleChange}
                                placeholder="e.g. Python, APIs, SQL"
                                required
                            />
                        </div>

                        <div className="form-group">
                            <label>Comments</label>
                            <textarea
                                name="comments"
                                value={form.comments}
                                minLength={5}
                                maxLength={1000}
                                onChange={handleChange}
                                placeholder="Overall feedback about the candidate"
                                required
                            />
                        </div>

                        <div className="form-group">
                            <label>Recommendation</label>
                            <select
                                name="recommendation"
                                value={form.recommendation}
                                onChange={handleChange}
                                required
                            >
                                <option value="">Select a recommendation</option>
                                <option value="SELECT">Select</option>
                                <option value="REJECT">Reject</option>
                                <option value="NEXT_ROUND">Next Round</option>
                            </select>
                        </div>

                        <div className="form-actions">
                            <button type="submit" className="btn btn-primary" disabled={loading}>
                                {loading ? 'Submitting...' : 'Submit Feedback'}
                            </button>
                        </div>
                    </form>
                </div>
            )}
        </div>
    )
}