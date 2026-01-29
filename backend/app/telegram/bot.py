"""Telegram Bot for GreenPulse
Handles climate alerts and AI chat via Telegram
Uses the same GreenPulse AI Intelligence as the website
"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)
from app.config import settings
from app.services.ai_intelligence import greenpulse_ai
from app.services.database import db_service
from app.services.google_maps_service import gmaps_service
import logging
import json

logger = logging.getLogger(__name__)


class GreenPulseTelegramBot:
    """
    Telegram bot for climate risk alerts and AI assistance
    """
    
    def __init__(self):
        self.token = settings.TELEGRAM_BOT_TOKEN
        self.app = None
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command - Auto-triggered when user starts bot"""
        user = update.effective_user
        
        try:
            from app.services.database import db_service
            
            # Get or create user
            user_record = await db_service.get_or_create_telegram_user(
                telegram_id=user.id,
                username=user.username,
                first_name=user.first_name
            )
            
            # Check if user already has location
            has_location = user_record and user_record.get('region')
            
            if has_location:
                # User already set up - show normal welcome
                welcome_message = f"""Hello {user.first_name}! 👋

Your location: *{user_record['region']}* ✅

━━━━━━━━━━━━━━━━━━━━

*Ask me anything:*
• "What's the weather forecast?"
• "Best crops for this season?"
• "How to prepare for drought?"

━━━━━━━━━━━━━━━━━━━━

_Just type your question!_"""
                
                await update.message.reply_text(welcome_message, parse_mode='Markdown')
            
            else:
                # NEW USER - Ask for location FIRST
                welcome_message = f"""Hello {user.first_name}!

Welcome to *GreenPulse* - Your AI climate assistant for Africa.

━━━━━━━━━━━━━━━━━━━━

*I can help you with:*

• Climate risk alerts
• Weather forecasts  
• Crop recommendations
• Land management tips

━━━━━━━━━━━━━━━━━━━━

**FIRST: Please share your location!**

This helps me give you:
✓ Accurate forecasts
✓ Region-specific alerts  
✓ Localized advice

━━━━━━━━━━━━━━━━━━━━

*How to share:*

1. Tap "Share My Location" below
2. Or type your town/county
   (e.g., "Nairobi", "Kitui")

━━━━━━━━━━━━━━━━━━━━"""
                
                keyboard = [
                    [InlineKeyboardButton("📍 Type My Location", callback_data="enter_location")],
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                
                await update.message.reply_text(
                    welcome_message,
                    parse_mode='Markdown',
                    reply_markup=reply_markup
                )
        
        except Exception as e:
            logger.error(f"Error in start command: {e}")
            # Fallback
            welcome_message = f"""Hello {user.first_name}!

Welcome to *GreenPulse* - Your AI climate assistant for Africa.


*I can help you with:*

• Climate risk alerts
• Weather forecasts  
• Crop recommendations
• Land management tips
• Climate adaptation strategies


*Just chat naturally!*

Examples:
→ "What's the weather in Nairobi?"
→ "Best crops for dry season?"
→ "How to prepare for drought?"

To get daily alerts, tell me your location:
→ "I'm in Kisumu"


_Ninaweza pia kusaidia kwa Kiswahili!_

How can I help you today?"""
            
            keyboard = [
                [
                    InlineKeyboardButton(" Share My Location", callback_data="share_location"),
                    InlineKeyboardButton(" Learn More", callback_data="education"),
                ],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.message.reply_text(
                welcome_message, 
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command - Only if user explicitly asks"""
        help_text = """
*GreenPulse Bot Help*

Just chat with me naturally! I understand questions like:
• "What's the weather forecast?"
• "How do I conserve water on my farm?"
• "Best crops for Nakuru region?"
• "Tell me about soil degradation"

*Special Actions:*
• Share your location to get climate alerts
• Send photos of crop issues for analysis
• Ask about any climate or agriculture topic

*Privacy:* Type "delete my data" to remove your information

What would you like to know?
"""
        await update.message.reply_text(help_text, parse_mode='Markdown')
    
    async def subscribe_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle location sharing for subscriptions"""
        keyboard = [
            [InlineKeyboardButton("📍 Type My Location", callback_data="enter_location")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "To get climate alerts for your area, I need to know your location.\n\nYou can either share your GPS location or just tell me your county/town (e.g., 'Nairobi', 'Mombasa'):",
            reply_markup=reply_markup
        )
    
    async def alerts_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle alerts request"""
        await update.message.reply_text(
            "Let me check the latest climate alerts in your area...\n\n(Connecting to database...)"
        )
        # TODO: Fetch from database
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle all regular messages - Same AI as website"""
        user_message = update.message.text
        user = update.effective_user
        chat_id = update.effective_chat.id
        
        # Show typing indicator
        await context.bot.send_chat_action(chat_id=chat_id, action="typing")
        
        try:
            # Quick greetings - respond instantly
            greetings = ['hello', 'hi', 'hey', 'habari', 'mambo', 'niaje', 'sasa', 'jambo']
            if user_message.lower().strip() in greetings:
                responses = [
                    f"Hello {user.first_name}! How can I help you today?",
                    f"Hi! Ask me about weather, farming, or land management.",
                    f"Habari {user.first_name}! Naweza kukusaidia namna gani?",
                    f"Hey! Ready to help. What's your question?"
                ]
                import random
                response = random.choice(responses)
                await update.message.reply_text(response)
                return
            
            logger.info(f"Processing message from {user.id}: {user_message[:100]}")
            
            # Get user's saved location from database
            user_location = None
            user_record = None
            try:
                from app.services.database import db_service
                user_record = await db_service.get_or_create_telegram_user(
                    telegram_id=user.id,
                    username=user.username,
                    first_name=user.first_name
                )
                if user_record and user_record.get('region'):
                    user_location = user_record['region']
                    logger.info(f"Using saved location: {user_location}")
            except Exception as db_error:
                logger.error(f"Could not get user location: {db_error}")
            
            # Detect location from message if none saved
            detected_location = None
            if not user_location:
                detected_location = self._extract_location_from_message(user_message)
                if detected_location:
                    user_location = detected_location
                    logger.info(f"Detected location from message: {detected_location}")
            
            # Use the SAME GreenPulse AI as the website
            # Mode: community (simple, casual, may use Swahili)
            import asyncio
            try:
                response_text = await asyncio.wait_for(
                    greenpulse_ai.ask(
                        question=user_message,
                        mode="community",
                        location=user_location,
                        include_weather=True
                    ),
                    timeout=60.0
                )
            except asyncio.TimeoutError:
                logger.warning(f"AI timeout for message: {user_message[:100]}")
                await update.message.reply_text(
                    "That's a complex question! Try breaking it into smaller parts."
                )
                return
            
            # Send the response
            await update.message.reply_text(response_text, parse_mode='Markdown')
            
            # Save detected location to database
            if detected_location and user_record:
                try:
                    location_data = await gmaps_service.geocode_address(detected_location)
                    if location_data:
                        await db_service.update_user_location(
                            user_id=user_record['id'],
                            latitude=location_data.get('latitude'),
                            longitude=location_data.get('longitude'),
                            region=detected_location
                        )
                        logger.info(f"Saved location '{detected_location}' for user {user.id}")
                except Exception as loc_error:
                    logger.error(f"Could not save location: {loc_error}")
            
            # Save conversation to database
            try:
                if user_record:
                    await db_service.save_telegram_message({
                        "user_id": user_record["id"],
                        "telegram_id": user.id,
                        "chat_id": chat_id,
                        "username": user.username,
                        "first_name": user.first_name,
                        "message": user_message,
                        "direction": "incoming",
                        "ai_response": response_text,
                        "language": "auto"
                    })
                    logger.info(f"Saved conversation for user {user.id}")
            except Exception as db_error:
                logger.error(f"Database save error: {db_error}")
            
        except Exception as e:
            logger.error(f"Error in message handler: {e}", exc_info=True)
            await update.message.reply_text(
                "Sorry, I had trouble with that. Could you rephrase your question?"
            )
    
    def _extract_location_from_message(self, message: str) -> str | None:
        """Extract Kenya county or town from message"""
        # Common Kenya locations
        kenya_locations = [
            'nairobi', 'mombasa', 'kisumu', 'nakuru', 'eldoret', 'thika', 'malindi',
            'kitale', 'garissa', 'nyeri', 'machakos', 'meru', 'lamu', 'naivasha',
            'kericho', 'bungoma', 'busia', 'kakamega', 'kisii', 'migori', 'homa bay',
            'siaya', 'vihiga', 'nandi', 'uasin gishu', 'trans nzoia', 'west pokot',
            'turkana', 'samburu', 'isiolo', 'marsabit', 'mandera', 'wajir', 'tana river',
            'kilifi', 'kwale', 'taita taveta', 'embu', 'kirinyaga', 'muranga', 'kiambu',
            'nyandarua', 'laikipia', 'baringo', 'elgeyo marakwet', 'narok', 'kajiado',
            'bomet', 'nyamira', 'makueni', 'kitui', 'tharaka nithi'
        ]
        
        message_lower = message.lower()
        
        # Check for "in [location]" pattern
        import re
        in_pattern = re.search(r'\bin\s+([a-zA-Z\s]+)', message_lower)
        if in_pattern:
            potential = in_pattern.group(1).strip()
            for loc in kenya_locations:
                if loc in potential:
                    return loc.title()
        
        # Check for "from [location]" pattern
        from_pattern = re.search(r'\bfrom\s+([a-zA-Z\s]+)', message_lower)
        if from_pattern:
            potential = from_pattern.group(1).strip()
            for loc in kenya_locations:
                if loc in potential:
                    return loc.title()
        
        # Direct mention
        for loc in kenya_locations:
            if loc in message_lower:
                return loc.title()
        
        return None
    
    async def handle_location(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle location sharing"""
        location = update.message.location
        user = update.effective_user
        
        try:
            from app.services.google_maps_service import gmaps_service
            from app.services.database import db_service
            
            # Reverse geocode to get region name
            region_data = await gmaps_service.reverse_geocode(
                location.latitude,
                location.longitude
            )
            
            region_name = region_data.get('region', 'Your area') if region_data else 'Your area'
            
            # Get or create user
            user_record = await db_service.get_or_create_telegram_user(
                telegram_id=user.id,
                username=user.username,
                first_name=user.first_name
            )
            
            if user_record:
                # Update user location in database
                await db_service.update_user_location(
                    user_id=user_record['id'],
                    latitude=location.latitude,
                    longitude=location.longitude,
                    region=region_name
                )
                
                logger.info(f"Saved location for user {user.id}: {region_name}")
                
                await update.message.reply_text(
                    f"✅ Perfect! I've saved your location: *{region_name}*\n\n"
                    "You'll now receive climate alerts for your area. I'll notify you about droughts, floods, and other risks.\n\n"
                    "Feel free to ask me anything!",
                    parse_mode='Markdown'
                )
            else:
                await update.message.reply_text(
                    "Location received, but I couldn't save it to the database. Please try again or type your location name."
                )
                
        except Exception as e:
            logger.error(f"Error handling location: {e}")
            await update.message.reply_text(
                f"Got your location ({location.latitude}, {location.longitude})\n\n"
                "Feel free to ask me anything!"
            )
    
    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle inline keyboard button callbacks"""
        query = update.callback_query
        await query.answer()
        
        callback_data = query.data
        
        if callback_data == "share_location":
            keyboard = [
                [InlineKeyboardButton("📍 Type My Location", callback_data="enter_location")],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.message.reply_text(
                "Tap the button below to share your location, or just tell me your town/county:",
                reply_markup=reply_markup
            )
        elif callback_data == "education":
            await query.message.reply_text(
                "*Climate Resilience Tips*\n\n"
                "━━━━━━━━━━━━━━━━━━━━\n\n"
                "*Drought Preparation:*\n\n"
                "• Plant drought-resistant crops\n"
                "  (sorghum, millet, cassava)\n\n"
                "• Implement water harvesting\n\n"
                "• Use mulching to retain moisture\n\n"
                "━━━━━━━━━━━━━━━━━━━━\n\n"
                "*Flood Protection:*\n\n"
                "• Build terraces on slopes\n\n"
                "• Plant trees to prevent erosion\n\n"
                "• Create drainage channels\n\n"
                "━━━━━━━━━━━━━━━━━━━━\n\n"
                "Ask me for specific advice anytime!",
                parse_mode='Markdown'
            )
        elif callback_data == "enter_location":
            await query.message.reply_text(
                "Just type your location and I'll set up alerts!\n\n"
                "Examples:\n"
                "→ Nairobi\n"
                "→ Kisumu\n"
                "→ Mombasa"
            )
        elif callback_data == "confirm_subscription":
            await query.message.reply_text(
                "✓ *Subscribed Successfully!*\n\n"
                "You'll receive daily climate alerts and risk warnings for your area.\n\n"
                "Feel free to ask me anything anytime!",
                parse_mode='Markdown'
            )
        elif callback_data == "no_subscription":
            await query.message.reply_text(
                "No problem!\n\n"
                "You can still chat with me anytime about climate, weather, or agriculture.\n\n"
                "Just ask away!"
            )
    
    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle errors"""
        logger.error(f"Telegram bot error: {context.error}")
        
        if update and update.effective_message:
            await update.effective_message.reply_text(
                "An error occurred while processing your request. Please try again later."
            )
    
    def build_application(self):
        """Build and configure the Telegram bot application"""
        self.app = Application.builder().token(self.token).build()
        
        # Command handlers (hidden from users, but work if typed)
        self.app.add_handler(CommandHandler("start", self.start_command))
        self.app.add_handler(CommandHandler("help", self.help_command))
        
        # Location handler (for sharing GPS)
        self.app.add_handler(MessageHandler(filters.LOCATION, self.handle_location))
        
        # Callback query handler (inline buttons)
        self.app.add_handler(CallbackQueryHandler(self.handle_callback))
        
        # Message handler - ALL text messages go to AI (natural conversation)
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        
        # Error handler
        self.app.add_error_handler(self.error_handler)
        
        return self.app
    
    async def send_alert(self, chat_id: int, alert_data: dict):
        """
        Send climate alert to a specific user
        
        Args:
            chat_id: Telegram chat ID
            alert_data: Alert information dict
        """
        severity_emoji_map = {
            "critical": "🔴 RED ALERT",
            "high": "⚠️ HIGH ALERT",
            "moderate": "⚡ ALERT",
            "low": "ℹ️ NOTICE"
        }
        
        severity = alert_data.get("severity", "moderate")
        risk_type = alert_data.get("risk_type", "Unknown")
        region = alert_data.get("region", "Your area")
        summary = alert_data.get("summary", "Climate alert detected")
        
        message = f"""*{severity_emoji_map.get(severity, "ALERT")}: {risk_type.replace('_', ' ').title()}*

*Region:* {region}
*Severity:* {severity.upper()}

{summary}

Stay safe and follow local advisories.

_GreenPulse - Guarding the Land_"""
        
        try:
            # Use Bot API directly without requiring Application to be initialized
            # This allows sending alerts from the cron job independently
            from telegram import Bot
            
            bot = Bot(token=self.token)
            
            async with bot:
                await bot.send_message(
                    chat_id=chat_id,
                    text=message,
                    parse_mode='Markdown'
                )
                logger.info(f"✅ Successfully sent alert to Telegram chat_id {chat_id}")
            
        except Exception as e:
            logger.error(f"Failed to send alert to chat_id {chat_id}: {e}")


# Global bot instance
telegram_bot = GreenPulseTelegramBot()
