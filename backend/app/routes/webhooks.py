"""
WhatsApp webhook endpoints for Twilio
"""
from fastapi import APIRouter, Request, Form, HTTPException
from app.whatsapp.twilio_client import whatsapp_client
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/webhook", tags=["webhooks"])


@router.post("/whatsapp")
async def whatsapp_webhook(
    From: str = Form(...),
    Body: str = Form(...),
    MessageSid: str = Form(None),
    ProfileName: str = Form(None)
):
    """
    Twilio WhatsApp webhook endpoint
    Receives incoming WhatsApp messages and processes them
    
    Args:
        From: Sender's WhatsApp number (format: whatsapp:+1234567890)
        Body: Message content
        MessageSid: Twilio message ID
        ProfileName: Sender's WhatsApp profile name
    
    Returns:
        Success/error status
    """
    try:
        logger.info(f"WhatsApp message from {From} ({ProfileName}): {Body}")
        
        # Handle the incoming message with profile name
        response = await whatsapp_client.handle_incoming_message(
            from_number=From,
            message_body=Body,
            profile_name=ProfileName
        )
        
        # Send response back to user
        if response:
            result = await whatsapp_client.send_message(From, response)
            
            if result.get('success'):
                logger.info(f"Response sent to {From}")
                return {"status": "success", "message_sid": result.get('message_sid')}
            else:
                logger.error(f"Failed to send response: {result.get('error')}")
                return {"status": "error", "message": result.get('error')}
        
        return {"status": "success", "message": "processed"}
    
    except Exception as e:
        logger.error(f"WhatsApp webhook error: {e}", exc_info=True)
        return {"status": "error", "message": str(e)}


@router.get("/whatsapp")
async def whatsapp_webhook_verification():
    """
    Webhook verification endpoint
    Used by Twilio to verify the webhook URL is active
    """
    return {"status": "active", "service": "GreenPulse WhatsApp Webhook"}


@router.post("/telegram")
async def telegram_webhook(request: Request):
    """
    Telegram webhook endpoint (alternative to polling)
    Currently using polling mode, but this is here for future webhook support
    """
    try:
        data = await request.json()
        logger.info(f"Telegram webhook received: {data}")
        
        # Process telegram update
        # (Currently bot uses polling, but this is ready for webhook mode)
        
        return {"status": "success"}
    
    except Exception as e:
        logger.error(f"Telegram webhook error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
