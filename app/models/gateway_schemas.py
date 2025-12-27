"""
Pydantic models for the API gateway.
Defines request and response schemas for the /api/state endpoint.
"""
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field


class EconomyRequest(BaseModel):
    """Request parameters for economy data."""
    asset: str = Field(..., description="Cryptocurrency asset code (btc, eth, sol)")


class WeatherRequest(BaseModel):
    """Request parameters for weather data."""
    country: str = Field(..., description="Country name")


class AirQualityRequest(BaseModel):
    """Request parameters for air quality data."""
    country: str = Field(..., description="Country name")


class StateRequest(BaseModel):

    economy: Optional[EconomyRequest] = Field(None, description="Economy data request")
    weather: Optional[WeatherRequest] = Field(None, description="Weather data request")
    air: Optional[AirQualityRequest] = Field(None, description="Air quality data request")


class StateResponse(BaseModel):

    economy: Optional[Dict[str, Any]] = Field(None, description="Economy data with raw values")
    weather: Optional[Dict[str, Any]] = Field(None, description="Weather data with raw values")
    air: Optional[Dict[str, Any]] = Field(None, description="Air quality data with raw values")
