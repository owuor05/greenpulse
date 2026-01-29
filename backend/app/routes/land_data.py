"""
Land Data Analysis Endpoint
Provides comprehensive land and climate data for any location in Kenya
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
from app.services.database import db_service
from app.services.google_maps_service import gmaps_service
from app.services.climate_risk_service import climate_service
from app.data.nasa_power import nasa_client
from app.data.google_weather import google_weather_client
from app.services.ai_service import ai_service
import logging
from datetime import datetime, timezone

router = APIRouter(prefix="/api/land-data", tags=["land-data"])
logger = logging.getLogger(__name__)


class LandDataRequest(BaseModel):
    """Request model for land data analysis"""
    location: str


@router.post("/analyze")
async def analyze_land_data(request: LandDataRequest):
    """
    Analyze comprehensive land and climate data for a location
    
    Features:
    - Current temperature and weather
    - Climate risk assessment (drought/flood)
    - Historical climate data
    - Active alerts
    - AI-generated summary (2 sentences)
    - 24-hour caching for performance
    
    Args:
        location: Location name (e.g., "Kitui", "Nairobi", "Weuye")
        
    Returns:
        Comprehensive land data with AI summary
    """
    try:
        location_name = request.location.strip()

        # NOTE: Caching disabled to keep results fully dynamic.

        # Step 1: Geocode location
        logger.info(f"Fetching fresh data for {location_name}")
        
        location_data = await gmaps_service.geocode_address(location_name)
        
        if not location_data:
            raise HTTPException(
                status_code=404,
                detail=f"Could not find location: {location_name}"
            )
        
        latitude = location_data['latitude']
        longitude = location_data['longitude']
        
        # Step 3: Fetch climate data (NASA POWER - last 30 days)
        climate_data = await nasa_client.get_recent_30_days(latitude, longitude)
        
        if not climate_data:
            raise HTTPException(
                status_code=500,
                detail="Could not fetch climate data from NASA POWER"
            )
        
        # Step 4: Analyze risks
        drought_analysis = nasa_client.analyze_drought_risk(climate_data)
        flood_analysis = nasa_client.analyze_flood_risk(climate_data)
        
        # Step 5: Build active alerts based on risk severity (HIGH or CRITICAL)
        active_alerts = []
        
        if drought_analysis['severity'].lower() in ['high', 'critical']:
            active_alerts.append({
                'risk_type': 'drought',
                'severity': drought_analysis['severity'],
                'description': f"DROUGHT ALERT: {drought_analysis['days_without_rain']} days without adequate rainfall. Average precipitation is only {drought_analysis['avg_precipitation_mm']:.2f}mm/day, well below the critical threshold of 2mm/day."
            })
        
        if flood_analysis['severity'].lower() in ['high', 'critical']:
            active_alerts.append({
                'risk_type': 'flood',
                'severity': flood_analysis['severity'],
                'description': f"FLOOD ALERT: Heavy rainfall detected with {flood_analysis['max_daily_precipitation_mm']:.1f}mm maximum daily rainfall. {flood_analysis['heavy_rain_days']} days with heavy rain in the analysis period."
            })
        
        # Also fetch any stored alerts from database
        db_alerts = await db_service.get_active_alerts(location_name)
        active_alerts.extend(db_alerts)
        
        # Step 6: Get current temperature from Google Weather API (temperature ONLY source)
        weather_data = await google_weather_client.get_current_weather(latitude, longitude)
        if weather_data and weather_data.get('temperature') is not None:
            current_temp = weather_data['temperature']
            feels_like = weather_data.get('feels_like', current_temp)
            weather_ok = True
        else:
            current_temp = None
            feels_like = None
            weather_ok = False

        current_temp_display = f"{current_temp:.1f}°C" if current_temp is not None else "N/A"
        feels_like_display = f"{feels_like:.1f}°C" if feels_like is not None else "N/A"
        
        # Step 7: Generate concise AI summary (2 paragraphs max, 100-150 words for speed)
        ai_prompt = f"""Analyze environmental conditions for {location_name}, Kenya.

**Current Data:**
- Temperature: {current_temp_display} (feels like {feels_like_display})
- Drought Risk: {drought_analysis.get('severity', 'none').upper()} ({drought_analysis.get('days_without_rain', 0)} days without rain, avg {drought_analysis.get('avg_precipitation_mm', 0):.2f}mm/day)
- Flood Risk: {flood_analysis.get('severity', 'none').upper()} ({flood_analysis.get('max_daily_precipitation_mm', 0):.1f}mm max daily rainfall)
- Active Alerts: {len(active_alerts)}

**Write exactly 2 paragraphs (100-150 words total):**

PARAGRAPH 1 - Environmental Assessment:
Summarize current environmental conditions in {location_name}. State the climate risk level, what it means for land stability, water resources, and ecosystems. Be specific and data-driven.

PARAGRAPH 2 - Decision Recommendations:
Provide 3-4 key recommendations for decision-makers (governments, businesses, or landowners). Focus on risk mitigation, compliance considerations, and actionable next steps.

**Requirements:**
- Maximum 150 words total
- Professional tone for decision-makers
- No emojis
- Be specific to {location_name}"""

        system_prompt = """You are GreenPulse AI - an environmental intelligence system for Kenya. 
Provide concise, professional environmental assessments for decision-makers.
Be data-driven, specific, and actionable. Maximum 150 words."""

        ai_summary_response = await ai_service.chat_response_with_system(
            user_message=ai_prompt,
            system_prompt=system_prompt
        )
        
        ai_summary = ai_summary_response if ai_summary_response else 'Climate data analysis in progress for this location.'
        
        # Step 8: Build comprehensive response
        land_data = {
            "location_name": location_name,
            "latitude": latitude,
            "longitude": longitude,
            "current_temperature_celsius": round(current_temp, 1) if current_temp is not None else None,
            "feels_like_celsius": round(feels_like, 1) if feels_like is not None else None,
            "temperature_status": "ok" if weather_ok else "unavailable",
            "climate_risks": {
                "drought": drought_analysis,
                "flood": flood_analysis
            },
            "active_alerts": active_alerts,
            "historical_data": {
                "period": "Last 30 days",
                "avg_precipitation_mm": drought_analysis.get('avg_precipitation_mm'),
                "total_precipitation_mm": flood_analysis.get('total_precipitation_mm')
            },
            "ai_summary": ai_summary,
            "data_source": {
                "temperature": "Google Maps Weather API (Real-time)",
                "climate_analysis": "NASA POWER (30-day trends)"
            },
            "analyzed_at": datetime.now(timezone.utc).isoformat()
        }
        
        logger.info(f"✅ Successfully analyzed data for {location_name}")
        
        return {
            "success": True,
            "location": location_name,
            "data": land_data,
            "cached": False
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error analyzing land data: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def land_data_health():
    """Health check for land data service"""
    return {
        "status": "healthy",
        "service": "Land Data Analysis",
        "features": [
            "Temperature data",
            "Climate risk assessment",
            "Active alerts",
            "AI summaries",
            "24-hour caching"
        ]
    }
