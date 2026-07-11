# Interview Management Portal

A full-stack portal for managing the hiring pipeline — job postings, candidate profiles, interview scheduling, interviewer feedback, and hiring decisions — with role-based access for Admin, HR, and Interviewer users.

## Tech Stack

**Backend**
- FastAPI (Python)
- MongoDB with Beanie (ODM) / Motor (async driver)
- Pydantic for request/response validation

**Frontend**
- React 19 + Vite
- React Router
- Axios

## Roles

| Role | Can do |
|---|---|
| **Admin** | Manage user accounts (create, update, activate/deactivate) |
| **HR** | Manage jobs, candidates, and interview scheduling; record hiring decisions |
| **Interviewer** | View assigned interviews, submit feedback |

## Core Flow

1. HR posts a job and registers a candidate against it.
2. HR schedules an interview with an interviewer.
3. Once the interview time passes, the candidate's status auto-advances.
4. The interviewer submits feedback with a recommendation (`NEXT_ROUND`, `SELECT`, or `REJECT`).
5. Based on the latest recommendation, HR either schedules the next round or records the final hiring decision (`SELECTED` / `REJECTED`).

## Project Structure

```
backend/
  src/
    core/        # config, database, security, logging, exceptions
    models/      # MongoDB document models (Beanie)
    schemas/     # request/response validation schemas
    repositories/# database access layer
    services/    # business logic
    routers/     # API endpoints
  tests/

frontend/
  src/
    pages/       # route-level screens (auth, users, jobs, candidates, interviews, dashboard)
    services/    # API client calls
    utils/       # form validation helpers
    context/     # auth context
```

## Getting Started

### Prerequisites
- Python 3.11+
- Node.js 18+
- A running MongoDB instance (local or Atlas)

### Backend

```bash
cd backend
pip install -r requirements.txt
```

Create a `.env` file inside `backend/`:

```
MONGO_URI=mongodb://localhost:27017
DATABASE_NAME=interview_portal_db
DEFAULT_ADMIN_NAME=Admin
DEFAULT_ADMIN_EMAIL=admin@nucleusteq.com
DEFAULT_ADMIN_PASSWORD=ChangeMe123!
```

Run the server:

```bash
uvicorn src.main:app --reload
```

The API will be available at `http://localhost:8000`, with interactive docs at `http://localhost:8000/docs`. A default admin account is seeded automatically on first startup using the credentials above.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

The app will be available at `http://localhost:3000` (or the port Vite reports).

### Tests

```bash
cd backend
pytest
```

## Login

Sign in with the seeded admin account, then create HR and Interviewer accounts from the Admin panel. New accounts must reset their password on first login.
