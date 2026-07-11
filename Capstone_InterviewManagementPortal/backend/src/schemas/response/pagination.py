"""
Shared pagination response wrapper used across all list endpoints.
"""
from typing import Generic, TypeVar
from pydantic import BaseModel

T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    """
    Wraps any list response with pagination metadata.

    items       → records for the current page
    total       → total number of records in the collection
    page        → current page number (1-based)
    page_size   → number of records per page
    total_pages → total number of pages
    """
    items: list[T]
    total: int
    page: int
    page_size: int
    total_pages: int