"""
Quality Service API
Handles product quality checking.
"""
from fastapi import FastAPI, status
from app.core import setup_cors, logger, settings
from app.core.exceptions import setup_exception_handlers
from app.models import ProductRequest, ProcessResponse
from app.services import quality_service
from app.api.common import router as common_router

# Create FastAPI application
app = FastAPI(
    title="Quality Service",
    description="Handles product quality checking stage",
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Setup middleware and exception handlers
setup_cors(app)
setup_exception_handlers(app)

# Include common routes (health check)
app.include_router(common_router)


@app.post(
    "/quality",
    response_model=ProcessResponse,
    status_code=status.HTTP_200_OK,
    tags=["Quality"],
    summary="Process quality check",
    description="Processes the quality checking stage for a given product"
)
async def quality_endpoint(product: ProductRequest) -> ProcessResponse:
    """
    Quality endpoint - processes quality check.
    
    Args:
        product: Product information including name
        
    Returns:
        ProcessResponse with quality check result
    """
    logger.info(f"Quality endpoint called for: {product.productName}")
    return quality_service.process_quality(product)


@app.on_event("startup")
async def startup_event():
    """Log startup information."""
    logger.info(f"Quality Service starting on port {settings.QUALITY_PORT}")


@app.on_event("shutdown")
async def shutdown_event():
    """Log shutdown information."""
    logger.info("Quality Service shutting down")
