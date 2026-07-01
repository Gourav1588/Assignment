"""
This module defines centralized exceptions that carry their own HTTP metadata.
"""
from fastapi import status

class AppException(Exception):
    """
    Base app exception that holds HTTP status codes, error codes, and message details.
    """
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    error_code: str = "INTERNAL_SERVER_ERROR"

    def __init__(self, detail: str):
        self.detail = detail
        super().__init__(self.detail)

class ResourceNotFoundException(AppException):
    """
    Raised when a requested resource or database record cannot be found.
    """
    status_code: int = status.HTTP_404_NOT_FOUND
    error_code: str = "RESOURCE_NOT_FOUND"

class ConflictException(AppException):
    """
    Raised when an action breaks database rules or state constraints.
    """
    status_code: int = status.HTTP_409_CONFLICT
    error_code: str = "RESOURCE_CONFLICT"

class DuplicateEmailException(ConflictException):
    """
    Raised when a user tries to register an email that already exists.
    """
    error_code: str = "DUPLICATE_EMAIL"

class UnauthorizedException(AppException):
    """
    Raised when credentials fail login or identity verification steps.
    """
    status_code: int = status.HTTP_401_UNAUTHORIZED
    error_code: str = "UNAUTHORIZED_ACCESS"

class ForbiddenException(AppException):
    """
    Raised when a logged-in user tries to do something their role does not allow.
    """
    status_code: int = status.HTTP_403_FORBIDDEN
    error_code: str = "INSUFFICIENT_PERMISSIONS"