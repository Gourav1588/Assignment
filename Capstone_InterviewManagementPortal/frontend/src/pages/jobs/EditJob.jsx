import { useState, useEffect } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import jobService from '../../services/jobService'
import { ROUTES } from '../../constants/route'
import './Jobs.css'
import { validateJob } from '../../utils/jobValidation'

export default function EditJob() {
    const [form, setForm] = useState({
        title: '',
        details: '',
        role: '',
        required_skills: '',
        experience_required: '',
        employment_type: 'Full Time',
        location: '',
    })
    const [error, setError] = useState('')
    const [loading, setLoading] = useState(false)
    const [fetching, setFetching] = useState(true)

    const { id } = useParams()
    const navigate = useNavigate()

    useEffect(() => {
        async function loadJob() {
            try {
                const job = await jobService.getJobById(id)
                setForm({
                    title: job.title,
                    details: job.details,
                    role: job.role,
                    required_skills: job.required_skills,
                    experience_required: job.experience_required,
                    employment_type: job.employment_type,
                    location: job.location,
                })
            } catch {
                setError('Failed to load job.')
            } finally {
                setFetching(false)
            }
        }
        loadJob()
    }, [id])

    function handleChange(e) {
        setForm({ ...form, [e.target.name]: e.target.value })
    }

    async function handleSubmit(e) {
        e.preventDefault()
        setError('')


        const validationError = validateJob(form)

        if (validationError) {
            setError(validationError)
            return
        }

        setLoading(true)

        try {
            await jobService.updateJob(id, form)
            navigate(ROUTES.JOBS)
        } catch (err) {
            const errors = err.response?.data?.errors
            const detail = err.response?.data?.detail
            if (errors?.length) {
                setError(errors[0].message)
            } else if (typeof detail === 'string') {
                setError(detail)
            } else {
                setError('Failed to update job.')
            }
        } finally {
            setLoading(false)
        }
    }

    if (fetching) return <p className="loading-text">Loading job...</p>

    return (
        <div>
            <div className="page-header">
                <h2>Edit Job Description</h2>
            </div>

            <div className="form-card">
                {error && <div className="error-msg">{error}</div>}

                <form onSubmit={handleSubmit}>
                    <div className="form-group">
                        <label>Job Title</label>
                        <input
                            name="title"
                            value={form.title}
                            onChange={handleChange}
                            minLength={2}
                            maxLength={100}
                            placeholder="e.g. Backend Developer"
                            required
                        />
                    </div>

                    <div className="form-group">
                        <label>Job Role</label>
                        <input
                            name="role"
                            value={form.role}
                            onChange={handleChange}
                            minLength={2}
                            maxLength={100}
                            placeholder="e.g. Software Engineer"
                            required
                        />
                    </div>

                    <div className="form-group">
                        <label>Job Details</label>
                        <textarea
                            name="details"
                            value={form.details}
                            onChange={handleChange}
                            minLength={10}
                            maxLength={500}
                            placeholder="Describe the role and responsibilities"
                            required
                        />
                    </div>

                    <div className="form-group">
                        <label>Required Skills</label>
                        <input
                            name="required_skills"
                            value={form.required_skills}
                            onChange={handleChange}
                            minLength={2}
                            maxLength={225}
                            placeholder="e.g. Python, FastAPI, MongoDB"
                            required
                        />
                    </div>

                    <div className="form-group">
                        <label>Experience Required</label>
                        <input
                            name="experience_required"
                            value={form.experience_required}
                            onChange={handleChange}
                            placeholder="e.g. 4 years  2.5 years"
                            required
                        />
                    </div>

                    <div className="form-group">
                        <label>Employment Type</label>
                        <select
                            name="employment_type"
                            value={form.employment_type}
                            onChange={handleChange}
                        >
                            <option value="Full Time">Full Time</option>
                            <option value="Internship">Internship</option>
                        </select>
                    </div>

                    <div className="form-group">
                        <label>Location</label>
                        <input
                            name="location"
                            value={form.location}
                            onChange={handleChange}
                            minLength={2}
                            maxLength={100}
                            placeholder="e.g. Bangalore"
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
                            onClick={() => navigate(ROUTES.JOBS)}
                        >
                            Cancel
                        </button>
                    </div>
                </form>
            </div>
        </div>
    )
}