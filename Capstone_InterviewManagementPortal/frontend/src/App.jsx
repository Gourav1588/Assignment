import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider, useAuth } from './context/AuthContext'
import MainLayout from './components/layout/MainLayout'
import { ROUTES } from './constants/route'
import Login from './pages/auth/Login'
import ResetPassword from './pages/auth/ResetPassword'
import UserList from './pages/users/UserList'
import EditUser from './pages/users/EditUser'
import CreateUser from './pages/users/CreateUser'

const DashboardPage = () => <div style={{ padding: 24 }}>Dashboard — coming soon</div>
const UsersPage = () => <div style={{ padding: 24 }}>Users — coming soon</div>
const JobsPage = () => <div style={{ padding: 24 }}>Jobs — coming soon</div>
const CandidatesPage = () => <div style={{ padding: 24 }}>Candidates — coming soon</div>
const InterviewsPage = () => <div style={{ padding: 24 }}>Interviews — coming soon</div>
const MyInterviewsPage = () => <div style={{ padding: 24 }}>My Interviews — coming soon</div>

function ProtectedRoute({ children, allowedRoles }) {
  const { user, pendingUser, loading } = useAuth()

  if (loading) return <div>Loading...</div>


  if (!user && !pendingUser) {
    return <Navigate to={ROUTES.LOGIN} replace />
  }

  if (pendingUser?.is_password_reset_pending) {
    return <Navigate to={ROUTES.RESET_PASSWORD} replace />
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


  if (user) return <Navigate to={ROUTES.DASHBOARD} replace />

  return children
}

function AppRoutes() {
  return (
    <Routes>
      {/* Public */}
      <Route path={ROUTES.LOGIN} element={<PublicRoute><Login /></PublicRoute>} />
      <Route path={ROUTES.RESET_PASSWORD} element={<ResetPassword />} />

      {/* Protected */}
      <Route path={ROUTES.DASHBOARD} element={<ProtectedRoute><DashboardPage /></ProtectedRoute>} />
      <Route path={ROUTES.USERS} element={<ProtectedRoute allowedRoles={['Admin']}><UserList /></ProtectedRoute>} />
      <Route path={ROUTES.USER_CREATE} element={<ProtectedRoute allowedRoles={['Admin']}><CreateUser /></ProtectedRoute>} />
      <Route path={ROUTES.USER_EDIT} element={<ProtectedRoute allowedRoles={['Admin']}><EditUser /></ProtectedRoute>} />
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