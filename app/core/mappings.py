"""
Mapping configurations for the API gateway.
Maps frontend identifiers to external API parameters.
"""

# Cryptocurrency asset mapping
# Maps frontend asset codes to CoinGecko API IDs
ASSET_MAPPING = {
    "btc": "bitcoin",
    "eth": "ethereum",
    "sol": "solana",
}

# Country to coordinates mapping
# Maps country names to latitude/longitude for weather and air quality APIs
COUNTRY_COORDINATES = {
    "algeria": {"latitude": 36.75, "longitude": 3.06},
    "usa": {"latitude": 40.71, "longitude": -74.01},  # New York
    "uk": {"latitude": 51.51, "longitude": -0.13},  # London
    "france": {"latitude": 48.86, "longitude": 2.35},  # Paris
    "germany": {"latitude": 52.52, "longitude": 13.40},  # Berlin
    "japan": {"latitude": 35.68, "longitude": 139.65},  # Tokyo
    "china": {"latitude": 39.90, "longitude": 116.40},  # Beijing
    "india": {"latitude": 28.61, "longitude": 77.21},  # New Delhi
    "brazil": {"latitude": -23.55, "longitude": -46.63},  # São Paulo
    "australia": {"latitude": -33.87, "longitude": 151.21},  # Sydney
}

# External API endpoints
COINGECKO_API_URL = "https://api.coingecko.com/api/v3/simple/price"
OPEN_METEO_WEATHER_URL = "https://api.open-meteo.com/v1/forecast"
OPEN_METEO_AIR_QUALITY_URL = "https://air-quality-api.open-meteo.com/v1/air-quality"
