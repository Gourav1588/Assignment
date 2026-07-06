"""
This module initializes the FastAPI server engine and registers all endpoint routers.

Contains:
- lifespan → Manages application lifecycle hooks for database operations
"""
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.core.database import Database
from src.routers.auth import router as auth_router
from src.core.error_handlers import register_error_handlers


logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handles startup database connections and handles clean shutdowns.
    """
    try:
        logger.info("Initializing MongoDB client connection and binding Beanie models...")
        await Database.connect_db()  # Initialize the MongoDB client connection and bind Beanie models
    except Exception as e:
        logger.critical(f"Failed to connect to MongoDB during startup: {e}")
        raise e
    
    yield
    
    logger.info("Safely closing down database pool connections on shutdown...") 
    Database.close_db()          # Safely close down database pool connections on shutdown
    

app = FastAPI(
    title="Interview Management Portal",
    description="Backend API engine managing candidates, jobs, and panel evaluations",
    version="1.0.0",
    lifespan=lifespan
)

register_error_handlers(app)  # Binds custom global exceptions to standardized JSON handlers

ALLOWED_ORIGINS = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api/v1")  