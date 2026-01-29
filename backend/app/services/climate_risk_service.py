"""
Climate Risk Detection Service
Orchestrates data collection and risk analysis
"""
from app.data.nasa_power import nasa_client
from app.services.database import db_service
from app.services.google_maps_service import gmaps_service
from app.services.ai_service import ai_service
from typing import Dict, Any, Optional, List
import logging
from datetime import datetime, timezone

logger = logging.getLogger(__name__)


class ClimateRiskService:
    """
    Main service for detecting and managing climate risks
    """
    
    async def detect_risks_for_region(self, region: str) -> List[Dict[str, Any]]:
        """
        Detect all climate risks for a specific region
        
        Args:
            region: Region name (e.g., 'Nairobi', 'Mombasa')
            
        Returns:
            List of detected risks with details
        """
        # Geocode region to get coordinates
        location = await gmaps_service.geocode_address(region)
        
        if not location:
            logger.error(f"Could not geocode region: {region}")
            return []
        
        latitude = location['latitude']
        longitude = location['longitude']
        
        # Get recent climate data
        climate_data = await nasa_client.get_recent_30_days(latitude, longitude)
        
        if not climate_data:
            logger.error(f"Could not fetch climate data for {region}")
            return []
        
        detected_risks = []
        
        # Check for drought
        drought_analysis = nasa_client.analyze_drought_risk(climate_data)
        if drought_analysis['risk'] == 'drought':
            risk = await self._create_risk_alert(
                region=region,
                risk_type='drought',
                severity=drought_analysis['severity'],
                climate_data=climate_data,
                analysis=drought_analysis
            )
            if risk:
                detected_risks.append(risk)
        
        # Check for flood
        flood_analysis = nasa_client.analyze_flood_risk(climate_data)
        if flood_analysis['risk'] == 'flood':
            risk = await self._create_risk_alert(
                region=region,
                risk_type='flood',
                severity=flood_analysis['severity'],
                climate_data=climate_data,
                analysis=flood_analysis
            )
            if risk:
                detected_risks.append(risk)
        
        return detected_risks
    
    async def _create_risk_alert(
        self,
        region: str,
        risk_type: str,
        severity: str,
        climate_data: Dict[str, Any],
        analysis: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Create a climate risk alert with AI summary
        
        Args:
            region: Region name
            risk_type: Type of risk (drought, flood, etc.)
            severity: Risk severity (low, moderate, high, critical)
            climate_data: Raw climate data
            analysis: Risk analysis results
            
        Returns:
            Created alert dict or None
        """
        try:
            # Generate AI summary
            ai_summary = await ai_service.generate_alert_summary({
                'region': region,
                'risk_type': risk_type,
                'data': analysis
            })
            
            # Create title
            title = f"{severity.upper()} {risk_type.replace('_', ' ').title()} Alert - {region}"
            
            # Create alert in database
            alert_data = {
                'region': region,
                'risk_type': risk_type,
                'severity': severity,
                'title': title,
                'description': ai_summary.get('summary', 'Climate risk detected'),
                'ai_summary': ai_summary,
                'climate_data': analysis,
                'status': 'active'
            }
            
            alert = await db_service.create_alert(alert_data)
            
            if alert:
                logger.info(f"Created {risk_type} alert for {region} with severity {severity}")
                
                # Notify subscribed users
                await self._notify_users_in_region(region, alert)
            
            return alert
        
        except Exception as e:
            logger.error(f"Error creating risk alert: {e}")
            return None
    
    async def _notify_users_in_region(self, region: str, alert: Dict[str, Any]):
        """
        Send notifications to all users in affected region
        
        Args:
            region: Region name
            alert: Alert data
        """
        try:
            # Import messaging clients
            from app.telegram.bot import telegram_bot
            
            users = await db_service.get_users_in_region(region)
            
            if not users:
                logger.info(f"No subscribed users found in {region}")
                return
            
            logger.info(f"Notifying {len(users)} users in {region}")
            
            sent_count = 0
            failed_count = 0
            
            # Send alerts to each user based on their platform
            for user in users:
                try:
                    # Get platform from preferences JSONB field
                    platform = user.get('preferences', {}).get('platform', 'unknown')
                    
                    # Prepare alert data for messaging
                    alert_message_data = {
                        'region': region,
                        'risk_type': alert.get('risk_type', 'unknown'),
                        'severity': alert.get('severity', 'moderate'),
                        'summary': alert.get('description', 'Climate alert detected')
                    }
                    
                    # Send Telegram alert
                    if user.get('telegram_id') and platform == 'telegram':
                        try:
                            # For direct messages, telegram_id is the chat_id
                            chat_id = user.get('telegram_id')
                            
                            await telegram_bot.send_alert(
                                chat_id,
                                alert_message_data
                            )
                            logger.info(f"✅ Sent Telegram alert to user {chat_id}")
                            sent_count += 1
                        except Exception as tg_error:
                            logger.error(f"Telegram error for user {user.get('telegram_id')}: {tg_error}")
                            failed_count += 1
                    
                    # Send SMS alert (if SMS platform exists)
                    elif user.get('phone_number') and platform == 'sms':
                        # TODO: Implement SMS sending when SMS service is available
                        logger.info(f"Would send SMS to {user['phone_number']} (SMS service not yet implemented)")
                    
                    # If no platform match, log it
                    else:
                        logger.warning(f"User {user.get('id')} has no valid messaging platform: platform={platform}, phone={user.get('phone_number')}, telegram={user.get('telegram_id')}")
                    
                except Exception as user_error:
                    logger.error(f"Error sending alert to user {user.get('id')}: {user_error}")
                    failed_count += 1
            
            logger.info(f"Alert notification complete: {sent_count} sent, {failed_count} failed")
        
        except Exception as e:
            logger.error(f"Error notifying users: {e}", exc_info=True)
    
    async def get_risk_forecast(
        self,
        region: str,
        risk_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get current risk status and forecast for a region
        
        Args:
            region: Region name
            risk_type: Specific risk type to check (optional)
            
        Returns:
            Dict with risk status and recommendations
        """
        location = await gmaps_service.geocode_address(region)
        
        if not location:
            return {
                'error': 'Region not found',
                'region': region
            }
        
        # Get climate data
        climate_data = await nasa_client.get_recent_30_days(
            location['latitude'],
            location['longitude']
        )
        
        if not climate_data:
            return {
                'error': 'Climate data unavailable',
                'region': region
            }
        
        # Analyze risks
        drought = nasa_client.analyze_drought_risk(climate_data)
        flood = nasa_client.analyze_flood_risk(climate_data)
        
        # Get active alerts from database
        active_alerts = await db_service.get_active_alerts(region)
        
        return {
            'region': region,
            'risks': {
                'drought': drought,
                'flood': flood
            },
            'active_alerts': active_alerts,
            'timestamp': datetime.now(timezone.utc).isoformat()
        }
    
    async def analyze_location_coordinates(
        self,
        latitude: float,
        longitude: float
    ) -> Dict[str, Any]:
        """
        Analyze climate risks for specific coordinates
        
        Args:
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            
        Returns:
            Dict with risk analysis
        """
        # Reverse geocode to get region
        location = await gmaps_service.reverse_geocode(latitude, longitude)
        
        if not location:
            return {'error': 'Could not determine location'}
        
        region = location.get('region', 'Unknown')
        
        # Get climate data
        climate_data = await nasa_client.get_recent_30_days(latitude, longitude)
        
        if not climate_data:
            return {'error': 'Climate data unavailable'}
        
        # Analyze all risks
        return {
            'location': location,
            'latitude': latitude,
            'longitude': longitude,
            'risks': {
                'drought': nasa_client.analyze_drought_risk(climate_data),
                'flood': nasa_client.analyze_flood_risk(climate_data)
            },
            'timestamp': datetime.now(timezone.utc).isoformat()
        }


# Global climate risk service instance
climate_service = ClimateRiskService()
