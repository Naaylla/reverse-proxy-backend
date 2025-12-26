"""
Assembly Service API
Handles product assembly processing.
"""
from fastapi import FastAPI, status
from app.core import setup_cors, logger, settings
from app.core.exceptions import setup_exception_handlers
from app.models import ProductRequest, ProcessResponse
from app.services import assembly_service
from app.api.common import router as common_router

# Create FastAPI application
app = FastAPI(
    title="Assembly Service",
    description="Handles product assembly stage",
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
    "/assemble",
    response_model=ProcessResponse,
    status_code=status.HTTP_200_OK,
    tags=["Assembly"],
    summary="Process product assembly",
    description="Processes the assembly stage for a given product"
)
async def assembly_endpoint(product: ProductRequest) -> ProcessResponse:
    """
    Assembly endpoint - processes product assembly.
    
    Args:
        product: Product information including name
        
    Returns:
        ProcessResponse with assembly result
    """
    logger.info(f"Assembly endpoint called for: {product.productName}")
    return assembly_service.process_assembly(product)


@app.on_event("startup")
async def startup_event():
    """Log startup information."""
    logger.info(f"Assembly Service starting on port {settings.ASSEMBLY_PORT}")


@app.on_event("shutdown")
async def shutdown_event():
    """Log shutdown information."""
    logger.info("Assembly Service shutting down")
