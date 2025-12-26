"""
Test configuration and fixtures.
"""
import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def sample_product():
    """Sample product data for testing."""
    return {"productName": "Test Widget"}


@pytest.fixture
def invalid_product():
    """Invalid product data for testing."""
    return {"productName": ""}
