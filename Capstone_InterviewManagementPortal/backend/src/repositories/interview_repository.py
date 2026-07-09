"""
Handles database operations for Interview documents.

Contains:
- create_interview      → inserts a new interview document
- find_all_paginated    → returns paginated interviews for HR
- find_by_interviewer   → returns interviews assigned to specific interviewer
- find_by_id            → returns single interview by ID
- update_interview      → updates interview fields
- count_by_interviewer  → counts interviews assigned to an interviewer
"""
from typing import Optional
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
        HR sees every interview regardless of which interviewer is assigned.
        skip = how many records to jump over based on current page.
        """
        skip = (page - 1) * page_size
        total = await Interview.count()
        interviews = await Interview.find_all().skip(skip).limit(page_size).to_list()
        return interviews, total

    @staticmethod
    async def find_by_interviewer(
        interviewer_id: str, page: int, page_size: int
    ) -> tuple[list[Interview], int]:
        """
        Returns paginated interviews assigned to a specific interviewer.
        Interviewers only see their own interviews .
        """
        skip = (page - 1) * page_size
        query = Interview.find({"interviewer_id": interviewer_id})
        total = await query.count()
        interviews = await query.skip(skip).limit(page_size).to_list()
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
        Other fields stay unchanged.
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
        """
        Counts total interviews assigned to a specific interviewer.
        Used for interviewer dashboard assigned_interviews count.
        """
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
        exclude_id is used during updates to skip the current interview
        so HR can keep the same slot without triggering a conflict.
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

interview_repository = InterviewRepository()