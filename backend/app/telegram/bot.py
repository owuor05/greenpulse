"""Telegram Bot for GreenPulse AI

GreenPulse AI is a smart, fast, and analytical AI system designed to help
governments, businesses, communities, and institutions in Kenya understand
environmental conditions, assess risks, ensure compliance, and make
climate-smart decisions using data, reasoning, and scientific knowledge.
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
    Telegram bot for GreenPulse AI - Environmental Intelligence for Kenya
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

Welcome to **GreenPulse AI** - Environmental Intelligence for Kenya.

Your location: **{user_record['region']}** ✅

━━━━━━━━━━━━━━━━━━━━

**I can help you with:**
• Environmental decision analysis
• Climate & weather intelligence
• Regulatory compliance (NEMA, EMCA)
• Land & water risk assessment
• Energy transition planning

━━━━━━━━━━━━━━━━━━━━

**Examples:**
• "What's the weather in Nakuru?"
• "Is this land suitable for construction?"
• "What NEMA permits do I need for a factory?"
• "Analyze climate risks for my farm"

_Just type your question!_"""
                
                await update.message.reply_text(welcome_message, parse_mode='Markdown')
            
            else:
                # NEW USER - Welcome with new identity
                welcome_message = f"""Hello {user.first_name}! 👋

Welcome to **GreenPulse AI** - Environmental Intelligence for Kenya.

━━━━━━━━━━━━━━━━━━━━

**I can help you with:**

• Environmental decision analysis
• Climate & weather intelligence  
• Regulatory compliance (NEMA, EMCA)
• Land & water risk assessment
• Energy transition planning

━━━━━━━━━━━━━━━━━━━━

**Examples:**
• "What's the weather in Nakuru?"
• "Is this land suitable for construction?"
• "What NEMA permits do I need?"
• "Analyze climate risks for my farm"

━━━━━━━━━━━━━━━━━━━━

_Just type your question to get started!_"""
                
                await update.message.reply_text(
                    welcome_message,
                    parse_mode='Markdown'
                )
        
        except Exception as e:
            logger.error(f"Error in start command: {e}")
            # Fallback
            welcome_message = f"""Hello {user.first_name}! 👋

Welcome to **GreenPulse AI** - Environmental Intelligence for Kenya.

**I can help you with:**
• Environmental decision analysis
• Climate & weather intelligence
• Regulatory compliance (NEMA, EMCA)
• Land & water risk assessment

**Just chat naturally!**

Examples:
→ "What's the weather in Nairobi?"
→ "What NEMA permits do I need?"
→ "Analyze risks for land in Kitui"

_Ninaweza pia kusaidia kwa Kiswahili!_

How can I help you today?"""
            
            await update.message.reply_text(
                welcome_message,
                parse_mode='Markdown'
            )
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        help_text = """**GreenPulse AI Help**

I'm an environmental intelligence system for Kenya. Just chat naturally!

**I can help with:**
• Weather & climate analysis
• Environmental impact assessment
• NEMA & regulatory compliance
• Land suitability & risk analysis
• Energy transition planning
• Agricultural advice

**Examples:**
• "What's the weather in Mombasa?"
• "What permits do I need for a factory?"
• "Analyze flood risk in Kisumu"
• "Is this land suitable for farming?"

**Tips:**
• Include location for better answers
• Upload documents for analysis
• Ask "what-if" scenarios

What would you like to know?
"""
        await update.message.reply_text(help_text, parse_mode='Markdown')
    
    async def location_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /location command - set user location"""
        await update.message.reply_text(
            "To set your location, just tell me your county or town.\n\n"
            "Examples:\n"
            "→ Nairobi\n"
            "→ Mombasa\n"
            "→ Kisumu\n\n"
            "Or share your GPS location using the attachment button."
        )
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle all regular messages - Smart AI with automatic location detection"""
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
                user_record = await db_service.get_or_create_telegram_user(
                    telegram_id=user.id,
                    username=user.username,
                    first_name=user.first_name
                )
                if user_record and user_record.get('region'):
                    user_location = user_record['region']
                    logger.info(f"User has saved location: {user_location}")
            except Exception as db_error:
                logger.error(f"Could not get user record: {db_error}")
            
            # SMART: Use AI to extract location from message
            detected_location = await greenpulse_ai.extract_location(user_message)
            if detected_location:
                user_location = detected_location
                logger.info(f"AI detected location: {detected_location}")
            
            # Use the SAME GreenPulse AI as the website
            # Pass location - AI will get ALL weather data and decide what to use
            import asyncio
            try:
                result = await asyncio.wait_for(
                    greenpulse_ai.ask(
                        question=user_message,
                        mode="community",
                        location=user_location,
                        include_weather=True,
                        telegram_fast_mode=True  # AI knows to be fast and concise (30s target)
                    ),
                    timeout=120.0  # 120s safety timeout, but AI targets 30s response
                )
            except asyncio.TimeoutError:
                logger.warning(f"AI timeout for message: {user_message[:100]}")
                await update.message.reply_text(
                    "Taking a bit longer than expected. Please try again or simplify your question."
                )
                return
            
            # Extract the answer text from the result dict
            if result.get("success"):
                response_text = result.get("answer", "I couldn't generate a response. Please try again.")
            else:
                response_text = "Sorry, I'm having trouble right now. Please try again."
                logger.error(f"AI error: {result.get('error')}")
            
            # Send the response
            try:
                await update.message.reply_text(response_text, parse_mode='Markdown')
            except Exception as md_error:
                # If markdown fails, send as plain text
                logger.warning(f"Markdown parse error, sending plain: {md_error}")
                await update.message.reply_text(response_text)
            
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
    
    # NOTE: Removed hardcoded _extract_location_from_message() function
    # Now using AI-based location extraction via greenpulse_ai.extract_location()
    # This is smarter and knows ALL Kenya locations without maintenance
    
    async def handle_location(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle location sharing"""
        location = update.message.location
        user = update.effective_user
        
        try:
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
                    f"✅ Location saved: **{region_name}**\n\n"
                    "I'll use this for localized environmental analysis.\n\n"
                    "Ask me anything about weather, climate risks, land assessment, or environmental compliance!",
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
                "Just type your location (county or town).\n\n"
                "Examples:\n"
                "→ Nairobi\n"
                "→ Kisumu\n"
                "→ Mombasa"
            )
        elif callback_data == "confirm_location":
            await query.message.reply_text(
                "✅ **Location Saved!**\n\n"
                "I'll use this for localized environmental analysis.\n\n"
                "Ask me anything!",
                parse_mode='Markdown'
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
        
        # Command handlers
        self.app.add_handler(CommandHandler("start", self.start_command))
        self.app.add_handler(CommandHandler("help", self.help_command))
        self.app.add_handler(CommandHandler("location", self.location_command))
        
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
        
        message = f"""**{severity_emoji_map.get(severity, "ALERT")}: {risk_type.replace('_', ' ').title()}**

**Region:** {region}
**Severity:** {severity.upper()}

{summary}

Stay safe and follow local advisories.

_GreenPulse AI - Environmental Intelligence for Kenya_"""
        
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
