import { useState, useEffect } from 'react'
import dashboardService from '../../services/dashboardService'
import '../interviews/Interviews.css'

export default function InterviewerDashboard() {
    const [data, setData] = useState(null)
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState('')

    useEffect(() => {
        async function load() {
            try {
                const result = await dashboardService.getInterviewerDashboard()
                setData(result)
            } catch {
                setError('Failed to load dashboard.')
            } finally {
                setLoading(false)
            }
        }
        load()
    }, [])

    if (loading) return <p className="loading-text">Loading dashboard...</p>
    if (error) return <div className="error-msg">{error}</div>

    const cards = [
        { label: 'Assigned Interviews', count: data.assigned_interviews },
        { label: 'Pending Feedback', count: data.pending_feedback },
        { label: 'Completed Feedback', count: data.completed_feedback },
    ]

    return (
        <div>
            <div className="page-header">
                <h2>Dashboard</h2>
            </div>

            <div className="dashboard-grid">
                {cards.map((card) => (
                    <div key={card.label} className="dashboard-card">
                        <div className="count">{card.count}</div>
                        <div className="label">{card.label}</div>
                    </div>
                ))}
            </div>
        </div>
    )
}