"""
Tests for Packaging Service.
"""
import pytest
from fastapi.testclient import TestClient
from app.api.packaging_service import app

client = TestClient(app)


def test_packaging_endpoint_success(sample_product):
    """Test packaging endpoint with valid data."""
    response = client.post("/package", json=sample_product)
    
    assert response.status_code == 200
    data = response.json()
    assert data["stage"] == "Packaging"
    assert "Test Widget" in data["message"]
    assert "timestamp" in data


def test_packaging_endpoint_validation_error():
    """Test packaging endpoint with invalid data."""
    response = client.post("/package", json={"productName": ""})
    
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
