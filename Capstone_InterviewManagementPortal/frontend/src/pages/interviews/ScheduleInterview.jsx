import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import interviewService from '../../services/interviewService'
import userService from '../../services/userService'
import candidateService from '../../services/candidateService'
import { ROUTES } from '../../constants/route'
import { validateInterview } from '../../utils/interviewValidation'
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

export default function ScheduleInterview() {
    const [form, setForm] = useState({
        candidate_id: '',
        job_title: '',
        interview_date: '',
        interview_time: '',
        interviewer_id: '',
        focus_areas: '',
    })
    const [interviewers, setInterviewers] = useState([])
    const [candidates, setCandidates] = useState([])
    const [error, setError] = useState('')
    const [loading, setLoading] = useState(false)
    const navigate = useNavigate()

    const dateBounds = getDateBounds()

    useEffect(() => {
        async function loadData() {
            try {
                const [interviewersData, candidatesData] = await Promise.all([
                    userService.getAllInterviewersForDropdown(),
                    candidateService.getAllCandidatesForDropdown(),
                ])
                setInterviewers(interviewersData)
                setCandidates(candidatesData)
            } catch {
                setError('Failed to load form data.')
            }
        }
        loadData()
    }, [])

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
            await interviewService.scheduleInterview(form)
            navigate(ROUTES.INTERVIEWS)
        } catch (err) {
            const detail = err.response?.data?.detail
            setError(typeof detail === 'string' ? detail : 'Failed to schedule interview.')
        } finally {
            setLoading(false)
        }
    }

    return (
        <div>
            <div className="page-header">
                <h2>Schedule Interview</h2>
            </div>

            <div className="form-card">
                {error && <div className="error-msg">{error}</div>}

                <form onSubmit={handleSubmit}>
                    <div className="form-group">
                        <label>Candidate</label>
                        <select name="candidate_id" value={form.candidate_id} onChange={handleChange} required>
                            <option value="">Select a candidate</option>
                            {candidates.map((c) => (
                                <option key={c.id} value={c.id}>
                                    {c.first_name} {c.last_name} — {c.email}
                                </option>
                            ))}
                        </select>
                    </div>

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
                        <select name="interviewer_id" value={form.interviewer_id} onChange={handleChange} required>
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
                            {loading ? 'Scheduling...' : 'Schedule Interview'}
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