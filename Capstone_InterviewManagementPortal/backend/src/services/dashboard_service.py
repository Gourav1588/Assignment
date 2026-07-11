"""
Business logic for Dashboard module.

Contains:
- get_hr_dashboard          → aggregates counts for HR dashboard
- get_interviewer_dashboard → aggregates counts for Interviewer dashboard
"""
import logging
from src.models.jobs import Job
from src.models.candidates import Candidate
from src.models.interview import Interview
from src.models.feedback import Feedback
from src.enums.candidate_enums import CandidateStatus
from src.repositories.user_repository import user_repository
from src.enums.roles import UserRole
from src.schemas.response.dashboard_response import (
    HRDashboardResponse,
    InterviewerDashboardResponse,
    AdminDashboardResponse
)

logger = logging.getLogger(__name__)


class DashboardService:

    async def get_hr_dashboard(self) -> HRDashboardResponse:
        """
        Returns counts for HR dashboard.
        scheduled_interviews = total interviews minus those with feedback submitted.
        """
        total_jobs       = await Job.count()
        total_candidates = await Candidate.count()

        selected = await Candidate.find(
            Candidate.status == CandidateStatus.SELECTED
        ).count()

        rejected = await Candidate.find(
            Candidate.status == CandidateStatus.REJECTED
        ).count()

        # interviews with no feedback = scheduled (pending)
        total_interviews    = await Interview.count()
        completed_interviews = await Feedback.count()
        scheduled            = total_interviews - completed_interviews

        logger.info("HR dashboard data fetched")
        return HRDashboardResponse(
            total_jobs=total_jobs,
            total_candidates=total_candidates,
            scheduled_interviews=scheduled,
            selected_candidates=selected,
            rejected_candidates=rejected,
        )

    async def get_interviewer_dashboard(
        self, interviewer_id: str
    ) -> InterviewerDashboardResponse:
        """
        Returns counts for Interviewer dashboard.
        All counts scoped to the current interviewer only.
        pending_feedback = assigned interviews minus completed ones.
        """
        assigned = await Interview.find(
            {"interviewer_id": interviewer_id}
        ).count()

        completed = await Feedback.find(
            {"interviewer_id": interviewer_id}
        ).count()

        pending = assigned - completed

        logger.info("Interviewer dashboard fetched for %s", interviewer_id)
        return InterviewerDashboardResponse(
            assigned_interviews=assigned,
            pending_feedback=pending,
            completed_feedback=completed,
        )
        
    async def get_admin_dashboard(self) -> AdminDashboardResponse:
        """
        Returns counts for the Admin dashboard.
        Account figures cover what Admin manages directly. The system figures
        give a read only sense of activity without exposing hiring outcomes.
        """
        total_users   = await user_repository.count_all()
        active_users  = await user_repository.count_active()
        hr_users      = await user_repository.count_by_role(UserRole.HR)
        interviewers  = await user_repository.count_by_role(UserRole.INTERVIEWER)

        total_jobs       = await Job.count()
        total_candidates = await Candidate.count()
        total_interviews = await Interview.count()

        logger.info("Admin dashboard data fetched")
        return AdminDashboardResponse(
            total_users=total_users,
            active_users=active_users,
            disabled_users=total_users - active_users,
            hr_users=hr_users,
            interviewers=interviewers,
            total_jobs=total_jobs,
            total_candidates=total_candidates,
            total_interviews=total_interviews,
        )



dashboard_service = DashboardService()