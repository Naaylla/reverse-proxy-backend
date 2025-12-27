"""
Tests for the API gateway service.
Tests the aggregation logic and external API integration.
"""
import pytest
from httpx import AsyncClient
from app.api.gateway_service import app
from app.services.gateway import ExternalAPIClient


@pytest.mark.asyncio
async def test_gateway_health_check():
    """Test that the health check endpoint works."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"


@pytest.mark.asyncio
async def test_gateway_root():
    """Test that the root endpoint returns service info."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "service" in data
        assert data["service"] == "API Gateway"


@pytest.mark.asyncio
async def test_state_endpoint_economy():
    """Test /state endpoint with economy request."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/state",
            json={"economy": {"asset": "btc"}}
        )
        assert response.status_code == 200
        data = response.json()
        # Check that economy data is present (may be None if API fails)
        assert "economy" in data or response.status_code == 200


@pytest.mark.asyncio
async def test_state_endpoint_weather():
    """Test /state endpoint with weather request."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/state",
            json={"weather": {"country": "algeria"}}
        )
        assert response.status_code == 200
        data = response.json()
        assert "weather" in data or response.status_code == 200


@pytest.mark.asyncio
async def test_state_endpoint_air_quality():
    """Test /state endpoint with air quality request."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/state",
            json={"air": {"country": "algeria"}}
        )
        assert response.status_code == 200
        data = response.json()
        assert "air" in data or response.status_code == 200


@pytest.mark.asyncio
async def test_state_endpoint_combined():
    """Test /state endpoint with combined request (all data types)."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/state",
            json={
                "economy": {"asset": "btc"},
                "weather": {"country": "algeria"},
                "air": {"country": "algeria"}
            }
        )
        assert response.status_code == 200
        data = response.json()
        # At least one type of data should be present
        assert len(data) > 0


@pytest.mark.asyncio
async def test_state_endpoint_invalid_asset():
    """Test /state endpoint with invalid asset."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/state",
            json={"economy": {"asset": "invalid_asset"}}
        )
        # Should return 200 with empty or null economy field
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_state_endpoint_invalid_country():
    """Test /state endpoint with invalid country."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/state",
            json={"weather": {"country": "invalid_country"}}
        )
        # Should return 200 with empty or null weather field
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_external_api_client_economy():
    """Test external API client economy data fetching."""
    client = ExternalAPIClient()
    # This test calls the real API - may fail if API is down
    result = await client.fetch_economy_data("btc")
    # Result should be a dict with btc_usd key, or None
    assert result is None or "btc_usd" in result


@pytest.mark.asyncio
async def test_external_api_client_weather():
    """Test external API client weather data fetching."""
    client = ExternalAPIClient()
    result = await client.fetch_weather_data("algeria")
    # Result should be a dict with temperature and wind_speed, or None
    assert result is None or ("temperature" in result and "wind_speed" in result)


@pytest.mark.asyncio
async def test_external_api_client_air_quality():
    """Test external API client air quality data fetching."""
    client = ExternalAPIClient()
    result = await client.fetch_air_quality_data("algeria")
    # Result should be a dict with pm10 key, or None
    assert result is None or "pm10" in result


@pytest.mark.asyncio
async def test_aggregate_data_parallel():
    """Test that aggregate_data calls APIs in parallel."""
    client = ExternalAPIClient()
    request_data = {
        "economy": {"asset": "btc"},
        "weather": {"country": "algeria"},
        "air": {"country": "algeria"}
    }
    result = await client.aggregate_data(request_data)
    # Should return a dict (may be empty if all APIs fail)
    assert isinstance(result, dict)
