import { useState, useEffect } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import interviewService from '../../services/interviewService'
import userService from '../../services/userService'
import { ROUTES } from '../../constants/route'
import { validateInterview } from '../../utils/interviewValidation'
import { hasInterviewPassed } from '../../utils/interviewTime'
import './Interviews.css'

function getDateBounds() {
    const today = new Date()
    const maxDate = new Date()
    maxDate.setDate(today.getDate() + 30)
    return {
        min: today.toISOString().split('T')[0],
        max: maxDate.toISOString().split('T')[0],
    }
}

export default function EditInterview() {
    const [form, setForm] = useState({
        candidate_id: '',
        job_title: '',
        interview_date: '',
        interview_time: '',
        interviewer_id: '',
        focus_areas: '',
    })
    const [interviewers, setInterviewers] = useState([])
    const [isPassed, setIsPassed] = useState(false)
    const [error, setError] = useState('')
    const [loading, setLoading] = useState(false)
    const [fetching, setFetching] = useState(true)

    const { id } = useParams()
    const navigate = useNavigate()

    const dateBounds = getDateBounds()

    useEffect(() => {
        async function load() {
            try {
                const [interview, interviewersData] = await Promise.all([
                    interviewService.getInterviewById(id),
                    userService.getAllInterviewersForDropdown(),
                ])

                setForm({
                    candidate_id: interview.candidate_id,
                    job_title: interview.job_title,
                    interview_date: interview.interview_date,
                    interview_time: interview.interview_time,
                    interviewer_id: interview.interviewer_id,
                    focus_areas: interview.focus_areas,
                })
                setInterviewers(interviewersData)
                setIsPassed(hasInterviewPassed(interview.interview_date, interview.interview_time))
            } catch (err) {
                const detail = err.response?.data?.detail
                setError(typeof detail === 'string' ? detail : 'Failed to load interview.')
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

        const validationError = validateInterview(form)
        if (validationError) {
            setError(validationError)
            return
        }

        setLoading(true)
        try {
            await interviewService.updateInterview(id, {
                job_title: form.job_title,
                interview_date: form.interview_date,
                interview_time: form.interview_time,
                interviewer_id: form.interviewer_id,
                focus_areas: form.focus_areas,
            })
            navigate(ROUTES.INTERVIEWS)
        } catch (err) {
            const detail = err.response?.data?.detail
            setError(typeof detail === 'string' ? detail : 'Failed to update interview.')
        } finally {
            setLoading(false)
        }
    }

    if (fetching) return <p className="loading-text">Loading interview...</p>

    if (isPassed) {
        return (
            <div>
                <div className="page-header">
                    <h2>Edit Interview</h2>
                    <button
                        className="btn btn-secondary"
                        onClick={() => navigate(ROUTES.INTERVIEWS)}
                    >
                        Back
                    </button>
                </div>
                <div className="detail-card">
                    <p style={{ fontSize: '14px', color: '#64748b' }}>
                        This interview has already taken place and can no longer be modified.
                    </p>
                </div>
            </div>
        )
    }

    return (
        <div>
            <div className="page-header">
                <h2>Edit Interview</h2>
                <button
                    className="btn btn-secondary"
                    onClick={() => navigate(ROUTES.INTERVIEWS)}
                >
                    Back
                </button>
            </div>

            <div className="form-card">
                {error && <div className="error-msg">{error}</div>}

                <form onSubmit={handleSubmit}>
                    <div className="form-group">
                        <label>Job Title</label>
                        <input
                            name="job_title"
                            value={form.job_title}
                            onChange={handleChange}
                            placeholder="e.g. Backend Developer"
                            minLength={2}
                            maxLength={100}
                            required
                        />
                    </div>

                    <div className="form-group">
                        <label>Interview Date</label>
                        <input
                            name="interview_date"
                            type="date"
                            value={form.interview_date}
                            onChange={handleChange}
                            min={dateBounds.min}
                            max={dateBounds.max}
                            required
                        />
                    </div>

                    <div className="form-group">
                        <label>Interview Time</label>
                        <input
                            name="interview_time"
                            type="time"
                            value={form.interview_time}
                            onChange={handleChange}
                            min="09:00"
                            max="18:00"
                            required
                        />
                        <p style={{ fontSize: '12px', color: '#94a3b8', marginTop: '4px' }}>
                            Between 09:00 AM and 06:00 PM
                        </p>
                    </div>

                    <div className="form-group">
                        <label>Interviewer</label>
                        <select
                            name="interviewer_id"
                            value={form.interviewer_id}
                            onChange={handleChange}
                            required
                        >
                            <option value="">Select an interviewer</option>
                            {interviewers.map((u) => (
                                <option key={u.id} value={u.id}>
                                    {u.full_name} — {u.email}
                                </option>
                            ))}
                        </select>
                    </div>

                    <div className="form-group">
                        <label>Focus Areas</label>
                        <textarea
                            name="focus_areas"
                            value={form.focus_areas}
                            onChange={handleChange}
                            placeholder="e.g. Python, System Design, DSA"
                            minLength={2}
                            maxLength={500}
                            required
                        />
                    </div>

                    <div className="form-actions">
                        <button type="submit" className="btn btn-primary" disabled={loading}>
                            {loading ? 'Saving...' : 'Save Changes'}
                        </button>
                        <button
                            type="button"
                            className="btn btn-secondary"
                            onClick={() => navigate(ROUTES.INTERVIEWS)}
                        >
                            Cancel
                        </button>
                    </div>
                </form>
            </div>
        </div>
    )
}