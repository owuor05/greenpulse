"""
Google Maps service for geocoding and location data
"""
import googlemaps
from app.config import settings
from typing import Optional, Dict, Any, Tuple
import logging

logger = logging.getLogger(__name__)


class GoogleMapsService:
    """
    Service for Google Maps API interactions
    """
    
    def __init__(self):
        self.client = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)
    
    async def geocode_address(self, address: str) -> Optional[Dict[str, Any]]:
        """
        Convert address/location name to coordinates
        
        Args:
            address: Location name or address
            
        Returns:
            Dict with lat, lng, formatted_address, region
        """
        try:
            result = self.client.geocode(address)
            
            if not result:
                return None
            
            location = result[0]
            geometry = location['geometry']['location']
            
            # Extract region/county from address components
            region = None
            for component in location.get('address_components', []):
                if 'administrative_area_level_1' in component['types']:
                    region = component['long_name']
                    break
                elif 'locality' in component['types']:
                    region = component['long_name']
            
            return {
                'latitude': geometry['lat'],
                'longitude': geometry['lng'],
                'formatted_address': location['formatted_address'],
                'region': region or address
            }
        except Exception as e:
            logger.error(f"Geocoding error for '{address}': {e}")
            return None
    
    async def reverse_geocode(self, latitude: float, longitude: float) -> Optional[Dict[str, Any]]:
        """
        Convert coordinates to address and region
        
        Args:
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            
        Returns:
            Dict with formatted_address, region, country
        """
        try:
            result = self.client.reverse_geocode((latitude, longitude))
            
            if not result:
                return None
            
            location = result[0]
            
            # Extract region/county
            region = None
            country = None
            for component in location.get('address_components', []):
                if 'administrative_area_level_1' in component['types']:
                    region = component['long_name']
                elif 'country' in component['types']:
                    country = component['long_name']
            
            return {
                'formatted_address': location['formatted_address'],
                'region': region,
                'country': country
            }
        except Exception as e:
            logger.error(f"Reverse geocoding error for ({latitude}, {longitude}): {e}")
            return None
    
    async def get_elevation(self, latitude: float, longitude: float) -> Optional[float]:
        """
        Get elevation for coordinates
        
        Args:
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            
        Returns:
            Elevation in meters
        """
        try:
            result = self.client.elevation((latitude, longitude))
            
            if result:
                return result[0]['elevation']
            return None
        except Exception as e:
            logger.error(f"Elevation error for ({latitude}, {longitude}): {e}")
            return None
    
    async def get_timezone(self, latitude: float, longitude: float) -> Optional[str]:
        """
        Get timezone for coordinates
        
        Args:
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            
        Returns:
            Timezone ID (e.g., 'Africa/Nairobi')
        """
        try:
            from datetime import datetime, timezone
            result = self.client.timezone((latitude, longitude), timestamp=datetime.now(timezone.utc))
            
            if result:
                return result['timeZoneId']
            return None
        except Exception as e:
            logger.error(f"Timezone error for ({latitude}, {longitude}): {e}")
            return None
    
    async def validate_kenyan_location(self, address: str) -> Tuple[bool, Optional[Dict[str, Any]]]:
        """
        Validate if location is in Kenya and return geocoded data
        
        Args:
            address: Location name to validate
            
        Returns:
            Tuple of (is_valid, location_data)
        """
        location_data = await self.geocode_address(address)
        
        if not location_data:
            return False, None
        
        # Check if in Kenya using reverse geocode
        reverse_data = await self.reverse_geocode(
            location_data['latitude'],
            location_data['longitude']
        )
        
        if reverse_data and reverse_data.get('country') == 'Kenya':
            return True, location_data
        
        return False, location_data


# Global Google Maps service instance
gmaps_service = GoogleMapsService()
