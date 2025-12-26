"""
Tests for Assembly Service.
"""
import pytest
from fastapi.testclient import TestClient
from app.api.assembly_service import app

client = TestClient(app)


def test_assembly_endpoint_success(sample_product):
    """Test assembly endpoint with valid data."""
    response = client.post("/assemble", json=sample_product)
    
    assert response.status_code == 200
    data = response.json()
    assert data["stage"] == "Assembly"
    assert "Test Widget" in data["message"]
    assert "timestamp" in data


def test_assembly_endpoint_validation_error():
    """Test assembly endpoint with invalid data."""
    response = client.post("/assemble", json={"productName": ""})
    
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
