import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import candidateService from '../../services/candidateService'
import jobService from '../../services/jobService'
import { ROUTES } from '../../constants/route'
import { validateCandidateCreate } from '../../utils/candidateValidation'
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
    const [resumeFile, setResumeFile] = useState(null)
    const [jobs, setJobs] = useState([])
    const [error, setError] = useState('')
    const [loading, setLoading] = useState(false)
    const navigate = useNavigate()

    useEffect(() => {
        async function loadJobs() {
            try {
                const data = await jobService.getAllJobsForDropdown()
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

    async function handleSubmit(e) {
        e.preventDefault()
        setError('')

        const validationError = validateCandidateCreate(form, resumeFile)
        if (validationError) {
            setError(validationError)
            return
        }

        setLoading(true)
        try {
            const formData = new FormData()
            formData.append('first_name', form.first_name.trim())
            formData.append('last_name', form.last_name.trim())
            formData.append('email', form.email.trim())
            formData.append('mobile_number', form.mobile_number.trim())
            formData.append('current_company', form.current_company.trim())
            formData.append('total_experience', form.total_experience)
            formData.append('applied_job', form.applied_job)
            formData.append('resume', resumeFile)

            await candidateService.createCandidate(formData)
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
                            maxLength={50}
                            minLength={2}
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
                            minLength={2}
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

                    <div className="form-group">
                        <label>Resume</label>
                        <input
                            type="file"
                            accept="application/pdf"
                            onChange={(e) => setResumeFile(e.target.files[0])}
                            required
                        />
                        <p className="form-hint">PDF only · Max 10MB</p>
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