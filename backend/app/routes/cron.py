"""
Cron/Scheduled Task Endpoints
These endpoints should be called by external cron services (Render Cron Jobs, cron-job.org, etc.)
"""
from fastapi import APIRouter, HTTPException, Header
from app.services.database import db_service
from app.services.climate_risk_service import climate_service
from app.config import settings
import logging
import time
from datetime import datetime
from typing import Optional
import os

router = APIRouter(prefix="/api/cron", tags=["cron"])
logger = logging.getLogger(__name__)

# Get secret from environment variable
CRON_SECRET = os.getenv("CRON_SECRET", "default-secret-key")


@router.post("/check-alerts")
async def check_alerts_for_all_regions(
    authorization: Optional[str] = Header(None)
):
    """
    Check for climate risks across all subscribed regions and create alerts
    
    This endpoint should be called daily by an external cron service.
    Requires Authorization header with secret key.
    
    Example: curl -X POST https://your-api.com/api/cron/check-alerts \
             -H "Authorization: Bearer your-secret-cron-key-here"
    """
    # Validate authorization
    if not authorization or authorization != f"Bearer {CRON_SECRET}":
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    try:
        logger.info("=== Starting daily alert check ===")
        
        # Get all unique regions from subscribed users
        regions = await db_service.get_all_subscribed_regions()
        
        if not regions:
            logger.info("No subscribed regions found")
            return {
                "success": True,
                "message": "No regions to check",
                "regions_checked": 0,
                "alerts_created": 0
            }
        
        logger.info(f"Checking {len(regions)} regions for risks")
        
        alerts_created = 0
        
        # Check each region for risks
        for region in regions:
            try:
                logger.info(f"Checking region: {region}")
                
                # This will detect risks and automatically create alerts
                risks = await climate_service.detect_risks_for_region(region)
                
                if risks:
                    alerts_created += len(risks)
                    logger.info(f"Created {len(risks)} alert(s) for {region}")
                else:
                    logger.info(f"No risks detected for {region}")
                    
            except Exception as e:
                logger.error(f"Error checking region {region}: {e}")
                continue
        
        logger.info(f"=== Daily alert check complete: {alerts_created} alerts created ===")
        
        return {
            "success": True,
            "message": "Alert check completed",
            "regions_checked": len(regions),
            "alerts_created": alerts_created,
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
    except Exception as e:
        logger.error(f"Error in daily alert check: {e}")
        # Return error with status instead of raising an exception
        # This prevents Render's cron job from failing
        return {
            "success": False,
            "error": str(e),
            "message": "Error in daily alert check",
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }


@router.get("/test-alert-detection")
async def test_alert_detection(
    region: str = "Nairobi"
):
    """
    Test endpoint to manually trigger alert detection for a specific region
    
    Use this to test if the alert system is working without waiting for cron.
    Example: /api/cron/test-alert-detection?region=Kitui
    """
    try:
        logger.info(f"=== Testing alert detection for {region} ===")
        
        risks = await climate_service.detect_risks_for_region(region)
        
        return {
            "success": True,
            "region": region,
            "risks_detected": len(risks),
            "risks": risks,
            "message": f"Found {len(risks)} risk(s) for {region}"
        }
        
    except Exception as e:
        logger.error(f"Error testing alert detection: {e}")
        # Return error with status instead of raising an exception
        return {
            "success": False,
            "error": str(e),
            "message": "Error testing alert detection",
            "region": region,
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
