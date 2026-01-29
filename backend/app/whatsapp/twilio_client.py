"""Twilio WhatsApp Client for GreenPulse
Handles WhatsApp messaging via Twilio API
"""
from twilio.rest import Client
from app.config import settings
from app.services.database import db_service
from app.services.ai_service import ai_service
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)


class TwilioWhatsAppClient:
    """
    Client for sending and receiving WhatsApp messages via Twilio
    """
    
    def __init__(self):
        self.account_sid = settings.TWILIO_ACCOUNT_SID
        self.auth_token = settings.TWILIO_AUTH_TOKEN
        self.whatsapp_number = settings.TWILIO_WHATSAPP_NUMBER
        self.client = None
        if self.account_sid and self.auth_token:
            self.client = Client(self.account_sid, self.auth_token)
        else:
            logger.warning(
                "Twilio WhatsApp client not configured (missing TWILIO_ACCOUNT_SID/TWILIO_AUTH_TOKEN). "
                "WhatsApp sending will be disabled."
            )
    
    async def send_message(
        self,
        to_number: str,
        message: str,
        media_url: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Send WhatsApp message to a user
        
        Args:
            to_number: Recipient phone number (e.g., '+254712345678')
            message: Message text
            media_url: Optional image/video URL
            
        Returns:
            Dict with success status and message SID
        """
        try:
            if not self.client:
                return {
                    'success': False,
                    'error': 'Twilio credentials not configured'
                }

            # Format WhatsApp number
            if not to_number.startswith('whatsapp:'):
                to_number = f'whatsapp:{to_number}'
            
            # Send message
            params = {
                'from_': self.whatsapp_number,
                'to': to_number,
                'body': message
            }
            
            if media_url:
                params['media_url'] = [media_url]
            
            message_obj = self.client.messages.create(**params)
            
            logger.info(f"WhatsApp message sent to {to_number}: {message_obj.sid}")
            
            return {
                'success': True,
                'message_sid': message_obj.sid,
                'status': message_obj.status
            }
        
        except Exception as e:
            logger.error(f"Failed to send WhatsApp message: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    async def send_alert(
        self,
        phone_number: str,
        alert_data: Dict[str, Any]
    ) -> bool:
        """
        Send climate alert via WhatsApp
        
        Args:
            phone_number: User's phone number
            alert_data: Alert information
            
        Returns:
            True if sent successfully
        """
        severity_emoji = {
            'critical': 'RED ALERT',
            'high': 'HIGH ALERT',
            'moderate': 'ALERT',
            'low': 'NOTICE'
        }
        
        severity = alert_data.get('severity', 'moderate')
        risk_type = alert_data.get('risk_type', 'Unknown')
        region = alert_data.get('region', 'Your area')
        summary = alert_data.get('summary', 'Climate alert detected')
        
        message = f"""*{severity_emoji.get(severity, 'ALERT')}: {risk_type.replace('_', ' ').title()}*


*Region:* {region}

*Severity:* {severity.upper()}


{summary}


Reply with questions or type HELP.

_GreenPulse - Guarding the Land_""".strip()
        
        result = await self.send_message(phone_number, message)
        return result.get('success', False)
    
    async def send_welcome_message(self, phone_number: str, region: str) -> bool:
        """
        Send welcome message to new subscriber
        
        Args:
            phone_number: User's phone number
            region: Subscribed region
            
        Returns:
            True if sent successfully
        """
        message = f"""*Welcome to GreenPulse!*

You're subscribed to climate alerts for:
*{region}*

*You'll receive alerts about:*

• Droughts
• Floods  
• Temperature extremes
• Farming tips


*How to use:*

Ask me anything:
→ "What crops should I plant?"
→ "Weather forecast?"

Commands:
→ STOP to unsubscribe
→ HELP for assistance

_Stay informed, stay resilient!_""".strip()
        
        result = await self.send_message(phone_number, message)
        return result.get('success', False)
    
    async def handle_incoming_message(
        self,
        from_number: str,
        message_body: str,
        profile_name: str = None
    ) -> str:
        """
        Handle incoming WhatsApp message from user
        
        Args:
            from_number: Sender's phone number
            message_body: Message text
            profile_name: Sender's WhatsApp profile name
            
        Returns:
            Response message
        """
        try:
            # Clean phone number
            clean_number = from_number.replace('whatsapp:', '')
            
            # Get or create user immediately
            user = await db_service.get_user_by_phone(clean_number)
            if not user:
                # Create new user
                user = await db_service.get_or_create_phone_user(clean_number, platform="whatsapp")
                logger.info(f"✅ Created new WhatsApp user: {clean_number}")
            
            # Check if new user (needs location)
            is_new_user = not user.get('region')
            
            # Handle commands
            message_lower = message_body.lower().strip()
            
            if message_lower in ['stop', 'unsubscribe', 'cancel']:
                if user:
                    await db_service.unsubscribe_user(user['id'])
                    return "You've been unsubscribed from GreenPulse alerts. Reply START to resubscribe anytime."
                return "You're not currently subscribed."
            
            if message_lower in ['start', 'subscribe', 'begin']:
                return """*Welcome to GreenPulse!*

I'll help you with climate alerts, weather forecasts, and farming tips!

**Please share your location using this exact format:**

→ "I am in Nairobi"
→ "I live in Kitui"
→ "I am from Mombasa"

Using this format helps me correctly identify your location and provide accurate forecasts and alerts for your specific region!
"""
            
            if message_lower in ['help', 'info', '?']:
                return """*GreenPulse Help*

*Commands:*
- STOP - Unsubscribe from alerts
- START - Subscribe to alerts
- HELP - Show this message

*Ask anything:*
- "What's the weather forecast?"
- "Best crops for dry season?"
- "How to conserve water?"

We're here to help!""".strip()
            
            # Use AI to process the message
            from app.services.intent_parser import generate_revolutionary_response
            import asyncio
            
            user_context = {
                'user_id': user['id'] if user else None,
                'phone_number': clean_number,
                'platform': 'whatsapp',
                'has_location': not is_new_user
            }
            
            # Get AI response with timeout (Twilio webhook times out at 15s)
            try:
                result = await asyncio.wait_for(
                    generate_revolutionary_response(message_body, user_context),
                    timeout=12.0  # 12 seconds max - leaves 3s buffer for Twilio
                )
                ai_response = result["response"]
                detected_language = result.get("language", "english")
                location = result.get("location")
                detected_name = result.get("name")  # AI might extract user's name
            
            except asyncio.TimeoutError:
                # AI took too long - send helpful message
                logger.warning(f"⏱️ AI timeout for WhatsApp message from {clean_number}: {message_body[:50]}")
                
                # Quick language detection
                is_swahili = any(word in message_body.lower() for word in ['habari', 'nina', 'hali', 'mambo', 'sasa'])
                
                if is_swahili:
                    return "Samahani rafiki, swali lako ni gumu sana. Jaribu kuuliza kwa maneno machache zaidi au kwa maswali madogo madogo."
                else:
                    return "That's quite a complex question! Could you break it down into smaller questions or use fewer words? I'll answer faster that way."
            
            # Save detected name if provided
            if detected_name and user:
                try:
                    await db_service.update_user_name(user['id'], detected_name)
                    logger.info(f"✅ Saved name '{detected_name}' for WhatsApp user {clean_number}")
                except Exception as name_error:
                    logger.error(f"Could not save user name: {name_error}")
            
            # If location detected, save it and auto-subscribe!
            if location:
                try:
                    # Add additional logging for debugging
                    logger.info(f"🔍 WhatsApp location detected: '{location}' from message: '{message_body[:30]}...'")
                    
                    # Validate location isn't a false positive
                    if len(location) < 3 or location.lower() in ['the', 'this', 'that', 'my', 'our', 'your']:
                        logger.warning(f"❌ Rejected invalid location: '{location}'")
                        # Don't return early, still process the message normally
                    else:
                        # Check cache FIRST (free, instant!)
                        from app.services.location_cache import get_cached_coordinates
                        location_data = get_cached_coordinates(location)
                        
                        if location_data:
                            logger.info(f"✅ Using cached coordinates for {location} (FREE!)")
                        else:
                            # Only call Google Maps API if not in cache
                            from app.services.google_maps_service import gmaps_service
                            location_data = await gmaps_service.geocode_address(location)
                            logger.warning(f"💰 Called Google Maps API for {location} (costs $0.005)")
                        
                        if location_data and user:
                            # Update user location and auto-subscribe
                            await db_service.update_user_location(
                                user_id=user['id'],
                                latitude=location_data.get('latitude'),
                                longitude=location_data.get('longitude'),
                                region=location
                            )
                            
                            # Auto-subscribe user (no questions asked!)
                            await db_service.subscribe_user(user['id'])
                            
                            logger.info(f"✅ Saved location '{location}' and auto-subscribed WhatsApp user {clean_number}")
                            
                            # Get user's name (priority: saved name > detected name > profile name)
                            user_name = user.get('name') or detected_name or profile_name or "friend"
                        
                            welcome_msg = f"""*Perfect, {user_name}!*

You're now subscribed to GreenPulse for *{location}*!


*You'll receive alerts for:*

• Droughts & floods
• Temperature extremes  
• Farming tips
• Weather forecasts


*Ask me anything:*
→ "Weather forecast?"
→ "Best crops to plant?"
→ "How to conserve water?"


_Stay informed, stay resilient!_"""
                        
                            # Send welcome message and STOP - don't send AI response
                            await self.send_message(from_number, welcome_msg)
                            
                            # Return empty to avoid double message
                            return ""
                    
                except Exception as loc_error:
                    logger.error(f"Could not save WhatsApp location: {loc_error}")
            
            # If new user but no location detected yet, remind them
            if is_new_user and not location:
                # Add reminder to response
                ai_response += f"\n\n━━━━━━━━━━━━━━━━━━━━\n\n_Tip: Share your location (e.g., 'Nairobi') to get personalized alerts!_"
            
            # Save conversation to database
            if user:
                try:
                    await db_service.save_sms_message({
                        'user_id': user['id'],
                        'phone_number': clean_number,
                        'message': message_body,
                        'direction': 'incoming',
                        'ai_response': ai_response,
                        'platform': 'whatsapp',
                        'language': detected_language
                    })
                    logger.info(f"✅ Saved WhatsApp conversation for {clean_number}")
                except Exception as save_error:
                    logger.error(f"Could not save WhatsApp conversation: {save_error}", exc_info=True)
            
            return ai_response
        
        except Exception as e:
            logger.error(f"Error handling WhatsApp message: {e}", exc_info=True)
            return "Sorry, I'm having trouble processing your message right now. Please try again in a moment."


# Global WhatsApp client instance
whatsapp_client = TwilioWhatsAppClient()
