import { useState, useEffect } from 'react'
import dashboardService from '../../services/dashboardService'
import '../interviews/Interviews.css'

export default function AdminDashboard() {
    const [data, setData] = useState(null)
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState('')

    useEffect(() => {
        async function load() {
            try {
                const result = await dashboardService.getAdminDashboard()
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

    const userCards = [
        { label: 'Total Users', count: data.total_users },
        { label: 'Active Users', count: data.active_users },
        { label: 'Disabled Users', count: data.disabled_users },
        { label: 'HR Users', count: data.hr_users },
        { label: 'Interviewers', count: data.interviewers },
    ]

    const systemCards = [
        { label: 'Total Jobs', count: data.total_jobs },
        { label: 'Total Candidates', count: data.total_candidates },
        { label: 'Total Interviews', count: data.total_interviews },
    ]

    return (
        <div>
            <div className="page-header">
                <h2>Dashboard</h2>
            </div>

            <h3 style={{ fontSize: '15px', color: '#1e293b', marginTop: '8px' }}>
                User Management
            </h3>
            <div className="dashboard-grid">
                {userCards.map((card) => (
                    <div key={card.label} className="dashboard-card">
                        <div className="count">{card.count}</div>
                        <div className="label">{card.label}</div>
                    </div>
                ))}
            </div>

            <h3 style={{ fontSize: '15px', color: '#1e293b', marginTop: '28px' }}>
                System Overview
            </h3>
            <div className="dashboard-grid">
                {systemCards.map((card) => (
                    <div key={card.label} className="dashboard-card">
                        <div className="count">{card.count}</div>
                        <div className="label">{card.label}</div>
                    </div>
                ))}
            </div>
        </div>
    )
}