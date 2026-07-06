"""
This module defines the authorized  user tier access classifications.
"""

from enum import Enum

class UserRole(str, Enum):
    ADMIN = "Admin"
    HR = "HR"
    INTERVIEWER = "Interviewer"