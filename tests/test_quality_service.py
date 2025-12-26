"""
Tests for Quality Service.
"""
import pytest
from fastapi.testclient import TestClient
from app.api.quality_service import app

client = TestClient(app)


def test_quality_endpoint_success(sample_product):
    """Test quality endpoint with valid data."""
    response = client.post("/quality", json=sample_product)
    
    assert response.status_code == 200
    data = response.json()
    assert data["stage"] == "Quality"
    assert "Test Widget" in data["message"]
    assert "timestamp" in data


def test_quality_endpoint_validation_error():
    """Test quality endpoint with invalid data."""
    response = client.post("/quality", json={"productName": ""})
    
    assert response.status_code == 422
    data = response.json()
    assert data["error"] == "ValidationError"


def test_health_check():
    """Test health check endpoint."""
    response = client.get("/health")
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "Assembly Factory"
    assert data["version"] == "1.0.0"
