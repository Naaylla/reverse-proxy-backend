"""
Design Service API
Handles product design processing.
"""
from fastapi import FastAPI, status
from app.core import setup_cors, logger, settings
from app.core.exceptions import setup_exception_handlers
from app.models import ProductRequest, ProcessResponse
from app.services import design_service
from app.api.common import router as common_router

# Create FastAPI application
app = FastAPI(
    title="Design Service",
    description="Handles product design stage",
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
    "/design",
    response_model=ProcessResponse,
    status_code=status.HTTP_200_OK,
    tags=["Design"],
    summary="Process product design",
    description="Processes the design stage for a given product"
)
async def design_endpoint(product: ProductRequest) -> ProcessResponse:
    """
    Design endpoint - processes product design.
    
    Args:
        product: Product information including name
        
    Returns:
        ProcessResponse with design result
    """
    logger.info(f"Design endpoint called for: {product.productName}")
    return design_service.process_design(product)


@app.on_event("startup")
async def startup_event():
    """Log startup information."""
    logger.info(f"Design Service starting on port {settings.DESIGN_PORT}")


@app.on_event("shutdown")
async def shutdown_event():
    """Log shutdown information."""
    logger.info("Design Service shutting down")
