"""
AI Chat Route - Stateless Q&A endpoint using OpenRouter (GPT-5 mini)
No memory, no logging, just instant answers for farming questions
"""
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field
from typing import Optional
import os
from openai import OpenAI
from collections import defaultdict
from datetime import datetime, timedelta
import asyncio

router = APIRouter(prefix="/api/ai", tags=["AI Assistant"])

# Rate limiting: simple in-memory counter (IP-based)
rate_limit_store = defaultdict(list)
MAX_REQUESTS_PER_MINUTE = 10

# System prompt for GreenPulse AI - Land Conservation Focus
SYSTEM_PROMPT = """You are GreenPulse AI Assistant - Africa's land conservation and climate resilience expert.

CORE MISSION:
Combat land degradation through education, awareness, and community engagement. Educate, alert, and inspire users across Kenya and Africa to conserve and rehabilitate land.

YOUR FOCUS AREAS:
1. LAND DEGRADATION EDUCATION
   - Explain causes: deforestation, overgrazing, poor farming practices, soil erosion
   - Teach rehabilitation: terracing, tree planting, mulching, organic farming, cover crops
   - Promote soil conservation: contour farming, agroforestry, composting

2. CONSERVATION MESSAGING
   - Encourage protection of forests, rivers, and soil
   - Share African environmental wisdom: "Mazinga yetu ni urithi wetu" (Our environment is our heritage)
   - Promote community-based environmental care
   - Emphasize: "Plant one tree, save your soil"

3. PRACTICAL CLIMATE ADVICE
   - Provide drought, flood, and erosion warnings
   - ALWAYS attach conservation advice to climate information
   - Example: "Heavy rain expected - protect topsoil by planting cover crops or building contour lines"

4. TREE PLANTING & REHABILITATION
   - Recommend region-specific tree species that prevent erosion
   - Promote tree planting drives and community nurseries
   - Share success stories of land restoration

RESPONSE STYLE:
- Simple, hopeful, and practical language (suitable for SMS)
- Mix English and Swahili naturally: "Tuchunge mazingira yetu. Let's care for our land."
- Be concise: 2-4 sentences ideal, max 150 words
- NO emojis
- Focus on what people CAN DO
- Connect every answer to land protection when relevant

TOPICS YOU EXCEL AT:
- Soil conservation and erosion control
- Drought-resistant crops and water management
- Tree planting for land rehabilitation
- Climate-smart agriculture
- Community reforestation initiatives
- Sustainable land use practices
- Organic farming and composting

If asked about unrelated topics, politely redirect to land conservation, climate, or farming questions."""

class QuestionRequest(BaseModel):
    question: str = Field(..., min_length=3, max_length=500, description="User's question")

class AnswerResponse(BaseModel):
    answer: str
    model: str
    timestamp: str

def check_rate_limit(ip: str) -> bool:
    """Simple IP-based rate limiting"""
    now = datetime.now()
    cutoff = now - timedelta(minutes=1)
    
    # Clean old entries
    rate_limit_store[ip] = [ts for ts in rate_limit_store[ip] if ts > cutoff]
    
    # Check limit
    if len(rate_limit_store[ip]) >= MAX_REQUESTS_PER_MINUTE:
        return False
    
    # Add current request
    rate_limit_store[ip].append(now)
    return True

@router.post("/answer", response_model=AnswerResponse)
async def get_ai_answer(
    question_data: QuestionRequest,
    request: Request
):
    """
    Get an AI answer to a farming/climate question.
    Stateless - no chat history or memory.
    """
    # Rate limit check
    client_ip = request.client.host
    if not check_rate_limit(client_ip):
        raise HTTPException(
            status_code=429,
            detail="Too many requests. Please wait a minute before asking again."
        )
    
    # Validate question
    question = question_data.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    
    # Get OpenRouter credentials from env
    api_key = os.getenv("OPENROUTER_API_KEY")
    base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
    model = os.getenv("OPENROUTER_MODEL", "openai/gpt-5-mini")
    
    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="AI service not configured. Please contact support."
        )
    
    try:
        # Initialize OpenAI client with OpenRouter config
        client = OpenAI(
            api_key=api_key,
            base_url=base_url
        )
        
        # Call the model - no timeout, no token limit for complete answers
        response = await asyncio.to_thread(
            client.chat.completions.create,
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": question}
            ],
            # No max_tokens - AI provides complete answers naturally
            temperature=0.7,
        )
        
        answer = response.choices[0].message.content.strip()
        
        return AnswerResponse(
            answer=answer,
            model=model,
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        # Log error but don't expose internals
        print(f"AI Error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to get AI response. Please try again in a moment."
        )

@router.get("/status")
async def ai_status():
    """Check if AI service is configured and ready"""
    api_key = os.getenv("OPENROUTER_API_KEY")
    model = os.getenv("OPENROUTER_MODEL", "openai/gpt-5-mini")
    
    return {
        "status": "configured" if api_key else "not_configured",
        "model": model if api_key else None,
        "rate_limit": f"{MAX_REQUESTS_PER_MINUTE} requests/minute",
        "features": {
            "stateless": True,
            "no_memory": True,
            "agriculture_focused": True
        }
    }
