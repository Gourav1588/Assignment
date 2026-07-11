"""
Handles database operations for Feedback documents.

Contains:
- create_feedback       → inserts a new feedback document
- find_by_interview     → returns feedback for a specific interview
- exists_for_interview  → checks if feedback already exists for an interview
- count_by_interviewer  → counts feedback submitted by an interviewer
"""
from typing import Optional
from src.models.feedback import Feedback


class FeedbackRepository:

    @staticmethod
    async def create_feedback(document: Feedback) -> Feedback:
        """Insert a new feedback document."""
        await document.insert()
        return document

    @staticmethod
    async def find_by_interview(interview_id: str) -> Optional[Feedback]:
        """
        Returns feedback for a specific interview.
        Returns None if no feedback submitted yet.
        """
        return await Feedback.find_one(
          {"interview_id": interview_id}
        )

    @staticmethod
    async def exists_for_interview(interview_id: str) -> bool:
        """
        Checks if feedback already exists for an interview.
        Used to prevent duplicate feedback submission.
        """
        result = await Feedback.find_one(         
            {"interview_id": interview_id}
        )
        
        return result is not None 

    @staticmethod
    async def count_by_interviewer(interviewer_id: str) -> int:
        """
        Counts feedback documents submitted by a specific interviewer.
        """
        return await Feedback.find(
             {"interviewer_id": interviewer_id}).count()


feedback_repository = FeedbackRepository()