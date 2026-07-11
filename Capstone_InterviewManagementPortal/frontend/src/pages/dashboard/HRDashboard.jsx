import { useState, useEffect } from 'react'
import dashboardService from '../../services/dashboardService'
import '../interviews/Interviews.css'

export default function HRDashboard() {
    const [data, setData] = useState(null)
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState('')

    useEffect(() => {
        async function load() {
            try {
                const result = await dashboardService.getHRDashboard()
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
        { label: 'Total Jobs', count: data.total_jobs },
        { label: 'Total Candidates', count: data.total_candidates },
        { label: 'Scheduled Interviews', count: data.scheduled_interviews },
        { label: 'Selected Candidates', count: data.selected_candidates },
        { label: 'Rejected Candidates', count: data.rejected_candidates },
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