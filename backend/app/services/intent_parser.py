"""AI Smart Response Generator for GreenPulse
Revolutionary single-call approach that maximizes GPT-5 capabilities
"""
from app.services.ai_service import ai_service
from typing import Dict, Any, Optional
import json
import re
import logging

logger = logging.getLogger(__name__)


def detect_language_simple(message: str) -> str:
    """
    Quick language detection using common Swahili words
    Fallback for when AI detection is needed instantly
    """
    swahili_keywords = [
        'habari', 'ninaishi', 'tafadhali', 'ninaweza', 'hali', 'hewa', 
        'nini', 'nina', 'nataka', 'naomba', 'sasa', 'leo', 'kesho',
        'mambo', 'niaje', 'poa', 'safi', 'bado', 'tu', 'tu', 'kwa',
        'ya', 'za', 'wa', 'unaweza', 'naweza', 'wanaweza'
    ]
    
    message_lower = message.lower()
    swahili_count = sum(1 for word in swahili_keywords if word in message_lower)
    
    return "swahili" if swahili_count >= 2 else "english"


def extract_location_keywords(message: str) -> Optional[str]:
    """
    Extract location from message using keywords and patterns
    """
    # Common Kenyan/East African locations
    locations = [
        'nairobi', 'mombasa', 'kisumu', 'nakuru', 'eldoret', 'thika', 'malindi',
        'kitale', 'garissa', 'kakamega', 'machakos', 'nyeri', 'meru', 'embu',
        'kampala', 'dar es salaam', 'arusha', 'kigali', 'dodoma', 'jinja',
        'kilifi', 'lamu', 'voi', 'taveta', 'kitui', 'wajir', 'mandera', 'marsabit',
        'isiolo', 'nanyuki', 'nyahururu', 'naivasha', 'busia', 'malaba', 'kericho'
    ]
    
    message_lower = message.lower()
    
    # Priority 1: Check for explicit location patterns - these are the most reliable
    location_patterns = [
        r'(?:i am in|i\'m in|i live in|i am from|i\'m from|ninaishi)\s+([A-Za-z]+(?:\s+[A-Za-z]+)?)',
        r'(?:my location is|my region is|my area is|my town is|my county is)\s+([A-Za-z]+(?:\s+[A-Za-z]+)?)',
        r'(?:i stay in|i reside in|i am located in|i\'m located in|located in)\s+([A-Za-z]+(?:\s+[A-Za-z]+)?)'
    ]
    
    for pattern in location_patterns:
        match = re.search(pattern, message_lower, re.IGNORECASE)
        if match:
            location = match.group(1).strip().title()
            logger.info(f"✅ Explicit location found: {location}")
            return location
    
    # Priority 2: Check for exact matches of known locations
    for location in locations:
        if f' {location} ' in f' {message_lower} ':  # Add spaces to match whole words
            logger.info(f"✅ Known location found: {location.title()}")
            return location.title()
    
    # Priority 3: Check for simple preposition patterns (less reliable)
    simple_patterns = [
        r'(?:in|from|at)\s+([A-Za-z][a-z]+(?:\s+[A-Za-z][a-z]+)?)',
        r'(?:to)\s+([A-Za-z][a-z]+(?:\s+[A-Za-z][a-z]+)?)'
    ]
    
    for pattern in simple_patterns:
        match = re.search(pattern, message_lower, re.IGNORECASE)
        if match:
            location = match.group(1).strip().title()
            # Validate it's not a common non-location word
            if location.lower() not in ['home', 'work', 'school', 'there', 'here', 'somewhere', 'anywhere']:
                logger.info(f"✅ Inferred location found: {location}")
                return location
    
    return None


def extract_name_keywords(message: str) -> Optional[str]:
    """
    Extract user's name from message using keywords and patterns
    """
    message_lower = message.lower()
    
    # Patterns for name extraction
    patterns = [
        # More explicit name patterns that avoid location conflicts
        r'(?:my name is|call me|i am called|i\'m called)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)',
        r'(?:jina langu ni|naitwa)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)',
        
        # More careful pattern for "I am" that avoids matching "I am in [Location]"
        r'(?:i am|i\'m)\s+(?!in\s|at\s|from\s|near\s|around\s|close\s)([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, message, re.IGNORECASE)
        if match:
            name = match.group(1).strip()
            # Additional validation - not a location indicator and not a common word
            if (name.lower() not in ['a', 'the', 'from', 'in', 'at', 'to', 'is', 'living', 'staying', 'based']) and not name.lower().startswith(('in ', 'at ', 'from ')):
                return name.title()
    
    return None


async def generate_revolutionary_response(
    user_message: str,
    user_context: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Revolutionary single-call AI response that maximizes GPT-5 capabilities
    
    This function:
    1. Detects language automatically
    2. Extracts location and name
    3. Tells us what data to fetch
    4. Generates perfect response in user's language
    
    Args:
        user_message: User's question/message
        user_context: Optional context (previous location, user data)
        
    Returns:
        Dict with:
        - response: The AI response text
        - language: Detected language
        - location: extracted location name
        - name: extracted user name
        - needs_climate_data: bool
        - subscribe_intent: bool
    """
    
    # Quick pre-detection
    detected_language = detect_language_simple(user_message)
    potential_location = extract_location_keywords(user_message)
    potential_name = extract_name_keywords(user_message)
    
    # Build rich context for AI
    context_parts = []
    if user_context:
        # Extract user info for AI to use
        user_id = user_context.get('user_id')
        platform = user_context.get('platform', 'unknown')
        has_location = user_context.get('has_location', False)
        
        # Get user data from database to pass to AI
        try:
            from app.services.database import db_service
            if user_id:
                # Fetch full user data
                if platform == 'sms':
                    user_data = await db_service.get_user_by_phone(user_context.get('phone_number'))
                elif platform == 'telegram':
                    user_data = await db_service.get_user_by_telegram_id(user_context.get('user_id'))
                else:
                    user_data = None
                
                if user_data:
                    context_parts.append(f"User name: {user_data.get('name', 'Unknown')}")
                    context_parts.append(f"User location: {user_data.get('region', 'Not set')}")
                    context_parts.append(f"Subscribed: {user_data.get('subscribed', False)}")
        except Exception as e:
            logger.error(f"Could not fetch user context: {e}")
    
    context_info = "\n".join(context_parts) if context_parts else "New user, no history"
    
    # System prompt focused on LAND DEGRADATION, CONSERVATION & REHABILITATION
    system_prompt = f"""You are GreenPulse AI - Africa's leading land conservation and climate resilience assistant.

CORE MISSION:
Combat land degradation through education, awareness, and community engagement. Your purpose is to educate, alert, and inspire users across Kenya and Africa to conserve and rehabilitate land - promoting sustainable land use, soil protection, reforestation, and community-based environmental care.

PRIMARY FOCUS AREAS:

1. LAND DEGRADATION EDUCATION:
   - Explain causes: deforestation, overgrazing, poor farming practices, soil erosion, desertification
   - Teach rehabilitation methods: terracing, tree planting, mulching, organic farming, cover crops
   - Promote soil conservation: contour farming, agroforestry, composting, water harvesting
   - Share success stories of land restoration in Kenya and Africa

2. CONSERVATION MESSAGING:
   - Encourage communities to protect forests, rivers, wetlands, and soil
   - Integrate African environmental wisdom: "Mazinga yetu ni urithi wetu" (Our environment is our heritage)
   - Promote community-based environmental care and collective action
   - Emphasize: "Plant one tree, save your soil"
   - Local ownership and responsibility

3. PRACTICAL CLIMATE ALERTS WITH CONSERVATION ADVICE:
   - Provide real-time drought, flood, and erosion risk warnings
   - ALWAYS attach conservation advice to alerts
   - Example: "Heavy rain expected in Kitui - protect your topsoil by planting cover crops or building contour lines"
   - Connect weather events directly to land management actions
   - Make alerts actionable for land protection

4. TREE PLANTING & REHABILITATION INTEGRATION:
   - Promote tree planting drives, community nurseries, and soil restoration programs
   - Provide region-specific tree species suggestions that prevent erosion or restore fertility
   - Examples: Vetiver grass for slopes, Acacia for nitrogen fixation, indigenous trees for biodiversity
   - Encourage "Did You Know?" mini-lessons (e.g., "Did you know planting vetiver grass along slopes reduces soil erosion by 80%?")
   - Support community reforestation initiatives

TONE & APPROACH:
- Simple, hopeful, and practical language suitable for both web and SMS
- Mix English and Swahili naturally where appropriate (e.g., "Tuchunge mazingira yetu. Let's care for our land.")
- Be warm, encouraging, and action-oriented
- Focus on what users CAN DO, not just problems
- Celebrate small wins and community efforts

CRITICAL RESPONSE REQUIREMENTS:
- RESPOND WITHIN 10 SECONDS - keep answers concise and focused
- For SMS: Limit to 2-4 sentences for simple questions (100-200 words max)
- For complex questions: Provide key points only, avoid lengthy explanations
- Use bullet points for lists to save space
- NO emojis whatsoever
- Mobile-friendly formatting with short paragraphs
- If question is complex, give the most important info first
- User can always ask follow-up questions for more details

RESPONSE LENGTH GUIDE:
- Simple question (weather, crop): 2-3 sentences
- How-to question (planting, conservation): 4-5 bullet points
- Emergency/alert: Key action steps only
- Educational: Core concept + 1 example
- Remember: Fast, focused, actionable > long and detailed

USER CONTEXT:
{context_info}

CONVERSATION STYLE:
- Use user's name naturally when known
- Reference their specific location for localized advice
- Be encouraging about their conservation journey
- Provide region-specific tree species and techniques
- Connect every answer back to land conservation when relevant

Remember: Every interaction is an opportunity to inspire land conservation, soil protection, and environmental stewardship. Keep it FAST and FOCUSED - users appreciate quick, actionable advice over lengthy explanations."""

    try:
        # Single AI call that does everything
        response_text = await ai_service.chat_response_with_system(
            user_message=user_message,
            system_prompt=system_prompt,
            context=user_context
        )
        
        # Analyze what the user needs (for system integration)
        needs_location = potential_location is not None or any(
            word in user_message.lower() 
            for word in ['weather', 'forecast', 'hali ya hewa', 'climate', 'rain', 'mvua']
        )
        
        needs_climate = any(
            word in user_message.lower()
            for word in ['weather', 'climate', 'drought', 'flood', 'ukame', 'mafuriko', 'hali ya hewa']
        )
        
        wants_subscription = any(
            word in user_message.lower()
            for word in ['alert', 'subscribe', 'daily', 'notify', 'niambie', 'notification']
        )
        
        return {
            "response": response_text,
            "language": detected_language,
            "location": potential_location,
            "name": potential_name,
            "needs_location_data": needs_location,
            "needs_climate_data": needs_climate,
            "subscribe_intent": wants_subscription
        }
        
    except Exception as e:
        logger.error(f"Revolutionary response error: {e}")
        
        # Fallback response in detected language
        if detected_language == "swahili":
            fallback = "Samahani rafiki, nina shida kidogo sasa.\n\nTafadhali jaribu tena baada ya sekunde chache."
        else:
            fallback = "Sorry rafiki, I'm having a brief technical issue.\n\nPlease try again in a moment."
        
        return {
            "response": fallback,
            "language": detected_language,
            "location": None,
            "name": None,
            "needs_location_data": False,
            "needs_climate_data": False,
            "subscribe_intent": False
        }
