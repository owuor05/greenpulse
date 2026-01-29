"""
NASA POWER API Client
Free climate data for any location worldwide
"""
import httpx
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
import logging

logger = logging.getLogger(__name__)


class NASAPowerClient:
    """
    Client for NASA POWER API
    Provides historical and recent climate data
    """
    
    def __init__(self):
        self.base_url = "https://power.larc.nasa.gov/api/temporal"
        self.api_key = "DEMO_KEY"  # No key required for NASA POWER
    
    async def get_daily_data(
        self,
        latitude: float,
        longitude: float,
        parameters: List[str],
        start_date: str,
        end_date: str
    ) -> Optional[Dict[str, Any]]:
        """
        Get daily climate data for a location and date range
        
        Args:
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            parameters: List of parameters (e.g., ['T2M', 'PRECTOTCORR', 'RH2M'])
            start_date: Start date in YYYYMMDD format
            end_date: End date in YYYYMMDD format
            
        Returns:
            Dict with climate data or None if error
        """
        try:
            params_str = ",".join(parameters)
            url = f"{self.base_url}/daily/point"
            
            params = {
                "parameters": params_str,
                "community": "AG",  # Agricultural community
                "longitude": longitude,
                "latitude": latitude,
                "start": start_date,
                "end": end_date,
                "format": "JSON"
            }
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(url, params=params)
                response.raise_for_status()
                
                data = response.json()
                return data.get("properties", {}).get("parameter", {})
        
        except Exception as e:
            logger.error(f"NASA POWER API error: {e}")
            return None
    
    async def get_recent_30_days(
        self,
        latitude: float,
        longitude: float
    ) -> Optional[Dict[str, Any]]:
        """
        Get last 30 days of climate data for drought/flood detection
        
        Args:
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            
        Returns:
            Dict with temperature, precipitation, humidity data
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        
        # Key parameters for climate risk detection
        parameters = [
            "T2M",              # Temperature at 2 meters (C)
            "T2M_MAX",          # Max temperature (C)
            "T2M_MIN",          # Min temperature (C)
            "PRECTOTCORR",      # Precipitation (mm/day)
            "RH2M",             # Relative humidity at 2m (%)
            "WS2M",             # Wind speed at 2m (m/s)
            "ALLSKY_SFC_SW_DWN" # Solar radiation (kWh/m2/day)
        ]
        
        return await self.get_daily_data(
            latitude=latitude,
            longitude=longitude,
            parameters=parameters,
            start_date=start_date.strftime("%Y%m%d"),
            end_date=end_date.strftime("%Y%m%d")
        )
    
    async def get_monthly_averages(
        self,
        latitude: float,
        longitude: float,
        months: int = 12
    ) -> Optional[Dict[str, Any]]:
        """
        Get monthly climate averages for trend analysis
        
        Args:
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            months: Number of months to retrieve (default 12)
            
        Returns:
            Dict with monthly averages
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(days=months * 30)
        
        try:
            params_str = "T2M,PRECTOTCORR,RH2M"
            url = f"{self.base_url}/monthly/point"
            
            params = {
                "parameters": params_str,
                "community": "AG",
                "longitude": longitude,
                "latitude": latitude,
                "start": start_date.strftime("%Y%m"),
                "end": end_date.strftime("%Y%m"),
                "format": "JSON"
            }
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(url, params=params)
                response.raise_for_status()
                
                data = response.json()
                return data.get("properties", {}).get("parameter", {})
        
        except Exception as e:
            logger.error(f"NASA POWER monthly data error: {e}")
            return None
    
    def analyze_drought_risk(self, climate_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze drought risk from NASA POWER data
        
        Args:
            climate_data: Daily climate data from NASA POWER
            
        Returns:
            Dict with drought risk assessment
        """
        if not climate_data:
            return {"risk": "unknown", "severity": "low"}
        
        # Extract precipitation and temperature data
        precip_data = climate_data.get("PRECTOTCORR", {})
        temp_data = climate_data.get("T2M_MAX", {})
        
        if not precip_data or not temp_data:
            return {"risk": "unknown", "severity": "low"}
        
        # Calculate metrics
        precip_values = [float(v) for v in precip_data.values() if v != -999]
        temp_values = [float(v) for v in temp_data.values() if v != -999]
        
        if not precip_values or not temp_values:
            return {"risk": "unknown", "severity": "low"}
        
        avg_precip = sum(precip_values) / len(precip_values)
        avg_temp = sum(temp_values) / len(temp_values)
        days_no_rain = sum(1 for v in precip_values if v < 1.0)
        
        # Drought criteria
        severity = "low"
        risk_detected = False
        
        if avg_precip < 2.0 and days_no_rain > 20:
            severity = "critical"
            risk_detected = True
        elif avg_precip < 3.0 and days_no_rain > 15:
            severity = "high"
            risk_detected = True
        elif avg_precip < 5.0 and days_no_rain > 10:
            severity = "moderate"
            risk_detected = True
        
        return {
            "risk": "drought" if risk_detected else "none",
            "severity": severity,
            "avg_precipitation_mm": round(avg_precip, 2),
            "avg_max_temperature_c": round(avg_temp, 2),
            "days_without_rain": days_no_rain,
            "total_days_analyzed": len(precip_values)
        }
    
    def analyze_flood_risk(self, climate_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze flood risk from NASA POWER data
        
        Args:
            climate_data: Daily climate data from NASA POWER
            
        Returns:
            Dict with flood risk assessment
        """
        if not climate_data:
            return {"risk": "unknown", "severity": "low"}
        
        precip_data = climate_data.get("PRECTOTCORR", {})
        
        if not precip_data:
            return {"risk": "unknown", "severity": "low"}
        
        precip_values = [float(v) for v in precip_data.values() if v != -999]
        
        if not precip_values:
            return {"risk": "unknown", "severity": "low"}
        
        # Calculate metrics
        total_precip = sum(precip_values)
        max_daily_precip = max(precip_values)
        avg_precip = total_precip / len(precip_values)
        heavy_rain_days = sum(1 for v in precip_values if v > 20.0)
        
        # Flood criteria
        severity = "low"
        risk_detected = False
        
        if max_daily_precip > 100 or heavy_rain_days > 5:
            severity = "critical"
            risk_detected = True
        elif max_daily_precip > 50 or heavy_rain_days > 3:
            severity = "high"
            risk_detected = True
        elif max_daily_precip > 30 or total_precip > 150:
            severity = "moderate"
            risk_detected = True
        
        return {
            "risk": "flood" if risk_detected else "none",
            "severity": severity,
            "total_precipitation_mm": round(total_precip, 2),
            "max_daily_precipitation_mm": round(max_daily_precip, 2),
            "avg_precipitation_mm": round(avg_precip, 2),
            "heavy_rain_days": heavy_rain_days,
            "total_days_analyzed": len(precip_values)
        }


# Global NASA POWER client instance
nasa_client = NASAPowerClient()
