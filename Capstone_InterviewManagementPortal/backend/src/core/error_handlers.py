"""
This module contains centralized registration handlers to normalize all application errors.
"""
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from bson.errors import InvalidId
from src.core.exceptions import AppException

def register_error_handlers(app: FastAPI) -> None:
    """
    Attaches global exception interceptors to the FastAPI application instance.
    """

    @app.exception_handler(AppException)
    async def handle_app_exception(request: Request, exc: AppException):
        """Catches self-describing domain business exceptions and extracts internal properties."""
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error_code": exc.error_code,
                "detail": exc.detail
            }
        )

    @app.exception_handler(RequestValidationError)
    async def handle_validation_error(request: Request, exc: RequestValidationError):
        """Formats all structural validation failures from Pydantic into a clean, comprehensive layout."""
        formatted_errors = []
        
        for err in exc.errors():
            field = err.get("loc", ["body"])[-1]
            msg = err.get("msg", "Invalid input value.")
            
            if msg.startswith("Value error, "):
                msg = msg.replace("Value error, ", "")
                
            formatted_errors.append({
                "field": str(field),
                "message": msg
            })

        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "error_code": "VALIDATION_ERROR",
                "detail": "Multiple field validations failed.",
                "errors": formatted_errors 
            }
        )
    @app.exception_handler(InvalidId)
    async def handle_invalid_bson_id(request: Request, exc: InvalidId):
        """Catches malformed MongoDB ObjectId hex-strings and forces a clean 400 Bad Request."""
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "error_code": "INVALID_RESOURCE_ID",
                "detail": "The provided database resource ID format is malformed or invalid."
            }
        )

    @app.exception_handler(StarletteHTTPException)
    async def handle_http_exception(request: Request, exc: StarletteHTTPException):
        """Ensures system router-level HTTP errors match the unified application shape."""
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error_code": f"HTTP_ERROR_{exc.status_code}",
                "detail": exc.detail
            }
        )

    @app.exception_handler(Exception)
    async def handle_unexpected(request: Request, exc: Exception):
        """Shields unexpected structural crashes from exposing development logs to users."""
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error_code": "INTERNAL_SERVER_ERROR",
                "detail": "An unexpected internal server error occurred."
            }
        )