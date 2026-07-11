export const ROUTES = {
  LOGIN: '/login',
  CHANGE_PASSWORD: '/change-password',
  DASHBOARD: '/dashboard',
  USERS: '/users',
  USER_CREATE: '/users/create',
  USER_EDIT: '/users/:id/edit',
  JOBS: '/jobs',
  JOBS_DETAIL: '/jobs/:id',
  JOB_CREATE: '/jobs/create',
  JOB_EDIT: '/jobs/:id/edit',
  CANDIDATES: '/candidates',
  CANDIDATE_CREATE: '/candidates/create',
  CANDIDATE_DETAIL: '/candidates/:id',
  CANDIDATE_EDIT: '/candidates/:id/edit',
  CANDIDATE_HISTORY: '/candidates/:id/history',
  INTERVIEWS: '/interviews',
  INTERVIEW_CREATE: '/interviews/create',
  INTERVIEW_EDIT: '/interviews/:id/edit',
  MY_INTERVIEWS: '/my-interviews',
  SUBMIT_FEEDBACK: '/my-interviews/:id/feedback',
  INTERVIEW_DETAIL: '/interviews/:id'
}

export const NAV_ITEMS = {
  Admin: [
    { label: 'Dashboard', path: ROUTES.DASHBOARD },
    { label: 'Users', path: ROUTES.USERS },
  ],
  HR: [
    { label: 'Dashboard', path: ROUTES.DASHBOARD },
    { label: 'Jobs', path: ROUTES.JOBS },
    { label: 'Candidates', path: ROUTES.CANDIDATES },
    { label: 'Interviews', path: ROUTES.INTERVIEWS },
  ],
  Interviewer: [
    { label: 'Dashboard', path: ROUTES.DASHBOARD },
    { label: 'My Interviews', path: ROUTES.MY_INTERVIEWS },
  ],
}