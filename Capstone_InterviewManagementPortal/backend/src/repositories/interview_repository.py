"""
Handles database operations for Interview documents.

Contains:
- create_interview               → inserts a new interview document
- find_all_paginated             → returns paginated interviews for HR
- find_by_interviewer            → returns interviews assigned to an interviewer
- find_by_id                     → returns single interview by ID
- update_interview               → updates interview fields
- count_by_interviewer           → counts interviews assigned to an interviewer
- find_conflict_for_candidate    → checks candidate double booking
- find_conflict_for_interviewer  → checks interviewer double booking
- find_upcoming_for_interviewer  → future interviews assigned to an interviewer
- find_by_candidate              → all interviews for a candidate, newest first
- find_latest_for_candidate      → most recent interview for a candidate
"""
from typing import Optional
from datetime import date
from src.models.interview import Interview


class InterviewRepository:

    @staticmethod
    async def create_interview(document: Interview) -> Interview:
        """Insert a new interview document."""
        await document.insert()
        return document

    @staticmethod
    async def find_all_paginated(
        page: int, page_size: int
    ) -> tuple[list[Interview], int]:
        """
        Returns paginated list of all interviews for HR.
        skip = how many records to jump over based on current page.
        """
        skip = (page - 1) * page_size
        total = await Interview.count()
        interviews = await Interview.find_all().sort("-_id").skip(skip).limit(page_size).to_list()
        return interviews, total

    @staticmethod
    async def find_by_interviewer(
        interviewer_id: str, page: int, page_size: int
    ) -> tuple[list[Interview], int]:
        """Returns paginated interviews assigned to a specific interviewer."""
        skip = (page - 1) * page_size
        query = Interview.find({"interviewer_id": interviewer_id})
        total = await query.count()
        interviews = await query.sort("-_id").skip(skip).limit(page_size).to_list()
        return interviews, total

    @staticmethod
    async def find_by_id(interview_id: str) -> Optional[Interview]:
        """Returns single interview by ID or None if not found."""
        try:
            return await Interview.get(interview_id)
        except Exception:
            return None

    @staticmethod
    async def update_interview(
        interview_id: str, update_data: dict
    ) -> Optional[Interview]:
        """
        Updates specific fields on an existing interview document.
        Only fields present in update_data are changed.
        """
        interview = await InterviewRepository.find_by_id(interview_id)
        if not interview:
            return None
        for field, value in update_data.items():
            setattr(interview, field, value)
        await interview.save()
        return interview

    @staticmethod
    async def count_by_interviewer(interviewer_id: str) -> int:
        """Counts total interviews assigned to a specific interviewer."""
        return await Interview.find(
            {"interviewer_id": interviewer_id}
        ).count()

    @staticmethod
    async def find_conflict_for_candidate(
        candidate_id: str,
        interview_date: str,
        interview_time: str,
        exclude_id: str | None = None,
    ) -> Optional[Interview]:
        """
        Checks if candidate already has an interview at the same date and time.
        exclude_id is used during updates to skip the current interview.
        """
        existing = await Interview.find_one({
            "candidate_id":   candidate_id,
            "interview_date": interview_date,
            "interview_time": interview_time,
        })

        if existing and exclude_id and str(existing.id) == exclude_id:
            return None
        return existing

    @staticmethod
    async def find_conflict_for_interviewer(
        interviewer_id: str,
        interview_date: str,
        interview_time: str,
        exclude_id: str | None = None,
    ) -> Optional[Interview]:
        """
        Checks if interviewer already has an interview at the same date and time.
        exclude_id is used during updates to skip the current interview.
        """
        existing = await Interview.find_one({
            "interviewer_id": interviewer_id,
            "interview_date": interview_date,
            "interview_time": interview_time,
        })
        if existing and exclude_id and str(existing.id) == exclude_id:
            return None
        return existing

    @staticmethod
    async def find_upcoming_for_interviewer(interviewer_id: str) -> list[Interview]:
        """Returns interviews assigned to an interviewer scheduled today or later."""
        today = date.today().isoformat()
        return await Interview.find({
            "interviewer_id": interviewer_id,
            "interview_date": {"$gte": today},
        }).to_list()

    @staticmethod
    async def find_by_candidate(candidate_id: str) -> list[Interview]:
        """
        Returns all interviews for a candidate, most recent slot first.
        Date and time are zero-padded strings, so sorting on them
        gives correct chronological order.
        """
        return await Interview.find(
            {"candidate_id": candidate_id}
        ).sort("-interview_date", "-interview_time").to_list()

    @staticmethod
    async def find_latest_for_candidate(candidate_id: str) -> Optional[Interview]:
        """Returns the candidate's most recently scheduled interview, if any."""
        interviews = await InterviewRepository.find_by_candidate(candidate_id)
        return interviews[0] if interviews else None


interview_repository = InterviewRepository()