import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider, useAuth } from './context/AuthContext'
import MainLayout from './components/layout/MainLayout'
import { ROUTES } from './constants/route'
import Login from './pages/auth/Login'
import ChangePassword from './pages/auth/ChangePassword'

const DashboardPage = () => <div style={{ padding: 24 }}>Dashboard — coming soon</div>
const UsersPage = () => <div style={{ padding: 24 }}>Users — coming soon</div>
const JobsPage = () => <div style={{ padding: 24 }}>Jobs — coming soon</div>
const CandidatesPage = () => <div style={{ padding: 24 }}>Candidates — coming soon</div>
const InterviewsPage = () => <div style={{ padding: 24 }}>Interviews — coming soon</div>
const MyInterviewsPage = () => <div style={{ padding: 24 }}>My Interviews — coming soon</div>

function ProtectedRoute({ children }) {
  const { user, loading } = useAuth()

  if (loading) return <div>Loading...</div>

  if (!user) { return <Navigate to={ROUTES.LOGIN} replace /> }

  if (user.is_password_reset_pending && location.pathname !== ROUTES.CHANGE_PASSWORD) {
    return <Navigate to={ROUTES.CHANGE_PASSWORD} replace />
  }

  return <MainLayout>{children}</MainLayout>
}

function PublicRoute({ children }) {
  const { user, loading } = useAuth()

  if (loading) return <div>Loading...</div>

  if (user?.is_password_reset_pending) {
    return <Navigate to={ROUTES.CHANGE_PASSWORD} replace />
  }

  if (user) return <Navigate to={ROUTES.DASHBOARD} replace />

  return children
}

function AppRoutes() {
  return (
    <Routes>
      {/* Public */}
      <Route path={ROUTES.LOGIN} element={<PublicRoute><Login /></PublicRoute>} />

      {/* Protected */}
      <Route path={ROUTES.CHANGE_PASSWORD} element={<ProtectedRoute><ChangePassword /></ProtectedRoute>} />
      <Route path={ROUTES.DASHBOARD} element={<ProtectedRoute><DashboardPage /></ProtectedRoute>} />
      <Route path={ROUTES.USERS} element={<ProtectedRoute><UsersPage /></ProtectedRoute>} />
      <Route path={ROUTES.JOBS} element={<ProtectedRoute><JobsPage /></ProtectedRoute>} />
      <Route path={ROUTES.CANDIDATES} element={<ProtectedRoute><CandidatesPage /></ProtectedRoute>} />
      <Route path={ROUTES.INTERVIEWS} element={<ProtectedRoute><InterviewsPage /></ProtectedRoute>} />
      <Route path={ROUTES.MY_INTERVIEWS} element={<ProtectedRoute><MyInterviewsPage /></ProtectedRoute>} />

      {/* Default */}
      <Route path="/" element={<Navigate to={ROUTES.LOGIN} replace />} />
      <Route path="*" element={<Navigate to={ROUTES.LOGIN} replace />} />
    </Routes>
  )
}

export default function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <AppRoutes />
      </AuthProvider>
    </BrowserRouter>
  )
}