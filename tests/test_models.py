"""
Tests for data models and schemas.
"""
import pytest
from datetime import datetime
from pydantic import ValidationError
from app.models.schemas import ProductRequest, ProcessResponse, HealthCheckResponse


def test_product_request_valid():
    """Test ProductRequest with valid data."""
    product = ProductRequest(productName="Test Product")
    assert product.productName == "Test Product"


def test_product_request_empty_name():
    """Test ProductRequest with empty name fails validation."""
    with pytest.raises(ValidationError):
        ProductRequest(productName="")


def test_product_request_too_long():
    """Test ProductRequest with name too long fails validation."""
    with pytest.raises(ValidationError):
        ProductRequest(productName="x" * 101)


def test_process_response():
    """Test ProcessResponse model."""
    response = ProcessResponse(
        stage="Design",
        message="Design completed"
    )
    assert response.stage == "Design"
    assert response.message == "Design completed"
    assert isinstance(response.timestamp, datetime)


def test_health_check_response():
    """Test HealthCheckResponse model."""
    response = HealthCheckResponse(
        status="healthy",
        service="Test Service",
        version="1.0.0"
    )
    assert response.status == "healthy"
    assert response.service == "Test Service"
    assert response.version == "1.0.0"
