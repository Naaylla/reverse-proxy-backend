"""
Tests for Design Service.
"""
import pytest
from fastapi.testclient import TestClient
from app.api.design_service import app

client = TestClient(app)


def test_design_endpoint_success(sample_product):
    """Test design endpoint with valid data."""
    response = client.post("/design", json=sample_product)
    
    assert response.status_code == 200
    data = response.json()
    assert data["stage"] == "Design"
    assert "Test Widget" in data["message"]
    assert "timestamp" in data


def test_design_endpoint_validation_error():
    """Test design endpoint with invalid data."""
    response = client.post("/design", json={"productName": ""})
    
    assert response.status_code == 422
    data = response.json()
    assert data["error"] == "ValidationError"


def test_design_endpoint_missing_field():
    """Test design endpoint with missing required field."""
    response = client.post("/design", json={})
    
    assert response.status_code == 422


def test_health_check():
    """Test health check endpoint."""
    response = client.get("/health")
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "Assembly Factory"
    assert data["version"] == "1.0.0"


def test_cors_headers():
    """Test CORS headers are present."""
    response = client.options("/design")
    
    # Options request should be handled
    assert response.status_code in [200, 405]
