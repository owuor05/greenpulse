"""Telegram Bot for GreenPulse
Handles climate alerts and AI chat via Telegram
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
from app.services.ai_service import ai_service
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
        """Handle all regular messages - Revolutionary AI-first conversation"""
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
                    f"Hello {user.first_name}!\n\nHow can I help you today?",
                    f"Hi there!\n\nAsk me about weather, farming, or land management.",
                    f"Habari {user.first_name}!\n\nNaweza kukusaidia namna gani?",
                    f"Hey!\n\nReady to help. What's your question?"
                ]
                import random
                response = random.choice(responses)
                await update.message.reply_text(response, parse_mode='Markdown')
                return
            
            # REVOLUTIONARY SINGLE-CALL APPROACH
            # Let GPT-5 do everything: detect language, extract location, generate response
            from app.services.intent_parser import generate_revolutionary_response
            import asyncio
            
            logger.info(f"Processing message: {user_message}")
            
            # Build user context
            user_context = {
                "user_id": user.id,
                "username": user.username,
                "first_name": user.first_name,
                "platform": "telegram"
            }
            
            # Get revolutionary AI response (single call!) with timeout protection
            try:
                result = await asyncio.wait_for(
                    generate_revolutionary_response(user_message, user_context),
                    timeout=60.0  # 60 seconds max for faster responses
                )
                
                response_text = result["response"]
                location = result.get("location")
                needs_climate = result.get("needs_climate_data", False)
                wants_subscription = result.get("subscribe_intent", False)
                detected_name = result.get("name")
            
            except asyncio.TimeoutError:
                # AI took too long - send helpful message
                logger.warning(f"⏱️ AI timeout for Telegram message from {user.id}: {user_message[:100]}")
                
                await update.message.reply_text(
                    "That's a complex question! Could you break it into smaller parts or use fewer words? I'll respond faster.",
                    parse_mode='Markdown'
                )
                return
            
            logger.info(f"AI Response - Language: {result['language']}, Location: {location}, Name: {detected_name}")
            
            # SMART SYSTEM INTEGRATION
            # If AI detected location need and we have location, fetch real data
            if location and needs_climate:
                try:
                    # Check cache FIRST (free!)
                    from app.services.location_cache import get_cached_coordinates
                    location_data = get_cached_coordinates(location)
                    
                    if not location_data:
                        # Only call Google Maps API if not cached
                        from app.services.google_maps_service import gmaps_service
                        location_data = await gmaps_service.geocode_address(location)
                    
                    if location_data:
                        from app.services.climate_risk_service import climate_risk_service
                        # Get real climate data from NASA
                        climate_info = await climate_risk_service.detect_risks_for_region(location)
                        
                        if climate_info:
                            # Enhance response with real data
                            if result['language'] == 'swahili':
                                data_note = f"\n\n━━━━━━━━━━━━━━━━━━━━\n\n*Taarifa za Hali ya Hewa - {location}*\n\n{json.dumps(climate_info, indent=2, ensure_ascii=False)}"
                            else:
                                data_note = f"\n\n━━━━━━━━━━━━━━━━━━━━\n\n*Real Climate Data - {location}*\n\n{json.dumps(climate_info, indent=2)}"
                            
                            # Let GPT-5 format the data beautifully
                            logger.info(f"Fetched climate data for {location}")
                
                except Exception as loc_error:
                    logger.error(f"Location/climate data error: {loc_error}")
            
            # Offer subscription if user wants alerts
            if wants_subscription and location:
                if result['language'] == 'swahili':
                    response_text += f"\n\n━━━━━━━━━━━━━━━━━━━━\n\n*Taarifa za Kila Siku*\n\nUngependa kupokea taarifa za hali ya hewa kila siku kwa {location}?"
                else:
                    response_text += f"\n\n━━━━━━━━━━━━━━━━━━━━\n\n*Daily Climate Alerts*\n\nWould you like to receive daily weather updates and risk alerts for {location}?"
                
                await update.message.reply_text(
                    response_text,
                    parse_mode='Markdown',
                    reply_markup=InlineKeyboardMarkup([[
                        InlineKeyboardButton("✓ Yes" if result['language'] == 'english' else "✓ Ndio", callback_data="confirm_subscription"),
                        InlineKeyboardButton("✗ No" if result['language'] == 'english' else "✗ Hapana", callback_data="no_subscription")
                    ]])
                )
            else:
                await update.message.reply_text(response_text, parse_mode='Markdown')
            
            # Save conversation to database
            try:
                from app.services.database import db_service
                
                # Get or create user
                user_record = await db_service.get_or_create_telegram_user(
                    telegram_id=user.id,
                    username=user.username,
                    first_name=user.first_name
                )
                
                if user_record:
                    # Save detected name if provided
                    if detected_name:
                        try:
                            await db_service.update_user_name(user_record['id'], detected_name)
                            logger.info(f"✅ Saved name '{detected_name}' for Telegram user {user.id}")
                        except Exception as name_error:
                            logger.error(f"Could not save user name: {name_error}")
                    
                    # If location was detected, save it to database
                    if location and not user_record.get('region'):
                        try:
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
                            
                            if location_data:
                                await db_service.update_user_location(
                                    user_id=user_record['id'],
                                    latitude=location_data.get('latitude'),
                                    longitude=location_data.get('longitude'),
                                    region=location
                                )
                                logger.info(f"✅ Saved typed location '{location}' for user {user.id}")
                        except Exception as loc_save_error:
                            logger.error(f"Could not save typed location: {loc_save_error}")
                    # Save incoming message
                    await db_service.save_telegram_message({
                        "user_id": user_record["id"],
                        "telegram_id": user.id,
                        "chat_id": chat_id,
                        "username": user.username,
                        "first_name": user.first_name,
                        "message": user_message,
                        "direction": "incoming",
                        "ai_response": response_text,
                        "language": result.get("language", "english")
                    })
                    
                    logger.info(f"Saved Telegram conversation for user {user.id}")
                else:
                    logger.warning(f"Could not save conversation - user creation failed")
                    
            except Exception as db_error:
                logger.error(f"Database save error: {db_error}", exc_info=True)
                # Don't fail the chat if database save fails
            
        except Exception as e:
            logger.error(f"Error in message handler: {e}", exc_info=True)
            error_str = str(e)
            
            # Smart error messages
            if '429' in error_str or 'Too Many Requests' in error_str:
                await update.message.reply_text(
                    "Rafiki, I'm getting too many requests right now.\n\nPlease try again in a few minutes."
                )
            else:
                await update.message.reply_text(
                    "Sorry, I had trouble with that.\n\nCould you rephrase your question?"
                )
    
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
