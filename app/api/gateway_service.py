from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.middleware import LoggingMiddleware
from app.models.gateway_schemas import StateRequest, StateResponse
from app.services.gateway import ExternalAPIClient

# Initialize FastAPI application
app = FastAPI(
    title="API Gateway",
    description="Reverse-proxy-backed aggregation gateway for external APIs",
    version="1.0.0"
)

# Add CORS middleware - fully permissive for now, tighten in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins - update this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add logging middleware
app.add_middleware(LoggingMiddleware)

# Initialize external API client for aggregation
api_client = ExternalAPIClient(timeout=10.0)


@app.get("/health")
async def health_check():
    
    return {"status": "healthy", "service": "gateway"}


@app.post("/state", response_model=StateResponse)
async def get_state(request: StateRequest):

    try:
        # Convert Pydantic model to dict for processing
        request_dict = {}
        
        if request.economy:
            request_dict["economy"] = {"asset": request.economy.asset}
        
        if request.weather:
            request_dict["weather"] = {"country": request.weather.country}
        
        if request.air:
            request_dict["air"] = {"country": request.air.country}
        
        # Aggregate data from external APIs in parallel
        aggregated_data = await api_client.aggregate_data(request_dict)
        
        # Return raw aggregated values only (no additional processing)
        return StateResponse(**aggregated_data)
        
    except Exception as e:
        # Handle unexpected errors
        raise HTTPException(
            status_code=500,
            detail=f"Failed to aggregate data: {str(e)}"
        )


@app.get("/")
async def root():
    """Root endpoint with service information."""
    return {
        "service": "API Gateway",
        "description": "Reverse-proxy-backed aggregation service",
        "endpoints": {
            "POST /state": "Aggregate external API data",
            "GET /health": "Health check"
        },
        "note": "Access via NGINX at /api/state"
    }
