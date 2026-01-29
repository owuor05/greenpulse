"""
API Router for Climate Risk endpoints
"""
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Optional, List
from app.services.climate_risk_service import climate_service
from app.services.google_maps_service import gmaps_service
from app.services.database import db_service

router = APIRouter(prefix="/api", tags=["climate"])


class LocationRequest(BaseModel):
    """Request model for location-based queries"""
    region: str = Field(..., description="Region name (e.g., 'Nairobi', 'Mombasa')")


class CoordinatesRequest(BaseModel):
    """Request model for coordinate-based queries"""
    latitude: float = Field(..., ge=-90, le=90, description="Latitude coordinate")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude coordinate")


class SubscriptionRequest(BaseModel):
    """Request model for alert subscriptions"""
    phone_number: Optional[str] = None
    telegram_id: Optional[int] = None
    region: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Terraguard Climate API",
        "version": "1.0.0"
    }


@router.post("/risk/detect")
async def detect_climate_risks(request: LocationRequest):
    """
    Detect climate risks for a specific region
    
    Analyzes last 30 days of climate data and identifies:
    - Drought conditions
    - Flood risks
    - Temperature extremes
    """
    try:
        risks = await climate_service.detect_risks_for_region(request.region)
        
        return {
            "success": True,
            "region": request.region,
            "risks_detected": len(risks),
            "risks": risks
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/risk/forecast")
async def get_risk_forecast(request: LocationRequest):
    """
    Get current risk status and forecast for a region
    
    Returns:
    - Current risk levels (drought, flood)
    - Active alerts
    - Climate data summary
    """
    try:
        forecast = await climate_service.get_risk_forecast(request.region)
        
        if 'error' in forecast:
            raise HTTPException(status_code=404, detail=forecast['error'])
        
        return {
            "success": True,
            "data": forecast
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/risk/analyze-coordinates")
async def analyze_coordinates(request: CoordinatesRequest):
    """
    Analyze climate risks for specific GPS coordinates
    
    Useful for mobile apps with GPS location
    """
    try:
        analysis = await climate_service.analyze_location_coordinates(
            request.latitude,
            request.longitude
        )
        
        if 'error' in analysis:
            raise HTTPException(status_code=404, detail=analysis['error'])
        
        return {
            "success": True,
            "data": analysis
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/alerts")
async def get_active_alerts(
    region: Optional[str] = Query(None, description="Filter by region")
):
    """
    Get all active climate alerts
    
    Optional region filter to get alerts for specific area
    """
    try:
        alerts = await db_service.get_active_alerts(region)
        
        return {
            "success": True,
            "count": len(alerts),
            "alerts": alerts
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/alerts/{alert_id}")
async def get_alert_details(alert_id: str):
    """
    Get detailed information about a specific alert
    """
    try:
        alert = await db_service.get_alert_by_id(alert_id)
        
        if not alert:
            raise HTTPException(status_code=404, detail="Alert not found")
        
        return {
            "success": True,
            "alert": alert
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/subscribe")
async def subscribe_to_alerts(request: SubscriptionRequest):
    """
    Subscribe to climate alerts for a region
    
    Supports both SMS (phone_number) and Telegram (telegram_id)
    """
    try:
        # Validate that at least one contact method is provided
        if not request.phone_number and not request.telegram_id:
            raise HTTPException(
                status_code=400,
                detail="Either phone_number or telegram_id must be provided"
            )
        
        # Check if user already exists
        user = None
        if request.phone_number:
            user = await db_service.get_user_by_phone(request.phone_number)
        elif request.telegram_id:
            user = await db_service.get_user_by_telegram_id(request.telegram_id)
        
        if user:
            # Update existing user
            await db_service.update_user_location(
                user['id'],
                request.latitude or user.get('latitude'),
                request.longitude or user.get('longitude'),
                request.region
            )
            
            return {
                "success": True,
                "message": "Subscription updated",
                "user_id": user['id']
            }
        else:
            # Create new user
            user_data = {
                "phone_number": request.phone_number,
                "telegram_id": request.telegram_id,
                "region": request.region,
                "latitude": request.latitude,
                "longitude": request.longitude,
                "subscribed": True
            }
            
            new_user = await db_service.create_user(user_data)
            
            if not new_user:
                raise HTTPException(status_code=500, detail="Failed to create subscription")
            
            return {
                "success": True,
                "message": "Subscribed to climate alerts",
                "user_id": new_user['id']
            }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/regions")
async def get_regions():
    """
    Get list of supported regions in Kenya
    """
    try:
        # For now, return hardcoded list
        # TODO: Fetch from database regions table
        regions = [
            {"name": "Nairobi", "climate_zone": "Temperate"},
            {"name": "Mombasa", "climate_zone": "Tropical"},
            {"name": "Kisumu", "climate_zone": "Tropical"},
            {"name": "Nakuru", "climate_zone": "Temperate"},
            {"name": "Eldoret", "climate_zone": "Temperate"},
            {"name": "Thika", "climate_zone": "Temperate"},
            {"name": "Malindi", "climate_zone": "Tropical"},
            {"name": "Kitale", "climate_zone": "Temperate"},
            {"name": "Garissa", "climate_zone": "Arid"},
            {"name": "Kakamega", "climate_zone": "Tropical"},
            {"name": "Meru", "climate_zone": "Temperate"},
            {"name": "Nyeri", "climate_zone": "Temperate"},
            {"name": "Machakos", "climate_zone": "Semi-Arid"},
            {"name": "Kisii", "climate_zone": "Tropical"},
            {"name": "Embu", "climate_zone": "Temperate"},
        ]
        
        return {
            "success": True,
            "count": len(regions),
            "regions": regions
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/geocode")
async def geocode_location(request: LocationRequest):
    """
    Convert location name to coordinates
    
    Useful for validating user input and getting GPS coordinates
    """
    try:
        location = await gmaps_service.geocode_address(request.region)
        
        if not location:
            raise HTTPException(status_code=404, detail="Location not found")
        
        return {
            "success": True,
            "location": location
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
