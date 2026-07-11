import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
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
import StatusHistory from './pages/candidates/StatusHistory'
import InterviewList from './pages/interviews/InterviewList'
import ScheduleInterview from './pages/interviews/ScheduleInterview'
import InterviewDetail from './pages/interviews/InterviewDetail'
import EditInterview from './pages/interviews/EditInterview'
import MyInterviewList from './pages/interviews/MyInterviewList'
import SubmitFeedback from './pages/interviews/SubmitFeedback'
import Dashboard from './pages/dashboard/Dashboard'


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

      {/* Auth */}
      <Route path={ROUTES.CHANGE_PASSWORD} element={<ProtectedRoute><ChangePassword /></ProtectedRoute>} />

      {/* Dashboard — role based inside Dashboard component */}
      <Route path={ROUTES.DASHBOARD} element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />

      {/* Admin */}
      <Route path={ROUTES.USERS} element={<ProtectedRoute allowedRoles={['Admin']}><UserList /></ProtectedRoute>} />
      <Route path={ROUTES.USER_CREATE} element={<ProtectedRoute allowedRoles={['Admin']}><CreateUser /></ProtectedRoute>} />
      <Route path={ROUTES.USER_EDIT} element={<ProtectedRoute allowedRoles={['Admin']}><EditUser /></ProtectedRoute>} />

      {/* HR */}
      <Route path={ROUTES.JOBS} element={<ProtectedRoute allowedRoles={['HR']}><JobList /></ProtectedRoute>} />
      <Route path={ROUTES.JOB_CREATE} element={<ProtectedRoute allowedRoles={['HR']} ><CreateJob /></ProtectedRoute>} />
      <Route path={ROUTES.JOBS_DETAIL} element={<ProtectedRoute allowedRoles={['HR']}><JobDetail /></ProtectedRoute>} />
      <Route path={ROUTES.JOB_EDIT} element={<ProtectedRoute allowedRoles={['HR']}><EditJob /></ProtectedRoute>} />
      <Route path={ROUTES.CANDIDATES} element={<ProtectedRoute allowedRoles={['HR']}><CandidateList /></ProtectedRoute>} />
      <Route path={ROUTES.CANDIDATE_CREATE} element={<ProtectedRoute allowedRoles={['HR']}><CreateCandidate /></ProtectedRoute>} />
      <Route path={ROUTES.CANDIDATE_HISTORY} element={<ProtectedRoute allowedRoles={['HR']}><StatusHistory /></ProtectedRoute>} />
      <Route path={ROUTES.CANDIDATE_DETAIL} element={<ProtectedRoute allowedRoles={['HR']}><CandidateDetail /></ProtectedRoute>} />
      <Route path={ROUTES.CANDIDATE_EDIT} element={<ProtectedRoute allowedRoles={['HR']}><EditCandidate /></ProtectedRoute>} />
      <Route path={ROUTES.INTERVIEWS} element={<ProtectedRoute allowedRoles={['HR']}><InterviewList /></ProtectedRoute>} />
      <Route path={ROUTES.INTERVIEW_CREATE} element={<ProtectedRoute allowedRoles={['HR']}><ScheduleInterview /></ProtectedRoute>} />
      <Route path={ROUTES.INTERVIEW_EDIT} element={<ProtectedRoute allowedRoles={['HR']}><EditInterview /></ProtectedRoute>} />
      <Route path={ROUTES.INTERVIEW_DETAIL} element={<ProtectedRoute allowedRoles={['HR']}><InterviewDetail /></ProtectedRoute>} />

      {/* Interviewer */}
      <Route path={ROUTES.MY_INTERVIEWS} element={<ProtectedRoute allowedRoles={['Interviewer']}><MyInterviewList /></ProtectedRoute>} />
      <Route path={ROUTES.SUBMIT_FEEDBACK} element={<ProtectedRoute allowedRoles={['Interviewer']}><SubmitFeedback /></ProtectedRoute>} />

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