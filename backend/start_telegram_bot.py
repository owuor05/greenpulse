"""
Start Telegram Bot
Run this to start the Terraguard Telegram bot
"""
import asyncio
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.telegram.bot import telegram_bot
import logging

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def main():
    """Start the bot"""
    print("Starting Terraguard Telegram Bot...")
    print("Bot will run until you press Ctrl+C")
    
    # Build application
    application = telegram_bot.build_application()
    
    # Start bot
    await application.initialize()
    await application.start()
    await application.updater.start_polling()
    
    print("Bot is running! Send /start to your bot on Telegram")
    print("Press Ctrl+C to stop")
    
    # Run until stopped
    await asyncio.Event().wait()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nBot stopped by user")
