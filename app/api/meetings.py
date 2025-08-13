# app/api/meetings.py

from fastapi import APIRouter, HTTPException
from datetime import datetime

router = APIRouter()

@router.get("/health")
async def health_check():
    """
    Health check endpoint for the meetings API
    """
    return {
        "status": "healthy",
        "service": "Triangle Meeting Analysis API",
        "timestamp": datetime.now().isoformat(),
        "message": "Meetings API is ready for development"
    }

@router.get("/")
async def meetings_info():
    """
    Basic info about the meetings API
    """
    return {
        "message": "Triangle Meeting Intelligence API",
        "endpoints": [
            "/health - Health check",
            "More endpoints coming soon..."
        ],
        "status": "MVP Development Phase"
    }