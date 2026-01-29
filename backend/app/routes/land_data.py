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
        
        # Step 1: Check cache first (24-hour expiry)
        cached_data = await db_service.get_cached_land_data(location_name)
        
        if cached_data:
            logger.info(f"Returning cached data for {location_name}")
            return {
                "success": True,
                "location": location_name,
                "data": cached_data,
                "cached": True,
                "cache_age_hours": (
                    datetime.now(timezone.utc)
                    - datetime.fromisoformat(
                        cached_data['created_at'].replace('Z', '+00:00')
                    )
                ).total_seconds() / 3600
            }
        
        # Step 2: Geocode location
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
        
        # Step 6: Calculate current temperature (average of last 7 days)
        temp_data = climate_data.get("T2M", {})
        if temp_data:
            recent_temps = list(temp_data.values())[-7:]  # Last 7 days
            current_temp = sum(float(t) for t in recent_temps if t != -999) / len(recent_temps)
        else:
            current_temp = None
        
        # Step 7: Generate comprehensive AI summary focusing on land degradation and conservation
        ai_prompt = f"""You are an environmental and climate conservation expert analyzing conditions for {location_name}, Kenya. 
Your focus is on understanding land degradation, soil health, vegetation cover, and local conservation strategies 
that support both communities and ecosystems.

Location: {location_name}, Kenya
Coordinates: {latitude}, {longitude}

Current Climate Data (Last 30 days):
- Average Temperature: {current_temp:.1f}°C
- Drought Risk: {drought_analysis.get('severity', 'none').upper()} - {drought_analysis.get('days_without_rain', 0)} days without rain, avg {drought_analysis.get('avg_precipitation_mm', 0):.2f}mm/day
- Flood Risk: {flood_analysis.get('severity', 'none').upper()} - {flood_analysis.get('max_daily_precipitation_mm', 0):.1f}mm max rainfall, {flood_analysis.get('heavy_rain_days', 0)} heavy rain days
- Active Alerts: {len(active_alerts)}

Task:
Write a comprehensive 300-500 word analysis in exactly 4 paragraphs:

PARAGRAPH 1 (Climate and Land Condition Overview):
Provide a detailed overview of {location_name}'s climate and land condition over the past decade. 
Discuss rainfall patterns, drought and flood frequency, vegetation loss, soil erosion, and other signs of land degradation. 
Mention any known conservation efforts or local environmental challenges. Be comprehensive and informative (4-6 sentences).

PARAGRAPH 2 (Current Situation Analysis):
Analyze the current data above to explain what the situation means for soil stability, vegetation, 
and water availability. Identify potential risks to farming, grazing, and local livelihoods, and describe their 
short-term implications. Be specific about severity and impact (4-5 sentences).

PARAGRAPH 3 (Land Rehabilitation and Conservation Actions):
Provide exactly 5 practical, region-appropriate actions that local communities or farmers can take to conserve 
and rehabilitate land in {location_name}. Mix short-term actions (e.g., mulching, contour farming) with 
long-term strategies (e.g., agroforestry, afforestation, sustainable grazing). Format as numbered list with 
detailed explanations for each action (5 items, each 2-3 sentences).

PARAGRAPH 4 (Specific Climate Risk Mitigation):
{"Provide exactly 5 actionable drought mitigation measures tailored to {location_name}. Focus on water conservation, soil moisture retention, drought-resistant crops and trees, and community water harvesting. Format as numbered list with practical details (5 items, each 2-3 sentences)." if drought_analysis['severity'].lower() in ['high', 'critical'] else ""}
{"Provide exactly 5 actionable flood preparedness measures tailored to {location_name}. Focus on soil protection from erosion, water drainage systems, contour farming, terracing, and vegetation barriers. Format as numbered list with practical details (5 items, each 2-3 sentences)." if flood_analysis['severity'].lower() in ['high', 'critical'] else ""}
{"Provide guidance on maintaining soil health and preventing land degradation in {location_name} under normal conditions. Include crop rotation, organic farming, tree integration, and community conservation practices. Format as 5 numbered items with details (5 items, each 2-3 sentences)." if drought_analysis['severity'].lower() not in ['high', 'critical'] and flood_analysis['severity'].lower() not in ['high', 'critical'] else ""}

CRITICAL REQUIREMENTS:
- Total length: 400-500 words across all 4 paragraphs
- Use clear, informative paragraphs and numbered lists
- NO emojis whatsoever
- Focus on land health, conservation, and rehabilitation practices
- Be region-specific, practical, and educational
- Include specific tree species, crops, and techniques appropriate for {location_name}
- Use African environmental wisdom and Swahili phrases where appropriate
- Emphasize community-based conservation and collective action"""

        system_prompt = """You are Terraguard's Lead Environmental Conservation Expert specializing in land degradation, 
soil rehabilitation, and community-based conservation across Kenya and East Africa. 

Your expertise includes:
- Land degradation assessment and rehabilitation strategies
- Soil conservation and erosion control techniques
- Agroforestry and reforestation for different ecological zones
- Climate-smart agriculture and sustainable land management
- Community mobilization for environmental conservation
- Indigenous and modern conservation practices
- Region-specific tree species and crop recommendations

Provide comprehensive, detailed analysis (400-500 words) that educates and empowers communities to protect 
and rehabilitate their land. Be thorough, practical, and inspiring. No emojis. Mix English and Swahili naturally 
when using environmental wisdom phrases."""

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
            "current_temperature_celsius": round(current_temp, 1) if current_temp else None,
            "climate_risks": {
                "drought": drought_analysis,
                "flood": flood_analysis
            },
            "active_alerts": active_alerts,
            "historical_data": {
                "period": "Last 30 days",
                "avg_precipitation_mm": drought_analysis.get('avg_precipitation_mm'),
                "avg_max_temperature_c": drought_analysis.get('avg_max_temperature_c'),
                "total_precipitation_mm": flood_analysis.get('total_precipitation_mm')
            },
            "ai_summary": ai_summary,
            "data_source": "NASA POWER",
            "analyzed_at": datetime.now(timezone.utc).isoformat()
        }
        
        # Step 9: Save to cache (24-hour expiry)
        await db_service.save_land_data_cache({
            "location_name": location_name,
            "latitude": latitude,
            "longitude": longitude,
            "temperature_data": {"current_celsius": current_temp},
            "climate_risks": {
                "drought": drought_analysis,
                "flood": flood_analysis
            },
            "active_alerts": active_alerts,
            "historical_data": land_data["historical_data"],
            "ai_summary": ai_summary
        })
        
        logger.info(f"✅ Successfully analyzed and cached data for {location_name}")
        
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
