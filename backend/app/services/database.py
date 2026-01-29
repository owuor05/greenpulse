"""
Database service for Terraguard
Handles all Supabase interactions
"""
from supabase import create_client, Client
from app.config import settings
from typing import Optional, List, Dict, Any
import logging

logger = logging.getLogger(__name__)


class DatabaseService:
    """
    Service for interacting with Supabase database
    """
    
    def __init__(self):
        self.client: Client = create_client(
            settings.SUPABASE_URL,
            settings.SUPABASE_KEY
        )
    
    # USERS
    async def get_user_by_phone(self, phone_number: str) -> Optional[Dict[str, Any]]:
        """Get user by phone number"""
        try:
            response = self.client.table("users").select("*").eq("phone_number", phone_number).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            logger.error(f"Error getting user by phone: {e}")
            return None
    
    async def get_user_by_telegram_id(self, telegram_id: int) -> Optional[Dict[str, Any]]:
        """Get user by Telegram ID"""
        try:
            response = self.client.table("users").select("*").eq("telegram_id", telegram_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            logger.error(f"Error getting user by telegram_id: {e}")
            return None
    
    async def create_user(self, user_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create new user"""
        try:
            response = self.client.table("users").insert(user_data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            return None
    
    async def update_user_location(self, user_id: str, latitude: float, longitude: float, region: str) -> bool:
        """Update user location"""
        try:
            self.client.table("users").update({
                "latitude": latitude,
                "longitude": longitude,
                "region": region
            }).eq("id", user_id).execute()
            return True
        except Exception as e:
            logger.error(f"Error updating user location: {e}")
            return False
    
    async def update_user_name(self, user_id: str, name: str) -> bool:
        """Update user's name"""
        try:
            self.client.table("users").update({
                "name": name
            }).eq("id", user_id).execute()
            logger.info(f"✅ Updated name for user {user_id}: {name}")
            return True
        except Exception as e:
            logger.error(f"Error updating user name: {e}")
            return False
    
    async def subscribe_user(self, user_id: str) -> bool:
        """Subscribe user to alerts"""
        try:
            self.client.table("users").update({
                "subscribed": True
            }).eq("id", user_id).execute()
            logger.info(f"✅ Subscribed user {user_id}")
            return True
        except Exception as e:
            logger.error(f"Error subscribing user: {e}")
            return False
    
    async def unsubscribe_user(self, user_id: str) -> bool:
        """Unsubscribe user from alerts"""
        try:
            self.client.table("users").update({
                "subscribed": False
            }).eq("id", user_id).execute()
            logger.info(f"✅ Unsubscribed user {user_id}")
            return True
        except Exception as e:
            logger.error(f"Error unsubscribing user: {e}")
            return False
    
    # ALERTS
    async def create_alert(self, alert_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create new climate alert"""
        try:
            response = self.client.table("alerts").insert(alert_data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            logger.error(f"Error creating alert: {e}")
            return None
    
    async def get_active_alerts(self, region: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get active alerts, optionally filtered by region"""
        try:
            # Fetch active alerts (optionally filtered by region)
            query = self.client.table("alerts").select("*").eq("status", "active")

            if region:
                query = query.eq("region", region)

            response = query.order("created_at", desc=True).execute()
            alerts = response.data or []

            if not alerts:
                return []

            # Deduplicate: keep latest alert per (region, risk_type, severity)
            deduped = {}
            for a in alerts:
                key = (a.get("region"), a.get("risk_type"), a.get("severity"))
                # If not seen or this one is newer, replace
                if key not in deduped:
                    deduped[key] = a
                else:
                    try:
                        # Compare created_at timestamps; keep the latest
                        existing = deduped[key]
                        if str(a.get("created_at", "")) > str(existing.get("created_at", "")):
                            deduped[key] = a
                    except Exception:
                        # If comparison fails, keep the first
                        pass

            # Return newest-first list
            return sorted(deduped.values(), key=lambda x: str(x.get("created_at", "")), reverse=True)
        except Exception as e:
            logger.error(f"Error getting active alerts: {e}")
            return []
    
    async def get_alert_by_id(self, alert_id: str) -> Optional[Dict[str, Any]]:
        """Get specific alert by ID"""
        try:
            response = self.client.table("alerts").select("*").eq("id", alert_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            logger.error(f"Error getting alert: {e}")
            return None
    
    async def get_users_in_region(self, region: str) -> List[Dict[str, Any]]:
        """Get all subscribed users in a specific region"""
        try:
            response = self.client.table("users").select("*").eq("region", region).eq("subscribed", True).execute()
            return response.data or []
        except Exception as e:
            logger.error(f"Error getting users in region: {e}")
            return []
    
    async def get_all_subscribed_regions(self) -> List[str]:
        """Get list of unique regions with subscribed users"""
        try:
            response = self.client.table("users").select("region").eq("subscribed", True).execute()
            
            if not response.data:
                return []
            
            # Extract unique regions (filter out None/empty values)
            regions = set()
            for user in response.data:
                region = user.get("region")
                if region and region.strip():
                    regions.add(region.strip())
            
            return list(regions)
        except Exception as e:
            logger.error(f"Error getting subscribed regions: {e}")
            return []
    
    # EDUCATION
    async def get_education_articles(self, category: Optional[str] = None, limit: int = 10) -> List[Dict[str, Any]]:
        """Get education articles"""
        try:
            query = self.client.table("education_articles").select("*")
            
            if category:
                query = query.eq("category", category)
            
            response = query.order("created_at", desc=True).limit(limit).execute()
            return response.data or []
        except Exception as e:
            logger.error(f"Error getting education articles: {e}")
            return []
    
    async def get_article_by_slug(self, slug: str) -> Optional[Dict[str, Any]]:
        """Get specific article by slug"""
        try:
            response = self.client.table("education_articles").select("*").eq("slug", slug).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            logger.error(f"Error getting article: {e}")
            return None
    
    # COMMUNITY REPORTS
    async def create_report(self, report_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create community report"""
        try:
            response = self.client.table("community_reports").insert(report_data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            logger.error(f"Error creating report: {e}")
            return None
    
    async def get_reports(self, region: Optional[str] = None, status: str = "pending") -> List[Dict[str, Any]]:
        """Get community reports"""
        try:
            query = self.client.table("community_reports").select("*").eq("status", status)
            
            if region:
                query = query.eq("region", region)
            
            response = query.order("created_at", desc=True).execute()
            return response.data or []
        except Exception as e:
            logger.error(f"Error getting reports: {e}")
            return []
    
    # CHAT HISTORY
    async def save_sms_message(self, message_data: Dict[str, Any]) -> bool:
        """Save SMS/WhatsApp chat message"""
        try:
            self.client.table("sms_chat_history").insert(message_data).execute()
            return True
        except Exception as e:
            logger.error(f"Error saving SMS/WhatsApp message: {e}")
            return False
    
    async def save_telegram_message(self, message_data: Dict[str, Any]) -> bool:
        """Save Telegram chat message"""
        try:
            self.client.table("telegram_chat_history").insert(message_data).execute()
            return True
        except Exception as e:
            logger.error(f"Error saving Telegram message: {e}")
            return False
    
    async def get_or_create_telegram_user(self, telegram_id: int, username: str = None, first_name: str = None) -> Optional[Dict[str, Any]]:
        """Get or create user by Telegram ID"""
        try:
            # Try to get existing user
            user = await self.get_user_by_telegram_id(telegram_id)
            
            if user:
                return user
            
            # Create new user
            user_data = {
                "telegram_id": telegram_id,
                "username": username,
                "subscribed": True,
                "preferences": {"platform": "telegram"}
            }
            
            return await self.create_user(user_data)
        except Exception as e:
            logger.error(f"Error getting/creating Telegram user: {e}")
            return None
    
    async def get_or_create_phone_user(self, phone_number: str, platform: str = "whatsapp") -> Optional[Dict[str, Any]]:
        """Get or create user by phone number"""
        try:
            # Try to get existing user
            user = await self.get_user_by_phone(phone_number)
            
            if user:
                return user
            
            # Create new user
            user_data = {
                "phone_number": phone_number,
                "subscribed": True,
                "preferences": {"platform": platform}
            }
            
            return await self.create_user(user_data)
        except Exception as e:
            logger.error(f"Error getting/creating phone user: {e}")
            return None
    
    async def get_chat_history(self, user_id: str, platform: str = "sms", limit: int = 10) -> List[Dict[str, Any]]:
        """Get chat history for a user"""
        try:
            table = "sms_chat_history" if platform == "sms" else "telegram_chat_history"
            response = self.client.table(table).select("*").eq("user_id", user_id).order("created_at", desc=True).limit(limit).execute()
            return response.data or []
        except Exception as e:
            logger.error(f"Error getting chat history: {e}")
            return []
    
    # AI FEEDBACK
    async def save_ai_feedback(self, feedback_data: Dict[str, Any]) -> bool:
        """Save AI response feedback"""
        try:
            self.client.table("ai_feedback").insert(feedback_data).execute()
            return True
        except Exception as e:
            logger.error(f"Error saving AI feedback: {e}")
            return False
    
    # LAND DATA CACHE
    async def get_cached_land_data(self, location_name: str) -> Optional[Dict[str, Any]]:
        """Get cached land data if not expired (< 24 hours)"""
        try:
            response = self.client.table("land_data_cache").select("*").eq("location_name", location_name).gt("expires_at", "now()").order("created_at", desc=True).limit(1).execute()
            
            if response.data:
                logger.info(f"✅ Cache HIT for location: {location_name}")
                return response.data[0]
            
            logger.info(f"❌ Cache MISS for location: {location_name}")
            return None
        except Exception as e:
            logger.error(f"Error getting cached land data: {e}")
            return None
    
    async def save_land_data_cache(self, cache_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Save land data to cache (24-hour expiry)"""
        try:
            response = self.client.table("land_data_cache").insert(cache_data).execute()
            
            if response.data:
                logger.info(f"✅ Cached land data for: {cache_data.get('location_name')}")
                return response.data[0]
            
            return None
        except Exception as e:
            logger.error(f"Error saving land data cache: {e}")
            return None


# Global database service instance
db_service = DatabaseService()
