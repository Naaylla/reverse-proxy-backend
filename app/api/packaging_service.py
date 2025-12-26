"""
Packaging Service API
Handles product packaging processing.
"""
from fastapi import FastAPI, status
from app.core import setup_cors, logger, settings
from app.core.exceptions import setup_exception_handlers
from app.models import ProductRequest, ProcessResponse
from app.services import packaging_service
from app.api.common import router as common_router

# Create FastAPI application
app = FastAPI(
    title="Packaging Service",
    description="Handles product packaging stage",
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
    "/package",
    response_model=ProcessResponse,
    status_code=status.HTTP_200_OK,
    tags=["Packaging"],
    summary="Process product packaging",
    description="Processes the packaging stage for a given product"
)
async def packaging_endpoint(product: ProductRequest) -> ProcessResponse:
    """
    Packaging endpoint - processes product packaging.
    
    Args:
        product: Product information including name
        
    Returns:
        ProcessResponse with packaging result
    """
    logger.info(f"Packaging endpoint called for: {product.productName}")
    return packaging_service.process_packaging(product)


@app.on_event("startup")
async def startup_event():
    """Log startup information."""
    logger.info(f"Packaging Service starting on port {settings.PACKAGING_PORT}")


@app.on_event("shutdown")
async def shutdown_event():
    """Log shutdown information."""
    logger.info("Packaging Service shutting down")
