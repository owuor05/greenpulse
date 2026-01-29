"""
Google Maps Weather API Client
Provides current weather conditions using Google Maps Platform Weather API
https://developers.google.com/maps/documentation/weather
"""
import httpx
from typing import Dict, Any, Optional
from app.config import settings
import logging

logger = logging.getLogger(__name__)


class GoogleWeatherClient:
    """
    Client for Google Maps Platform Weather API
    Requires GOOGLE_MAPS_API_KEY with Weather API enabled
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
        Get current weather conditions for a location using Google Weather API
        
        Args:
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            
        Returns:
            Dict with current weather data including:
            - temperature (°C)
            - feels_like (°C)
            - humidity (%)
            - wind_speed (km/h)
            - conditions (description)
            - uv_index
            - precipitation
        """
        if not self.api_key:
            logger.warning("Google Maps API key not configured")
            return None
        
        try:
            url = f"{self.base_url}/currentConditions:lookup"
            
            params = {
                "location.latitude": latitude,
                "location.longitude": longitude,
                "unitsSystem": "METRIC",
                "key": self.api_key
            }
            
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(url, params=params)
                
                if response.status_code != 200:
                    error_body: str
                    try:
                        error_body = str(response.json())
                    except Exception:
                        error_body = response.text

                    logger.error(
                        "Google Weather API error %s - %s",
                        response.status_code,
                        (error_body[:800] + "...") if len(error_body) > 800 else error_body,
                    )
                    return None
                    
                data = response.json()
                
                # Parse Google Weather API response
                temperature_data = data.get("temperature", {})
                feels_like_data = data.get("feelsLikeTemperature", {})
                wind_data = data.get("wind", {})
                weather_condition = data.get("weatherCondition", {})
                precipitation_data = data.get("precipitation", {})
                
                return {
                    "temperature": temperature_data.get("degrees"),
                    "feels_like": feels_like_data.get("degrees"),
                    "humidity": data.get("relativeHumidity"),
                    "wind_speed": wind_data.get("speed", {}).get("value"),
                    "wind_direction": wind_data.get("direction", {}).get("cardinal"),
                    "conditions": weather_condition.get("description", {}).get("text", ""),
                    "precipitation": precipitation_data.get("qpf", {}).get("quantity", 0),
                    "pressure": data.get("airPressure", {}).get("meanSeaLevelMillibars"),
                    "visibility": data.get("visibility", {}).get("distance"),
                    "uv_index": data.get("uvIndex"),
                    "cloud_cover": data.get("cloudCover"),
                    "dew_point": data.get("dewPoint", {}).get("degrees"),
                    "is_daytime": data.get("isDaytime", True),
                    "timestamp": data.get("currentTime")
                }
        
        except httpx.HTTPStatusError as e:
            logger.error(f"Google Weather API HTTP error: {e.response.status_code} - {e.response.text[:200]}")
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
        Get weather forecast for a location using Google Weather API
        
        Args:
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            days: Number of days to forecast (up to 10)
            
        Returns:
            Dict with forecast data
        """
        if not self.api_key:
            logger.warning("Google Maps API key not configured")
            return None
            
        try:
            url = f"{self.base_url}/dailyForecast:lookup"
            
            params = {
                "location.latitude": latitude,
                "location.longitude": longitude,
                "days": min(days, 10),  # Max 10 days
                "key": self.api_key
            }
            
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(url, params=params)
                response.raise_for_status()
                
                data = response.json()
                
                return {
                    "location": data.get("location"),
                    "forecast_list": data.get("dailyForecasts", [])
                }
        
        except Exception as e:
            logger.error(f"Google Weather forecast API error: {e}")
            return None


# Global instance
google_weather_client = GoogleWeatherClient()
