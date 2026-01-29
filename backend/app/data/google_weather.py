"""
Google Maps Weather API Client
Provides current weather and forecast data
"""
import httpx
from typing import Dict, Any, Optional
from app.config import settings
import logging

logger = logging.getLogger(__name__)


class GoogleWeatherClient:
    """
    Client for Google Maps Platform Weather API
    """
    
    def __init__(self):
        self.api_key = settings.GOOGLE_MAPS_API_KEY
        self.base_url = "https://weather.googleapis.com/v1"
    
    async def get_current_weather(
        self,
        latitude: float,
        longitude: float
    ) -> Optional[Dict[str, Any]]:
        """
        Get current weather conditions for a location
        
        Args:
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            
        Returns:
            Dict with current weather data including:
            - temperature (current, feels_like, min, max)
            - humidity
            - wind speed
            - conditions
            - precipitation
        """
        try:
            url = f"{self.base_url}/current"
            
            params = {
                "location": f"{latitude},{longitude}",
                "key": self.api_key
            }
            
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(url, params=params)
                response.raise_for_status()
                
                data = response.json()
                
                # Parse Google Weather API response
                return {
                    "temperature": data.get("temperature", {}).get("value"),
                    "feels_like": data.get("temperature", {}).get("feelsLike"),
                    "humidity": data.get("humidity", {}).get("value"),
                    "wind_speed": data.get("wind", {}).get("speed"),
                    "wind_direction": data.get("wind", {}).get("direction"),
                    "conditions": data.get("condition", {}).get("description"),
                    "precipitation": data.get("precipitation", {}).get("value"),
                    "pressure": data.get("pressure", {}).get("value"),
                    "visibility": data.get("visibility", {}).get("value"),
                    "uv_index": data.get("uvIndex", {}).get("value"),
                    "timestamp": data.get("observationTime")
                }
        
        except httpx.HTTPStatusError as e:
            logger.error(f"Google Weather API HTTP error: {e.response.status_code} - {e.response.text}")
            return None
        except Exception as e:
            logger.error(f"Google Weather API error: {e}")
            return None
    
    async def get_forecast(
        self,
        latitude: float,
        longitude: float,
        days: int = 7
    ) -> Optional[Dict[str, Any]]:
        """
        Get weather forecast for a location
        
        Args:
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            days: Number of days to forecast (default 7)
            
        Returns:
            Dict with forecast data
        """
        try:
            url = f"{self.base_url}/forecast"
            
            params = {
                "location": f"{latitude},{longitude}",
                "days": days,
                "key": self.api_key
            }
            
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(url, params=params)
                response.raise_for_status()
                
                data = response.json()
                return data.get("forecast", {})
        
        except Exception as e:
            logger.error(f"Google Weather API forecast error: {e}")
            return None


# Global instance
google_weather_client = GoogleWeatherClient()
