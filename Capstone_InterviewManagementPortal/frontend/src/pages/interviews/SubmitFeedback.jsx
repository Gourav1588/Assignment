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

export default function SubmitFeedback() {
    const [interview, setInterview] = useState(null)
    const [feedback, setFeedback] = useState(null)
    const [form, setForm] = useState({
        technical_rating: '',
        communication_rating: '',
        problem_solving: '',
        tech_areas_covered: '',
        comments: '',
        recommendation: 'SELECT',
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

    function validate() {
        const r = (v) => parseInt(v)
        if (!form.technical_rating) return 'Technical rating is required.'
        if (!form.communication_rating) return 'Communication rating is required.'
        if (!form.problem_solving) return 'Problem solving rating is required.'
        if (r(form.technical_rating) < 1 || r(form.technical_rating) > 5)
            return 'Technical rating must be between 1 and 5.'
        if (r(form.communication_rating) < 1 || r(form.communication_rating) > 5)
            return 'Communication rating must be between 1 and 5.'
        if (r(form.problem_solving) < 1 || r(form.problem_solving) > 5)
            return 'Problem solving rating must be between 1 and 5.'
        if (!form.tech_areas_covered.trim()) return 'Tech areas covered is required.'
        if (!form.comments.trim()) return 'Comments are required.'
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

    return (
        <div>
            <div className="page-header">
                <h2>Submit Feedback</h2>
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
                                {feedback.recommendation.replace('_', ' ')}
                            </span>
                        </span>
                    </div>
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
                            />
                        </div>

                        <div className="form-group">
                            <label>Tech Areas Covered</label>
                            <input
                                name="tech_areas_covered"
                                value={form.tech_areas_covered}
                                onChange={handleChange}
                                placeholder="e.g. Python, APIs, SQL"
                            />
                        </div>

                        <div className="form-group">
                            <label>Comments</label>
                            <textarea
                                name="comments"
                                value={form.comments}
                                onChange={handleChange}
                                placeholder="Overall feedback about the candidate"
                            />
                        </div>

                        <div className="form-group">
                            <label>Recommendation</label>
                            <select
                                name="recommendation"
                                value={form.recommendation}
                                onChange={handleChange}
                            >
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