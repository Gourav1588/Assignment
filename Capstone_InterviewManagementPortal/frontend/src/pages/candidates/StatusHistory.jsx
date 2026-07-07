import { useState, useEffect } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import candidateService from '../../services/candidateService'
import { ROUTES } from '../../constants/route'
import './Candidates.css'

export default function StatusHistory() {
    const [candidate, setCandidate] = useState(null)
    const [history, setHistory] = useState([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState('')

    const { id } = useParams()
    const navigate = useNavigate()

    useEffect(() => {
        async function load() {
            try {
                const [c, h] = await Promise.all([
                    candidateService.getCandidateById(id),
                    candidateService.getStatusHistory(id),
                ])
                setCandidate(c)
                setHistory(h)
            } catch {
                setError('Failed to load status history.')
            } finally {
                setLoading(false)
            }
        }
        load()
    }, [id])

    if (loading) return <p className="loading-text">Loading...</p>
    if (error) return <div className="error-msg">{error}</div>

    return (
        <div>
            <div className="page-header">
                <h2>
                    Status History — {candidate.first_name} {candidate.last_name}
                </h2>
                <button
                    className="btn btn-secondary btn-lg"
                    onClick={() => navigate(ROUTES.CANDIDATES)}
                >
                    Back
                </button>
            </div>

            {history.length === 0 ? (
                <p style={{ color: '#94a3b8', fontSize: '14px' }}>
                    No status changes recorded yet.
                </p>
            ) : (
                <div className="table-wrapper">
                    <table className="history-table">
                        <thead>
                            <tr>
                                <th>From</th>
                                <th>To</th>
                                <th>Changed By</th>
                                <th>Date</th>
                            </tr>
                        </thead>
                        <tbody>
                            {history.map((h) => (
                                <tr key={h.id}>
                                    <td>{h.previous_status.replace(/_/g, ' ')}</td>
                                    <td>{h.new_status.replace(/_/g, ' ')}</td>
                                    <td>{h.changed_by}</td>
                                    <td>{new Date(h.changed_at).toLocaleString('en-GB', {
                                        day: '2-digit',
                                        month: '2-digit',
                                        year: 'numeric',
                                    })}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            )}
        </div>
    )
}