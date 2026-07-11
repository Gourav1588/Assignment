import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import jobService from '../../services/jobService'
import { ROUTES } from '../../constants/route'
import './Jobs.css'
import { validateJob } from '../../utils/jobValidation'

export default function CreateJob() {
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
    const navigate = useNavigate()

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
            await jobService.createJob(form)
            navigate(ROUTES.JOBS)
        } catch (err) {
            const errors = err.response?.data?.errors
            const detail = err.response?.data?.detail
            if (errors?.length) {
                setError(errors[0].message)
            } else if (typeof detail === 'string') {
                setError(detail)
            } else {
                setError('Failed to create job.')
            }
        } finally {
            setLoading(false)
        }
    }

    return (
        <div>
            <div className="page-header">
                <h2>Create Job Description</h2>
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
                            placeholder="e.g. Backend Developer"
                            minLength={2}
                            maxLength={100}
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
                            maxLength={50}
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
                            placeholder="e.g. 2 or 4 "
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
                            {loading ? 'Creating...' : 'Create Job'}
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