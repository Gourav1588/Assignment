import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import interviewService from '../../services/interviewService'
import { ROUTES } from '../../constants/route'
import { hasInterviewPassed } from '../../utils/interviewTime'
import './Interviews.css'

export default function InterviewList() {
    const [interviews, setInterviews] = useState([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState('')
    const [page, setPage] = useState(1)
    const [totalPages, setTotalPages] = useState(1)
    const PAGE_SIZE = 10
    const navigate = useNavigate()

    useEffect(() => {
        fetchInterviews()
    }, [page])

    async function fetchInterviews() {
        setLoading(true)
        setError('')
        try {
            const data = await interviewService.getAllInterviews(page, PAGE_SIZE)
            setInterviews(data.items)
            setTotalPages(data.total_pages)
        } catch {
            setError('Failed to load interviews.')
        } finally {
            setLoading(false)
        }
    }

    if (loading) return <p className="loading-text">Loading interviews...</p>

    return (
        <div>
            <div className="page-header">
                <h2>Interviews</h2>
                <button
                    className="btn btn-primary"
                    onClick={() => navigate(ROUTES.INTERVIEW_CREATE)}
                >
                    + Schedule Interview
                </button>
            </div>

            {error && <div className="error-msg">{error}</div>}

            <div className="table-wrapper">
                <table>
                    <thead>
                        <tr>
                            <th>Job Title</th>
                            <th>Date</th>
                            <th>Time</th>
                            <th>Focus Areas</th>
                            <th>Status</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {interviews.length === 0 ? (
                            <tr>
                                <td colSpan="6" style={{ textAlign: 'center', color: '#94a3b8' }}>
                                    No interviews scheduled
                                </td>
                            </tr>
                        ) : (
                            interviews.map((i) => {
                                const passed = hasInterviewPassed(i.interview_date, i.interview_time)

                                return (
                                    <tr key={i.id}>
                                        <td>{i.job_title}</td>
                                        <td>{i.interview_date}</td>
                                        <td>{i.interview_time}</td>
                                        <td>{i.focus_areas}</td>
                                        <td>
                                            <span className={passed ? 'badge badge-completed' : 'badge badge-scheduled'}>
                                                {passed ? 'Completed' : 'Scheduled'}
                                            </span>
                                        </td>
                                        <td style={{ display: 'flex', gap: '8px' }}>
                                            <button
                                                className="btn btn-secondary"
                                                style={{ padding: '6px 12px', fontSize: '12px' }}
                                                onClick={() => navigate(`/interviews/${i.id}`)}
                                            >
                                                View
                                            </button>
                                            <button
                                                className="btn btn-warning"
                                                disabled={passed}
                                                title={passed ? 'Interview has already taken place' : ''}
                                                onClick={() => navigate(`/interviews/${i.id}/edit`)}
                                            >
                                                Edit
                                            </button>
                                        </td>
                                    </tr>
                                )
                            })
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