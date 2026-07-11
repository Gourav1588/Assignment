import { useAuth } from '../../context/AuthContext'
import HRDashboard from './HRDashboard'
import InterviewerDashboard from './InterviewerDashboard'
import AdminDashboard from './AdminDashboard'

export default function Dashboard() {
    const { user } = useAuth()

    if (user?.role === 'HR') return <HRDashboard />
    if (user?.role === 'Interviewer') return <InterviewerDashboard />
    if (user?.role === 'Admin') return <AdminDashboard />

    return (
        <div style={{ padding: 24 }}>
            <h2 style={{ fontSize: '20px', color: '#1e293b' }}>Dashboard</h2>
            <p style={{ color: '#64748b', marginTop: '8px' }}>
                Welcome, {user?.full_name}
            </p>
        </div>
    )
}