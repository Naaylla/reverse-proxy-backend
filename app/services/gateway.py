"""
External API client for aggregating data from multiple sources.
This module handles all external API calls and data normalization.
"""
import asyncio
from typing import Dict, Any, Optional
import httpx
from app.core.mappings import (
    ASSET_MAPPING,
    COUNTRY_COORDINATES,
    COINGECKO_API_URL,
    OPEN_METEO_WEATHER_URL,
    OPEN_METEO_AIR_QUALITY_URL,
)
from app.core.exceptions import ExternalAPIError


class ExternalAPIClient:
    """
    Client for making parallel requests to external APIs.
    Implements the aggregation layer of the API gateway pattern.
    """
    
    def __init__(self, timeout: float = 10.0):
        """
        Initialize the external API client.
        
        Args:
            timeout: Maximum time to wait for external API responses (seconds)
        """
        self.timeout = timeout
    
    async def fetch_economy_data(self, asset: str) -> Optional[Dict[str, Any]]:
        """
        Fetch cryptocurrency price from CoinGecko API.
        
        Args:
            asset: Asset code (e.g., 'btc', 'eth', 'sol')
            
        Returns:
            Dictionary with price data or None if request fails
        """
        # Map frontend asset code to CoinGecko ID
        coin_id = ASSET_MAPPING.get(asset.lower())
        if not coin_id:
            return None
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                # Call CoinGecko API to get current price in USD
                response = await client.get(
                    COINGECKO_API_URL,
                    params={
                        "ids": coin_id,
                        "vs_currencies": "usd"
                    }
                )
                response.raise_for_status()
                data = response.json()
                
                # Extract and normalize the price value
                if coin_id in data and "usd" in data[coin_id]:
                    price = data[coin_id]["usd"]
                    return {f"{asset.lower()}_usd": price}
                
                return None
                
        except (httpx.HTTPError, KeyError, ValueError) as e:
            # Log error but don't fail the entire request
            print(f"Economy API error for {asset}: {str(e)}")
            return None
    
    async def fetch_weather_data(self, country: str) -> Optional[Dict[str, Any]]:
        """
        Fetch current weather data from Open-Meteo API.
        
        Args:
            country: Country name (e.g., 'algeria', 'france')
            
        Returns:
            Dictionary with weather data or None if request fails
        """
        # Map country name to coordinates
        coords = COUNTRY_COORDINATES.get(country.lower())
        if not coords:
            return None
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                # Call Open-Meteo weather API with coordinates
                response = await client.get(
                    OPEN_METEO_WEATHER_URL,
                    params={
                        "latitude": coords["latitude"],
                        "longitude": coords["longitude"],
                        "current_weather": "true"
                    }
                )
                response.raise_for_status()
                data = response.json()
                
                # Extract and normalize weather values
                if "current_weather" in data:
                    current = data["current_weather"]
                    return {
                        "temperature": current.get("temperature"),
                        "wind_speed": current.get("windspeed")
                    }
                
                return None
                
        except (httpx.HTTPError, KeyError, ValueError) as e:
            print(f"Weather API error for {country}: {str(e)}")
            return None
    
    async def fetch_air_quality_data(self, country: str) -> Optional[Dict[str, Any]]:
        """
        Fetch air quality data from Open-Meteo Air Quality API.
        
        Args:
            country: Country name (e.g., 'algeria', 'france')
            
        Returns:
            Dictionary with air quality data or None if request fails
        """
        # Map country name to coordinates (reuse same mapping as weather)
        coords = COUNTRY_COORDINATES.get(country.lower())
        if not coords:
            return None
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                # Call Open-Meteo air quality API with coordinates
                response = await client.get(
                    OPEN_METEO_AIR_QUALITY_URL,
                    params={
                        "latitude": coords["latitude"],
                        "longitude": coords["longitude"],
                        "current": "pm10"
                    }
                )
                response.raise_for_status()
                data = response.json()
                
                # Extract and normalize air quality values
                if "current" in data and "pm10" in data["current"]:
                    return {
                        "pm10": data["current"]["pm10"]
                    }
                
                return None
                
        except (httpx.HTTPError, KeyError, ValueError) as e:
            print(f"Air quality API error for {country}: {str(e)}")
            return None
    
    async def aggregate_data(self, request_data: Dict[str, Dict[str, str]]) -> Dict[str, Any]:
        """
        Aggregate data from multiple external APIs in parallel.
        This is the core of the API gateway aggregation pattern.
        
        Args:
            request_data: Dictionary specifying what data to fetch
                Example: {
                    "economy": {"asset": "btc"},
                    "weather": {"country": "algeria"},
                    "air": {"country": "algeria"}
                }
        
        Returns:
            Aggregated response with raw values only
            Example: {
                "economy": {"btc_usd": 68421},
                "weather": {"temperature": 22, "wind_speed": 15.2},
                "air": {"pm10": 45}
            }
        """
        # Build list of async tasks for parallel execution
        tasks = []
        task_keys = []
        
        # Check if economy data is requested
        if "economy" in request_data and "asset" in request_data["economy"]:
            asset = request_data["economy"]["asset"]
            tasks.append(self.fetch_economy_data(asset))
            task_keys.append("economy")
        
        # Check if weather data is requested
        if "weather" in request_data and "country" in request_data["weather"]:
            country = request_data["weather"]["country"]
            tasks.append(self.fetch_weather_data(country))
            task_keys.append("weather")
        
        # Check if air quality data is requested
        if "air" in request_data and "country" in request_data["air"]:
            country = request_data["air"]["country"]
            tasks.append(self.fetch_air_quality_data(country))
            task_keys.append("air")
        
        # Execute all API calls in parallel for optimal performance
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Build aggregated response
        response = {}
        for key, result in zip(task_keys, results):
            if isinstance(result, Exception):
                # Skip failed requests
                continue
            if result is not None:
                response[key] = result
        
        return response
