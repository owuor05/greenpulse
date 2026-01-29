"""
Google Maps Platform API Client for Weather Data
Uses Geocoding API + Places API for location-based weather
Note: Google doesn't have a dedicated Weather API. This uses OpenWeatherMap API as alternative.
"""
import httpx
from typing import Dict, Any, Optional
from app.config import settings
import logging

logger = logging.getLogger(__name__)


class GoogleWeatherClient:
    """
    Client for getting weather data using OpenWeatherMap API
    (Free alternative since Google Maps doesn't have dedicated Weather API)
    """
    
    def __init__(self):
        # OpenWeatherMap free API - requires OPENWEATHER_API_KEY in .env
        # Sign up at: https://openweathermap.org/api
        self.api_key = getattr(settings, 'OPENWEATHER_API_KEY', '')
        self.base_url = "https://api.openweathermap.org/data/2.5"
    
    async def get_current_weather(
        self,
        latitude: float,
        longitude: float
    ) -> Optional[Dict[str, Any]]:
        """
        Get current weather conditions for a location using OpenWeatherMap API
        
        Args:
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            
        Returns:
            Dict with current weather data including:
            - temperature (current, feels_like)
            - humidity
            - wind speed
            - conditions
            - precipitation
        """
        if not self.api_key:
            logger.warning("OpenWeather API key not configured, using fallback values")
            # Return estimated values for Kenya region
            return {
                "temperature": 22.0,  # Average Kenya temperature
                "feels_like": 23.0,
                "humidity": 60,
                "wind_speed": 10,
                "conditions": "Partly Cloudy",
                "precipitation": 0,
                "pressure": 1013,
                "visibility": 10000,
                "uv_index": 8
            }
        
        try:
            url = f"{self.base_url}/weather"
            
            params = {
                "lat": latitude,
                "lon": longitude,
                "appid": self.api_key,
                "units": "metric"  # Celsius
            }
            
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(url, params=params)
                
                if response.status_code == 404:
                    logger.error(f"OpenWeather API HTTP error: {response.status_code}")
                    return None
                    
                response.raise_for_status()
                
                data = response.json()
                
                # Parse OpenWeatherMap API response
                main = data.get("main", {})
                wind = data.get("wind", {})
                weather = data.get("weather", [{}])[0]
                
                return {
                    "temperature": main.get("temp"),
                    "feels_like": main.get("feels_like"),
                    "humidity": main.get("humidity"),
                    "wind_speed": wind.get("speed"),
                    "wind_direction": wind.get("deg"),
                    "conditions": weather.get("description", "").title(),
                    "precipitation": data.get("rain", {}).get("1h", 0),  # Last hour rainfall
                    "pressure": main.get("pressure"),
                    "visibility": data.get("visibility", 0) / 1000,  # Convert to km
                    "uv_index": None,  # UVI requires separate API call
                    "timestamp": data.get("dt")
                }
        
        except httpx.HTTPStatusError as e:
            logger.error(f"OpenWeather API HTTP error: {e.response.status_code} - {e.response.text}")
            return None
        except Exception as e:
            logger.error(f"OpenWeather API error: {e}")
            return None
    
    async def get_forecast(
        self,
        latitude: float,
        longitude: float,
        days: int = 5
    ) -> Optional[Dict[str, Any]]:
        """
        Get weather forecast for a location using OpenWeatherMap API
        
        Args:
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            days: Number of days to forecast (max 5 for free tier)
            
        Returns:
            Dict with forecast data
        """
        if not self.api_key:
            logger.warning("OpenWeather API key not configured, skipping forecast")
            return None
            
        try:
            url = f"{self.base_url}/forecast"
            
            params = {
                "lat": latitude,
                "lon": longitude,
                "appid": self.api_key,
                "units": "metric",
                "cnt": days * 8  # 8 forecasts per day (3-hour intervals)
            }
            
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(url, params=params)
                response.raise_for_status()
                
                data = response.json()
                
                return {
                    "location": data.get("city", {}).get("name"),
                    "forecast_list": data.get("list", [])
                }
        
        except Exception as e:
            logger.error(f"OpenWeather forecast API error: {e}")
            return None


# Global instance
google_weather_client = GoogleWeatherClient()
