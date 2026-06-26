export const ROUTES = {
  LOGIN:            '/login',
  RESET_PASSWORD:   '/reset-password',
  DASHBOARD:        '/dashboard',
  USERS:            '/users',
  USER_CREATE:      '/users/create',
  USER_EDIT:        '/users/:id/edit',
  JOBS:             '/jobs',
  JOB_CREATE:       '/jobs/create',
  JOB_EDIT:         '/jobs/:id/edit',
  CANDIDATES:       '/candidates',
  CANDIDATE_CREATE: '/candidates/create',
  CANDIDATE_DETAIL: '/candidates/:id',
  INTERVIEWS:       '/interviews',
  INTERVIEW_CREATE: '/interviews/create',
  MY_INTERVIEWS:    '/my-interviews',
}

export const NAV_ITEMS = {
  Admin: [
    { label: 'Dashboard', path: ROUTES.DASHBOARD },
    { label: 'Users',     path: ROUTES.USERS },
  ],
  HR: [
    { label: 'Dashboard',  path: ROUTES.DASHBOARD  },
    { label: 'Jobs',       path: ROUTES.JOBS       },
    { label: 'Candidates', path: ROUTES.CANDIDATES },
    { label: 'Interviews', path: ROUTES.INTERVIEWS },
  ],
  Interviewer: [
    { label: 'Dashboard',     path: ROUTES.DASHBOARD     },
    { label: 'My Interviews', path: ROUTES.MY_INTERVIEWS },
  ],
}