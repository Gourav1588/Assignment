import { BrowserRouter, Routes, Route, Navigate, useLocation } from 'react-router-dom'
import { AuthProvider, useAuth } from './context/AuthContext'
import MainLayout from './components/layout/MainLayout'
import { ROUTES } from './constants/route'
import Login from './pages/auth/Login'
import ChangePassword from './pages/auth/ChangePassword'
import UserList from './pages/users/UserList'
import EditUser from './pages/users/EditUser'
import CreateUser from './pages/users/CreateUser'
import JobList from './pages/jobs/JobList'
import CreateJob from './pages/jobs/CreateJob'
import EditJob from './pages/jobs/EditJob'
import JobDetail from './pages/jobs/JobDetail'
import CandidateList from './pages/candidates/CandidateList'
import CreateCandidate from './pages/candidates/CreateCandidate'
import CandidateDetail from './pages/candidates/CandidateDetail'
import EditCandidate from './pages/candidates/EditCandidate'

const DashboardPage = () => <div style={{ padding: 24 }}>Dashboard — coming soon</div>
const InterviewsPage = () => <div style={{ padding: 24 }}>Interviews — coming soon</div>
const MyInterviewsPage = () => <div style={{ padding: 24 }}>My Interviews — coming soon</div>

function ProtectedRoute({ children, allowedRoles }) {
  const { user, loading } = useAuth()

  if (loading) return <div>Loading...</div>

  if (!user) { return <Navigate to={ROUTES.LOGIN} replace /> }

  if (user.is_password_reset_pending && location.pathname !== ROUTES.CHANGE_PASSWORD) {
    return <Navigate to={ROUTES.CHANGE_PASSWORD} replace />
  }

  if (allowedRoles && !allowedRoles.includes(user?.role)) {
    return (
      <MainLayout>
        <div style={{ padding: 24, color: '#dc2626', fontWeight: 'bold' }}>
          Unauthorized Access: You do not have permission to view this page.
        </div>
      </MainLayout>
    )
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
      <Route path={ROUTES.USERS} element={<ProtectedRoute allowedRoles={['Admin']}><UserList /></ProtectedRoute>} />
      <Route path={ROUTES.USER_CREATE} element={<ProtectedRoute allowedRoles={['Admin']}><CreateUser /></ProtectedRoute>} />
      <Route path={ROUTES.USER_EDIT} element={<ProtectedRoute allowedRoles={['Admin']}><EditUser /></ProtectedRoute>} />
      <Route path={ROUTES.JOBS} element={<ProtectedRoute allowedRoles={['HR']}><JobList /></ProtectedRoute>} />
      <Route path={ROUTES.JOB_CREATE} element={<ProtectedRoute allowedRoles={['HR']} ><CreateJob /></ProtectedRoute>} />
      <Route path={ROUTES.JOBS_DETAIL} element={<ProtectedRoute allowedRoles={['HR']}><JobDetail /></ProtectedRoute>} />
      <Route path={ROUTES.JOB_EDIT} element={<ProtectedRoute allowedRoles={['HR']}><EditJob /></ProtectedRoute>} />
      <Route path={ROUTES.CANDIDATES} element={<ProtectedRoute allowedRoles={['HR']}><CandidateList /></ProtectedRoute>} />
      <Route path={ROUTES.CANDIDATE_CREATE} element={<ProtectedRoute allowedRoles={['HR']}><CreateCandidate /></ProtectedRoute>} />
      <Route path={ROUTES.CANDIDATE_DETAIL} element={<ProtectedRoute allowedRoles={['HR']}><CandidateDetail /></ProtectedRoute>} />
      <Route path={ROUTES.CANDIDATE_EDIT} element={<ProtectedRoute allowedRoles={['HR']}><EditCandidate /></ProtectedRoute>} />
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