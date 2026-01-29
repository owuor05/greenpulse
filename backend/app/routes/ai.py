"""
GreenPulse AI Routes - Complete Environmental Intelligence API
Uses the GreenPulse AI Intelligence Service for all capabilities
"""
from fastapi import APIRouter, HTTPException, Request, UploadFile, File, Form
from pydantic import BaseModel, Field
from typing import Optional, Literal
from collections import defaultdict
from datetime import datetime, timedelta
import asyncio
import io

# PDF extraction
try:
    from PyPDF2 import PdfReader
    PDF_SUPPORT = True
except ImportError:
    PDF_SUPPORT = False

# Import our intelligent AI service
from app.services.ai_intelligence import greenpulse_ai

router = APIRouter(prefix="/api/ai", tags=["AI Intelligence"])

# Rate limiting: simple in-memory counter (IP-based)
rate_limit_store = defaultdict(list)
MAX_REQUESTS_PER_MINUTE = 20  # Increased for power users


def check_rate_limit(ip: str) -> bool:
    """Simple IP-based rate limiting"""
    now = datetime.now()
    cutoff = now - timedelta(minutes=1)
    rate_limit_store[ip] = [ts for ts in rate_limit_store[ip] if ts > cutoff]
    if len(rate_limit_store[ip]) >= MAX_REQUESTS_PER_MINUTE:
        return False
    rate_limit_store[ip].append(now)
    return True


def extract_text_from_pdf(file_content: bytes) -> str:
    """Extract text from PDF file"""
    if not PDF_SUPPORT:
        raise HTTPException(status_code=500, detail="PDF support not available")
    try:
        pdf_reader = PdfReader(io.BytesIO(file_content))
        text = ""
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text.strip()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to extract text from PDF: {str(e)}")


def extract_text_from_file(file_content: bytes, filename: str) -> str:
    """Extract text from uploaded file based on type"""
    filename_lower = filename.lower()
    if filename_lower.endswith('.pdf'):
        return extract_text_from_pdf(file_content)
    elif filename_lower.endswith(('.txt', '.md', '.csv', '.json')):
        try:
            return file_content.decode('utf-8')
        except UnicodeDecodeError:
            return file_content.decode('latin-1')
    else:
        raise HTTPException(
            status_code=400, 
            detail="Unsupported file type. Supported: PDF, TXT, MD, CSV, JSON"
        )


# ═══════════════════════════════════════════════════════════════════
# REQUEST/RESPONSE MODELS
# ═══════════════════════════════════════════════════════════════════

class QuestionRequest(BaseModel):
    """Simple question request (backwards compatible)"""
    question: str = Field(..., min_length=3, max_length=2000)


class IntelligenceRequest(BaseModel):
    """Full-featured intelligence request"""
    question: str = Field(..., min_length=3, max_length=5000, description="Your question or scenario")
    location: Optional[str] = Field(None, description="Kenya location for context (e.g., 'Nairobi', 'Mombasa', 'Kitui')")
    mode: Literal["community", "professional"] = Field("community", description="Response style")
    include_weather: bool = Field(True, description="Include real-time weather/climate data")


class DecisionRequest(BaseModel):
    """Decision analysis request - What-if scenarios"""
    scenario: str = Field(..., min_length=10, max_length=5000, description="Describe the proposed action or scenario")
    location: str = Field(..., description="Kenya location where action would take place")
    mode: Literal["community", "professional"] = Field("professional", description="Response style")


class RiskAssessmentRequest(BaseModel):
    """Environmental risk scoring request"""
    location: str = Field(..., description="Kenya location to assess")
    activity: Optional[str] = Field(None, description="Specific activity or industry (e.g., 'farming', 'manufacturing', 'construction')")
    mode: Literal["community", "professional"] = Field("professional", description="Response style")


class ComplianceRequest(BaseModel):
    """Regulatory compliance check request"""
    activity: str = Field(..., description="Describe the business activity or operation")
    location: Optional[str] = Field(None, description="Kenya location")
    mode: Literal["community", "professional"] = Field("professional", description="Response style")


class EnergyAdviceRequest(BaseModel):
    """Energy transition and alternatives request"""
    current_energy: str = Field(..., description="Current energy source and usage description")
    location: Optional[str] = Field(None, description="Kenya location for renewable potential")
    budget_level: Literal["low", "medium", "high"] = Field("medium", description="Budget consideration")
    mode: Literal["community", "professional"] = Field("professional", description="Response style")


class FutureScenarioRequest(BaseModel):
    """Future projection request - 5-10 year outlook"""
    location: str = Field(..., description="Kenya location")
    current_situation: Optional[str] = Field(None, description="Current land use or environmental situation")
    proposed_action: Optional[str] = Field(None, description="What action (or inaction) to project")
    years: int = Field(5, ge=1, le=20, description="Years into the future")
    mode: Literal["community", "professional"] = Field("professional", description="Response style")


# ═══════════════════════════════════════════════════════════════════
# UNIFIED SMART ENDPOINT
# ═══════════════════════════════════════════════════════════════════

@router.post("/ask")
async def unified_ai_ask(
    request: Request,
    question: str = Form(...),
    location: Optional[str] = Form(None),
    mode: str = Form("community"),
    file: Optional[UploadFile] = File(None)
):
    """
    🤖 UNIFIED GREENPULSE AI ENDPOINT
    
    ONE endpoint that does EVERYTHING:
    - Simple questions: "What's the weather in Nairobi?"
    - Document analysis: Upload PDF + ask "What are the main risks?"
    - Location-aware: Automatically gets real weather/climate data
    - Risk assessment: "Environmental risks for my factory in Mombasa?"
    - Compliance: "What permits do I need for quarrying in Machakos?"
    - Energy advice: "Help me switch to solar power"
    - Future scenarios: "What will Turkana look like in 10 years?"
    - Any environmental question about Kenya
    
    The AI automatically detects what you need and provides the right analysis.
    
    Parameters:
    - question: Your question (required)
    - location: Kenya location for context (optional)
    - mode: "community" (simple) or "professional" (formal) 
    - file: Upload document for analysis (optional, max 10MB)
    
    Supported files: PDF, TXT, MD, CSV, JSON
    """
    client_ip = request.client.host
    if not check_rate_limit(client_ip):
        raise HTTPException(status_code=429, detail="Too many requests. Please wait a minute.")
    
    document_content = None
    file_info = None
    
    # Handle optional file upload
    if file and file.filename:
        try:
            file_content = await file.read()
            if len(file_content) > 10 * 1024 * 1024:  # 10MB limit
                raise HTTPException(status_code=400, detail="File too large. Maximum 10MB.")
            
            document_content = extract_text_from_file(file_content, file.filename)
            file_info = {
                "filename": file.filename,
                "size_kb": round(len(file_content) / 1024, 1),
                "chars_extracted": len(document_content) if document_content else 0
            }
        except HTTPException:
            raise  # Re-raise HTTP exceptions
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"File processing error: {str(e)}")
    
    # Validate mode
    if mode not in ["community", "professional"]:
        mode = "community"
    
    # Call the unified GreenPulse AI
    result = await greenpulse_ai.ask(
        question=question,
        mode=mode,
        location=location,
        document_content=document_content,
        include_weather=location is not None  # Auto-include weather if location provided
    )
    
    if not result.get("success"):
        raise HTTPException(status_code=500, detail=result.get("error", "AI service error"))
    
    # Add file info if a file was analyzed
    response = {**result}
    if file_info:
        response["file_analyzed"] = file_info
    
    return response


# ═══════════════════════════════════════════════════════════════════
# LEGACY ENDPOINTS (Removed - Use /ask instead)
# ═══════════════════════════════════════════════════════════════════
# 
# All specific endpoints have been consolidated into the smart /ask endpoint:
# - /intelligence → Use /ask with location parameter
# - /decision-analysis → Use /ask with "analyze this scenario:" question
# - /risk-assessment → Use /ask with "assess risks for:" question  
# - /compliance-check → Use /ask with "what permits/compliance for:" question
# - /energy-advice → Use /ask with "energy recommendations for:" question
# - /future-scenario → Use /ask with "predict future scenario:" question
# - /analyze-document → Use /ask with file upload
#
# The AI automatically detects what you need - no need for separate endpoints!
# ═══════════════════════════════════════════════════════════════════


@router.post("/chat")
async def chat_with_context(
    request: Request,
    question: str = Form(...),
    location: Optional[str] = Form(None),
    mode: str = Form("community"),
    file: Optional[UploadFile] = File(None)
):
    """
    💬 UNIFIED CHAT ENDPOINT
    
    Single endpoint that handles:
    - Simple questions
    - Location-based queries
    - Document analysis
    - All in one request
    
    Perfect for frontend integration.
    """
    client_ip = request.client.host
    if not check_rate_limit(client_ip):
        raise HTTPException(status_code=429, detail="Too many requests. Please wait a minute.")
    
    document_content = None
    file_info = None
    
    # Handle optional file
    if file and file.filename:
        file_content = await file.read()
        if len(file_content) > 10 * 1024 * 1024:
            raise HTTPException(status_code=400, detail="File too large. Maximum 10MB.")
        document_content = extract_text_from_file(file_content, file.filename)
        file_info = {
            "filename": file.filename,
            "size_kb": round(len(file_content) / 1024, 1),
            "chars_extracted": len(document_content)
        }
    
    result = await greenpulse_ai.ask(
        question=question,
        mode=mode if mode in ["community", "professional"] else "community",
        location=location,
        document_content=document_content,
        include_weather=location is not None
    )
    
    if not result.get("success"):
        raise HTTPException(status_code=500, detail=result.get("error", "AI service error"))
    
    response = {**result}
    if file_info:
        response["file_analyzed"] = file_info
    
    return response


@router.get("/status")
async def ai_status():
    """Check AI service status - simplified unified API"""
    import os
    api_key = os.getenv("OPENROUTER_API_KEY")
    model = os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-2024-11-20")
    
    return {
        "status": "operational" if api_key else "not_configured",
        "model": model if api_key else None,
        "version": "3.0.0",
        "name": "GreenPulse Environmental Intelligence",
        "api_design": "Simplified - ONE smart endpoint handles everything",
        "rate_limit": f"{MAX_REQUESTS_PER_MINUTE} requests/minute",
        "main_endpoint": "/api/ai/ask",
        "capabilities": "All environmental analysis via natural language - the AI detects what you need automatically",
        "features": [
            "Environmental Q&A with real weather data",
            "Document analysis (PDF, TXT, MD, CSV, JSON)", 
            "Risk assessment and compliance guidance",
            "Energy transition recommendations",
            "Future scenario projections",
            "Location-aware responses for Kenya",
            "Both community and professional response modes"
        ],
        "data_sources": {
            "weather": "Google Weather API (real-time + 7-day forecast)",
            "climate": "NASA POWER (30-day historical trends)",
            "geocoding": "Google Maps Geocoding"
        },
        "response_modes": ["community", "professional"],
        "supported_files": ["PDF", "TXT", "MD", "CSV", "JSON"],
        "max_file_size_mb": 10,
        "pdf_support": PDF_SUPPORT,
        "region_focus": "Kenya"
    }


@router.get("/capabilities")
async def list_capabilities():
    """
    GreenPulse AI capabilities - now simplified to ONE smart endpoint.
    """
    return {
        "name": "GreenPulse Environmental Intelligence",
        "tagline": "Kenya's AI-Powered Environmental Decision Support System",
        "api_philosophy": "ONE endpoint does everything - the AI is smart enough to understand what you need",
        "main_endpoint": {
            "url": "/api/ai/ask",
            "method": "POST",
            "description": "Send any environmental question, with optional file upload and location context. The AI automatically detects and handles all types of analysis.",
            "parameters": {
                "question": "Your question (required) - can be simple or complex",
                "location": "Kenya location for context (optional)",
                "mode": "community or professional response style (optional)",
                "file": "Upload document for analysis (optional, max 10MB)"
            }
        },
        "what_it_handles": [
            "Weather & climate questions - 'What's the weather in Nairobi?'",
            "Risk assessment - 'Environmental risks for my factory in Mombasa?'", 
            "Decision analysis - 'Should I plant maize in Kitui right now?'",
            "Compliance guidance - 'What permits do I need for quarrying?'",
            "Energy advice - 'Help me switch to solar power'",
            "Future scenarios - 'What will Turkana look like in 10 years?'",
            "Document analysis - Upload any PDF + ask questions about it",
            "Location-specific advice - Automatically gets real weather/climate data",
            "Any environmental question about Kenya"
        ],
        "smart_features": [
            "Language detection - responds in the same language you write",
            "Auto-context - fetches weather data when you mention locations", 
            "File analysis - upload PDFs, get comprehensive environmental analysis",
            "Risk scoring - automatically provides LOW/MEDIUM/HIGH/CRITICAL ratings",
            "Regulation awareness - knows Kenyan environmental laws (NEMA, EMCA)",
            "Data integration - combines Google Weather + NASA climate data",
            "Dual modes - community (simple) or professional (formal) responses"
        ],
        "legacy_note": "All specific endpoints (/intelligence, /decision-analysis, etc.) have been consolidated into /ask for simplicity",
        "response_modes": {
            "community": "Simple, clear language matching your language (English if you write English, Swahili if you write Swahili)",
            "professional": "Formal, structured, data-driven responses for business and reports"
        },
        "supported_files": ["PDF", "TXT", "MD", "CSV", "JSON"],
        "max_file_size": "10MB",
        "region_focus": "Kenya (counties, climate zones, regulations)"
    }
