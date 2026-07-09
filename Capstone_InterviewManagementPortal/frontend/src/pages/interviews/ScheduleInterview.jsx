import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import interviewService from '../../services/interviewService'
import userService from '../../services/userService'
import candidateService from '../../services/candidateService'
import { ROUTES } from '../../constants/route'
import './Interviews.css'

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

    useEffect(() => {
        async function loadData() {
            try {
                const [usersData, candidatesData] = await Promise.all([
                    userService.getAllUsers(1, 100),
                    candidateService.getAllCandidates(1, 100),
                ])
                setInterviewers(usersData.items.filter(u => u.role === 'Interviewer'))
                setCandidates(candidatesData.items)
            } catch {
                setError('Failed to load form data.')
            }
        }
        loadData()
    }, [])

    function handleChange(e) {
        setForm({ ...form, [e.target.name]: e.target.value })
    }

    function validate() {
        if (!form.candidate_id) return 'Please select a candidate.'
        if (!form.job_title.trim()) return 'Job title is required.'
        if (!form.interview_date) return 'Interview date is required.'
        if (!form.interview_time) return 'Interview time is required.'
        if (!form.interviewer_id) return 'Please select an interviewer.'
        if (!form.focus_areas.trim()) return 'Focus areas are required.'
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
                        <select name="candidate_id" value={form.candidate_id} onChange={handleChange}>
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
                        />
                    </div>

                    <div className="form-group">
                        <label>Interview Date</label>
                        <input
                            name="interview_date"
                            type="date"
                            value={form.interview_date}
                            onChange={handleChange}
                        />
                    </div>

                    <div className="form-group">
                        <label>Interview Time</label>
                        <input
                            name="interview_time"
                            type="time"
                            value={form.interview_time}
                            onChange={handleChange}
                        />
                    </div>

                    <div className="form-group">
                        <label>Interviewer</label>
                        <select name="interviewer_id" value={form.interviewer_id} onChange={handleChange}>
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