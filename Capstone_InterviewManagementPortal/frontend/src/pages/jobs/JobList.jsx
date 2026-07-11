import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import jobService from '../../services/jobService'
import { ROUTES } from '../../constants/route'
import './Jobs.css'

export default function JobList() {
    const [jobs, setJobs] = useState([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState('')
    const [page, setPage] = useState(1)
    const [totalPages, setTotalPages] = useState(1)

    const PAGE_SIZE = 10

    const navigate = useNavigate()

    useEffect(() => {
        fetchJobs()
    }, [page])

    async function fetchJobs() {
        setLoading(true)
        try {
            const data = await jobService.getAllJobs(page, PAGE_SIZE)
            setJobs(data.items)
            setTotalPages(data.total_pages)
        } catch {
            setError('Failed to load jobs.')
        } finally {
            setLoading(false)
        }
    }

    if (loading) return <p className="loading-text">Loading jobs...</p>

    return (
        <div>
            <div className="page-header">
                <h2>Job Descriptions</h2>
                <button
                    className="btn btn-primary"
                    onClick={() => navigate(ROUTES.JOB_CREATE)}
                >
                    + Create Job
                </button>
            </div>

            {error && <div className="error-msg">{error}</div>}

            <div className="table-wrapper">
                <table>
                    <thead>
                        <tr>
                            <th>Title</th>
                            <th>Role</th>
                            <th>Location</th>
                            <th>Employment Type</th>
                            <th>Experience</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {jobs.length === 0 ? (
                            <tr>
                                <td colSpan="6" style={{ textAlign: 'center', color: '#94a3b8' }}>
                                    No jobs found
                                </td>
                            </tr>
                        ) : (
                            jobs.map((job) => (
                                <tr key={job.id}>
                                    <td>{job.title}</td>
                                    <td>{job.role}</td>
                                    <td>{job.location}</td>
                                    <td>
                                        <span className="badge">{job.employment_type}</span>
                                    </td>
                                    <td>{job.experience_required} years</td>
                                    <td style={{ display: 'flex', gap: '8px' }}>
                                        <button
                                            className="btn btn-secondary"
                                            style={{ padding: '6px 12px', fontSize: '12px' }}
                                            onClick={() => navigate(`/jobs/${job.id}`)}
                                        >
                                            View
                                        </button>
                                        <button
                                            className="btn btn-warning"
                                            onClick={() => navigate(`/jobs/${job.id}/edit`)}
                                        >
                                            Edit
                                        </button>
                                    </td>
                                </tr>
                            ))
                        )}
                    </tbody>
                </table>
            </div>

            {totalPages > 1 && (
                <div className="pagination">
                    <button
                        className="btn btn-secondary"
                        onClick={() => setPage((p) => p - 1)}
                        disabled={page === 1}
                    >
                        ← Prev
                    </button>

                    <span style={{ fontSize: '13px', color: '#374151', padding: '0 12px' }}>
                        Page {page} of {totalPages}
                    </span>

                    <button
                        className="btn btn-secondary"
                        onClick={() => setPage((p) => p + 1)}
                        disabled={page === totalPages}
                    >
                        Next →
                    </button>

                </div>
            )}

        </div>
    )
}