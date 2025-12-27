"""
API Gateway Service - Single entry point for aggregated external data.

This service implements a reverse-proxy-backed API gateway pattern:
- NGINX acts as the public reverse proxy (single entry point)
- This gateway service aggregates data from multiple external APIs
- Frontend never calls external APIs directly
- All routing and API selection happens in the backend
- Returns only raw values with no business logic

Architecture:
    Frontend -> NGINX (reverse proxy) -> Gateway Service -> External APIs
"""
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
    """
    Health check endpoint for monitoring.
    NGINX can use this to verify the gateway service is running.
    """
    return {"status": "healthy", "service": "gateway"}


@app.post("/state", response_model=StateResponse)
async def get_state(request: StateRequest):
    """
    Main aggregation endpoint - returns raw data from multiple external APIs.
    
    This endpoint demonstrates the API gateway aggregation pattern:
    1. Frontend sends a single request specifying what data it needs
    2. Gateway service routes to appropriate external APIs in parallel
    3. External API responses are aggregated and normalized
    4. Only raw values are returned (no status, thresholds, or game logic)
    
    Request Body Example:
        {
            "economy": {"asset": "btc"},
            "weather": {"country": "algeria"},
            "air": {"country": "algeria"}
        }
    
    Response Example:
        {
            "economy": {"btc_usd": 68421},
            "weather": {"temperature": 22, "wind_speed": 15.2},
            "air": {"pm10": 45}
        }
    
    Note: NGINX routes /api/state to this endpoint. Frontend calls /api/state,
          NGINX proxies it here, keeping external API details hidden.
    """
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
