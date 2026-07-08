"""
Enums for Interview and Feedback modules.

RecommendationEnum → what interviewer recommends after interview
                     NEXT_ROUND = candidate needs another interview
                     SELECT     = candidate should be hired
                     REJECT     = candidate should not be hired
"""
from enum import StrEnum


class RecommendationEnum(StrEnum):
    NEXT_ROUND = "NEXT_ROUND"
    SELECT     = "SELECT"
    REJECT     = "REJECT"