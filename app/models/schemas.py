"""
Pydantic models for request/response validation.
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ProductRequest(BaseModel):
    """Request model for product processing."""
    productName: str = Field(..., min_length=1, max_length=100, description="Name of the product")
    
    class Config:
        json_schema_extra = {
            "example": {
                "productName": "Widget 3000"
            }
        }


class ProcessResponse(BaseModel):
    """Response model for processing stages."""
    stage: str = Field(..., description="Processing stage name")
    message: str = Field(..., description="Processing result message")
    timestamp: Optional[datetime] = Field(default_factory=datetime.utcnow, description="Processing timestamp")
    
    class Config:
        json_schema_extra = {
            "example": {
                "stage": "Design",
                "message": "Design completed for Widget 3000",
                "timestamp": "2024-01-01T12:00:00"
            }
        }


class HealthCheckResponse(BaseModel):
    """Response model for health check endpoint."""
    status: str = Field(..., description="Service health status")
    service: str = Field(..., description="Service name")
    version: str = Field(..., description="API version")
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "service": "Design Service",
                "version": "1.0.0"
            }
        }


class ErrorResponse(BaseModel):
    """Response model for errors."""
    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information")
    
    class Config:
        json_schema_extra = {
            "example": {
                "error": "ValidationError",
                "message": "Invalid product name",
                "detail": "Product name cannot be empty"
            }
        }
