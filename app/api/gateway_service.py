from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.core.config import settings
from app.models.gateway_schemas import StateRequest, StateResponse
from app.services.gateway import ExternalAPIClient
from collections import defaultdict
from datetime import datetime
import time

# Initialize FastAPI application
app = FastAPI(
    title="API Gateway",
    description="Reverse-proxy-backed aggregation gateway for external APIs",
    version="1.0.0"
)

# Metrics storage
metrics = {
    "total_requests": 0,
    "successful_requests": 0,
    "failed_requests": 0,
    "average_response_time_ms": 0,
    "requests_by_asset": defaultdict(int),
    "requests_by_country": defaultdict(int),
    "cache_hits": 0,
    "cache_misses": 0
}

# Rate limiting storage
rate_limits = defaultdict(list)

# Add CORS middleware - fully permissive for now, tighten in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins - update this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rate limiting middleware
@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    """Rate limit: 60 requests per minute per IP"""
    # Skip rate limiting for health checks
    if request.url.path in ["/health", "/health/external", "/metrics"]:
        return await call_next(request)
    
    client_ip = request.client.host
    now = datetime.now()
    
    # Remove old requests (older than 1 minute)
    rate_limits[client_ip] = [
        ts for ts in rate_limits[client_ip] 
        if (now - ts).total_seconds() < 60
    ]
    
    # Check limit (60 requests per minute)
    if len(rate_limits[client_ip]) >= 60:
        return JSONResponse(
            status_code=429,
            content={"error": "Rate limit exceeded", "retry_after": 60, "limit": "60 requests/minute"}
        )
    
    rate_limits[client_ip].append(now)
    return await call_next(request)

# Initialize external API client for aggregation
api_client = ExternalAPIClient(timeout=10.0)


@app.get("/health")
async def health_check():
    """Health check endpoint for Render monitoring."""
    return {"status": "healthy", "service": "gateway"}


@app.post("/state")
async def get_state(request: StateRequest):
    """Main endpoint - aggregates external API data with metrics and timing."""
    start_time = time.time()
    metrics["total_requests"] += 1
    
    try:
        # Track request patterns
        if request.economy:
            metrics["requests_by_asset"][request.economy.asset] += 1
        if request.weather:
            metrics["requests_by_country"][request.weather.country] += 1
        
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
        
        # Track cache metrics
        if api_client._last_was_cached:
            metrics["cache_hits"] += 1
        else:
            metrics["cache_misses"] += 1
        
        # Calculate response time
        duration_ms = (time.time() - start_time) * 1000
        
        # Update metrics
        metrics["successful_requests"] += 1
        metrics["average_response_time_ms"] = (
            metrics["average_response_time_ms"] * 0.9 + duration_ms * 0.1
        )
        
        # Add metadata to response
        response_data = {
            **aggregated_data,
            "_meta": {
                "response_time_ms": round(duration_ms, 2),
                "api_calls": len([k for k in request_dict.keys()]),
                "cached": getattr(api_client, '_last_was_cached', False),
                "timestamp": datetime.now().isoformat()
            }
        }
        
        return response_data
        
    except Exception as e:
        metrics["failed_requests"] += 1
        # Handle unexpected errors
        raise HTTPException(
            status_code=500,
            detail=f"Failed to aggregate data: {str(e)}"
        )


@app.get("/metrics")
async def get_metrics():
    """Get API usage metrics and statistics."""
    total = metrics["total_requests"]
    cache_total = metrics["cache_hits"] + metrics["cache_misses"]
    cache_hit_rate = (metrics["cache_hits"] / cache_total * 100) if cache_total > 0 else 0
    
    return {
        "overview": {
            "total_requests": total,
            "successful_requests": metrics["successful_requests"],
            "failed_requests": metrics["failed_requests"],
            "success_rate": f"{(metrics['successful_requests']/total*100) if total > 0 else 0:.1f}%",
            "average_response_time_ms": round(metrics["average_response_time_ms"], 2)
        },
        "cache": {
            "hits": metrics["cache_hits"],
            "misses": metrics["cache_misses"],
            "hit_rate": f"{cache_hit_rate:.1f}%"
        },
        "popular_assets": dict(sorted(metrics["requests_by_asset"].items(), key=lambda x: x[1], reverse=True)[:5]),
        "popular_countries": dict(sorted(metrics["requests_by_country"].items(), key=lambda x: x[1], reverse=True)[:5])
    }


@app.get("/health/external")
async def external_health():
    """Check health of external API services."""
    import httpx
    from app.core.mappings import COINGECKO_API_URL, OPEN_METEO_WEATHER_URL
    
    results = {}
    
    async with httpx.AsyncClient(timeout=5.0) as client:
        # Test CoinGecko
        try:
            r = await client.get(f"{COINGECKO_API_URL}?ids=bitcoin&vs_currencies=usd")
            results["coingecko"] = "healthy" if r.status_code == 200 else "degraded"
        except Exception:
            results["coingecko"] = "down"
        
        # Test Open-Meteo Weather
        try:
            r = await client.get(f"{OPEN_METEO_WEATHER_URL}?latitude=0&longitude=0&current=temperature_2m")
            results["open_meteo_weather"] = "healthy" if r.status_code == 200 else "degraded"
        except Exception:
            results["open_meteo_weather"] = "down"
        
        # Test Open-Meteo Air Quality
        try:
            from app.core.mappings import OPEN_METEO_AIR_QUALITY_URL
            r = await client.get(f"{OPEN_METEO_AIR_QUALITY_URL}?latitude=0&longitude=0&current=pm10")
            results["open_meteo_air"] = "healthy" if r.status_code == 200 else "degraded"
        except Exception:
            results["open_meteo_air"] = "down"
    
    all_healthy = all(v == "healthy" for v in results.values())
    
    return {
        "status": "all systems operational" if all_healthy else "degraded",
        "services": results,
        "timestamp": datetime.now().isoformat()
    }


@app.get("/")
async def root():
    """Root endpoint with service information."""
    return {
        "service": "API Gateway",
        "version": "1.0.0",
        "description": "Reverse-proxy-backed aggregation service with caching, metrics, and rate limiting",
        "endpoints": {
            "POST /state": "Aggregate external API data",
            "GET /health": "Health check",
            "GET /health/external": "External API health status",
            "GET /metrics": "API usage statistics"
        },
        "features": [
            "Parallel API aggregation",
            "Response caching (30s TTL)",
            "Rate limiting (60 req/min)",
            "Real-time metrics",
            "External service monitoring"
        ],
        "note": "Access via NGINX at /api/state"
    }
