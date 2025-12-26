"""
Common API utilities and health check endpoints.
"""
from fastapi import APIRouter
from app.models.schemas import HealthCheckResponse
from app.core.config import settings

router = APIRouter()


@router.get("/health", response_model=HealthCheckResponse, tags=["Health"])
async def health_check(service_name: str = "Assembly Factory"):
    """
    Health check endpoint.
    Returns the service status and version information.
    """
    return HealthCheckResponse(
        status="healthy",
        service=service_name,
        version=settings.APP_VERSION
    )
