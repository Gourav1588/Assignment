import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import candidateService from '../../services/candidateService'
import jobService from '../../services/jobService'
import { ROUTES } from '../../constants/route'
import './Candidates.css'

export default function CreateCandidate() {
    const [form, setForm] = useState({
        first_name: '',
        last_name: '',
        email: '',
        mobile_number: '',
        current_company: '',
        total_experience: '',
        applied_job: '',
    })
    const [jobs, setJobs] = useState([])
    const [error, setError] = useState('')
    const [loading, setLoading] = useState(false)
    const navigate = useNavigate()

    useEffect(() => {
        async function loadJobs() {
            try {
                const data = await jobService.getAllJobs()
                setJobs(data)
            } catch {
                setError('Failed to load jobs.')
            }
        }
        loadJobs()
    }, [])

    function handleChange(e) {
        setForm({ ...form, [e.target.name]: e.target.value })
    }

    function validate() {
        if (!form.first_name.trim()) return 'First name is required.'
        if (!form.last_name.trim()) return 'Last name is required.'
        if (!form.email.trim()) return 'Email is required.'
        if (!form.mobile_number.trim()) return 'Mobile number is required.'
        if (!/^\d{10}$/.test(form.mobile_number)) {
            return 'Mobile number must be exactly 10 digits.'
        }
        if (!form.current_company.trim()) return 'Current company is required.'
        if (form.total_experience === '') return 'Total experience is required.'
        if (!form.applied_job) return 'Please select an applied job.'
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
            await candidateService.createCandidate({
                ...form,
                total_experience: parseFloat(form.total_experience),
            })
            navigate(ROUTES.CANDIDATES)
        } catch (err) {
            const errors = err.response?.data?.errors
            const detail = err.response?.data?.detail
            if (errors?.length) {
                setError(errors[0].message)
            } else if (typeof detail === 'string') {
                setError(detail)
            } else {
                setError('Failed to register candidate.')
            }
        } finally {
            setLoading(false)
        }
    }

    return (
        <div>
            <div className="page-header">
                <h2>Register Candidate</h2>
            </div>

            <div className="form-card">
                {error && <div className="error-msg">{error}</div>}

                <form onSubmit={handleSubmit}>
                    <div className="form-group">
                        <label>First Name</label>
                        <input
                            name="first_name"
                            value={form.first_name}
                            onChange={handleChange}
                            placeholder="Enter first name"
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
                            required
                        />
                    </div>

                    <div className="form-group">
                        <label>Email</label>
                        <input
                            name="email"
                            type="email"
                            value={form.email}
                            onChange={handleChange}
                            placeholder="candidate@example.com"
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

                    <div className="form-group">
                        <label>Applied Job</label>
                        <select
                            name="applied_job"
                            value={form.applied_job}
                            onChange={handleChange}
                            required
                        >
                            <option value="">Select a job</option>
                            {jobs.map((job) => (
                                <option key={job.id} value={job.id}>
                                    {job.title} — {job.location}
                                </option>
                            ))}
                        </select>
                    </div>

                    <div className="form-actions">
                        <button type="submit" className="btn btn-primary" disabled={loading}>
                            {loading ? 'Registering...' : 'Register Candidate'}
                        </button>
                        <button
                            type="button"
                            className="btn btn-secondary"
                            onClick={() => navigate(ROUTES.CANDIDATES)}
                        >
                            Cancel
                        </button>
                    </div>
                </form>
            </div>
        </div>
    )
}