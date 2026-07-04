import { useState, useEffect } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import candidateService from '../../services/candidateService'
import './Candidates.css'

export default function EditCandidate() {
    const [form, setForm] = useState({
        first_name: '',
        last_name: '',
        mobile_number: '',
        current_company: '',
        total_experience: '',
    })
    const [error, setError] = useState('')
    const [loading, setLoading] = useState(false)
    const [fetching, setFetching] = useState(true)

    const { id } = useParams()
    const navigate = useNavigate()

    useEffect(() => {
        async function loadCandidate() {
            try {
                const candidate = await candidateService.getCandidateById(id)
                setForm({
                    first_name: candidate.first_name,
                    last_name: candidate.last_name,
                    mobile_number: candidate.mobile_number,
                    current_company: candidate.current_company,
                    total_experience: candidate.total_experience,
                })
            } catch {
                setError('Failed to load candidate.')
            } finally {
                setFetching(false)
            }
        }
        loadCandidate()
    }, [id])

    function handleChange(e) {
        setForm({ ...form, [e.target.name]: e.target.value })
    }

    function validate() {
        if (form.mobile_number && !/^\d{10}$/.test(form.mobile_number)) {
            return 'Mobile number must be exactly 10 digits.'
        }
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
            await candidateService.updateCandidate(id, {
                ...form,
                total_experience: parseFloat(form.total_experience),
            })
            navigate(`/candidates/${id}`)
        } catch (err) {
            const errors = err.response?.data?.errors
            const detail = err.response?.data?.detail
            if (errors?.length) {
                setError(errors[0].message)
            } else if (typeof detail === 'string') {
                setError(detail)
            } else {
                setError('Failed to update candidate.')
            }
        } finally {
            setLoading(false)
        }
    }

    if (fetching) return <p className="loading-text">Loading candidate...</p>

    return (
        <div>
            <div className="page-header">
                <h2>Edit Candidate</h2>
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

                    <div className="form-actions">
                        <button type="submit" className="btn btn-primary" disabled={loading}>
                            {loading ? 'Saving...' : 'Save Changes'}
                        </button>
                        <button
                            type="button"
                            className="btn btn-secondary"
                            onClick={() => navigate(`/candidates/${id}`)}
                        >
                            Cancel
                        </button>
                    </div>
                </form>
            </div>
        </div>
    )
}