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
# ENDPOINTS
# ═══════════════════════════════════════════════════════════════════

@router.post("/answer")
async def get_ai_answer(question_data: QuestionRequest, request: Request):
    """
    [LEGACY] Simple Q&A endpoint - backwards compatible.
    For full features, use /intelligence endpoint.
    """
    client_ip = request.client.host
    if not check_rate_limit(client_ip):
        raise HTTPException(status_code=429, detail="Too many requests. Please wait a minute.")
    
    result = await greenpulse_ai.ask(
        question=question_data.question,
        mode="community",
        include_weather=False
    )
    
    if not result.get("success"):
        raise HTTPException(status_code=500, detail=result.get("error", "AI service error"))
    
    return {
        "answer": result["answer"],
        "model": result["model"],
        "timestamp": result["timestamp"]
    }


@router.post("/intelligence")
async def ask_intelligence(data: IntelligenceRequest, request: Request):
    """
    🧠 MAIN INTELLIGENCE ENDPOINT
    
    Ask GreenPulse AI anything about Kenya's environment.
    Automatically fetches real weather/climate data when location is provided.
    
    Capabilities:
    - Answer any environmental question
    - Provide location-specific insights with real data
    - Climate and weather interpretation
    - Regulatory guidance
    - Conservation advice
    
    Examples:
    - "What is the current weather in Nairobi and what does it mean for farming?"
    - "Is it safe to plant maize in Kitui right now?"
    - "What are the main environmental challenges in Mombasa?"
    """
    client_ip = request.client.host
    if not check_rate_limit(client_ip):
        raise HTTPException(status_code=429, detail="Too many requests. Please wait a minute.")
    
    result = await greenpulse_ai.ask(
        question=data.question,
        mode=data.mode,
        location=data.location,
        include_weather=data.include_weather
    )
    
    if not result.get("success"):
        raise HTTPException(status_code=500, detail=result.get("error", "AI service error"))
    
    return result


@router.post("/decision-analysis")
async def analyze_decision(data: DecisionRequest, request: Request):
    """
    🎯 DECISION INTELLIGENCE
    
    Analyze proposed actions BEFORE they happen.
    Answer "what-if" questions with data-backed predictions.
    
    Examples:
    - "If we expand our factory production by 30%, what are the environmental impacts?"
    - "If we clear 10 hectares of forest for farming in Nyandarua, what happens?"
    - "What if we stop using fertilizers on our Nakuru farm?"
    """
    client_ip = request.client.host
    if not check_rate_limit(client_ip):
        raise HTTPException(status_code=429, detail="Too many requests. Please wait a minute.")
    
    question = f"""DECISION ANALYSIS REQUEST

Analyze this proposed action and predict environmental consequences:

PROPOSED SCENARIO:
{data.scenario}

LOCATION: {data.location}, Kenya

Please provide:
1. Environmental Impact Assessment (positive and negative)
2. Risk Scores (Land Degradation, Water Stress, Emissions, Compliance)
3. Timeline of likely impacts (immediate, 1 year, 5 years)
4. Alternative approaches to reduce negative impacts
5. Recommended mitigation measures"""

    result = await greenpulse_ai.ask(
        question=question,
        mode=data.mode,
        location=data.location,
        include_weather=True
    )
    
    if not result.get("success"):
        raise HTTPException(status_code=500, detail=result.get("error", "AI service error"))
    
    return {
        "analysis_type": "decision_intelligence",
        "scenario": data.scenario,
        "location": data.location,
        **result
    }


@router.post("/risk-assessment")
async def assess_environmental_risk(data: RiskAssessmentRequest, request: Request):
    """
    📊 ENVIRONMENTAL RISK SCORING
    
    Get clear risk scores for any Kenya location.
    Uses real weather and climate data.
    
    Returns scores for:
    - Land Degradation Risk
    - Water Stress Score
    - Climate Vulnerability
    - Drought/Flood Risk
    - Activity-specific risks
    """
    client_ip = request.client.host
    if not check_rate_limit(client_ip):
        raise HTTPException(status_code=429, detail="Too many requests. Please wait a minute.")
    
    activity_context = f"\nSPECIFIC ACTIVITY: {data.activity}" if data.activity else ""
    
    question = f"""ENVIRONMENTAL RISK ASSESSMENT REQUEST

Provide a comprehensive risk assessment for this location:{activity_context}

Please provide clear risk scores (LOW / MEDIUM / HIGH / CRITICAL) for:
1. Land Degradation Risk - soil erosion, fertility loss
2. Water Stress Score - availability and quality
3. Climate Vulnerability Score - exposure to climate extremes
4. Drought Risk - based on current and historical data
5. Flood Risk - based on terrain and rainfall patterns
{"6. " + data.activity.title() + " Risk - specific to this activity" if data.activity else ""}

For each score, provide:
- The rating (LOW/MEDIUM/HIGH/CRITICAL)
- Brief explanation (1-2 sentences)
- Key mitigation recommendation

End with an OVERALL RISK SUMMARY."""

    result = await greenpulse_ai.ask(
        question=question,
        mode=data.mode,
        location=data.location,
        include_weather=True
    )
    
    if not result.get("success"):
        raise HTTPException(status_code=500, detail=result.get("error", "AI service error"))
    
    return {
        "analysis_type": "risk_assessment",
        "location": data.location,
        "activity": data.activity,
        **result
    }


@router.post("/compliance-check")
async def check_compliance(data: ComplianceRequest, request: Request):
    """
    📋 REGULATORY & COMPLIANCE INTELLIGENCE
    
    Check if an activity complies with Kenyan environmental regulations.
    References NEMA, EMCA, and relevant laws.
    
    NOTE: Advisory only, not legal authority.
    """
    client_ip = request.client.host
    if not check_rate_limit(client_ip):
        raise HTTPException(status_code=429, detail="Too many requests. Please wait a minute.")
    
    location_context = f" in {data.location}, Kenya" if data.location else " in Kenya"
    
    question = f"""REGULATORY COMPLIANCE CHECK

Analyze this activity for environmental compliance{location_context}:

ACTIVITY DESCRIPTION:
{data.activity}

Please provide:
1. RELEVANT REGULATIONS
   - Identify applicable Kenyan laws (EMCA, NEMA requirements, Water Act, Forest Act, etc.)
   - List specific permits or licenses that may be required

2. COMPLIANCE ASSESSMENT
   - Potential compliance issues or gaps
   - Areas of concern
   - Compliance Risk Rating: LOW / MEDIUM / HIGH / CRITICAL

3. CONSEQUENCES OF NON-COMPLIANCE
   - Potential penalties (fines, closure orders, legal action)
   - Reputational and operational risks

4. CORRECTIVE ACTIONS
   - Steps to achieve or maintain compliance
   - Timeline recommendations

5. DOCUMENTATION NEEDED
   - Required reports, assessments, or permits

DISCLAIMER: This is advisory guidance only, not legal advice. Consult NEMA or a qualified environmental lawyer for definitive compliance requirements."""

    result = await greenpulse_ai.ask(
        question=question,
        mode=data.mode,
        location=data.location if data.location else None,
        include_weather=False
    )
    
    if not result.get("success"):
        raise HTTPException(status_code=500, detail=result.get("error", "AI service error"))
    
    return {
        "analysis_type": "compliance_check",
        "activity": data.activity,
        "location": data.location,
        "disclaimer": "Advisory guidance only. Consult NEMA or qualified legal counsel for binding compliance requirements.",
        **result
    }


@router.post("/energy-advice")
async def get_energy_advice(data: EnergyAdviceRequest, request: Request):
    """
    ⚡ ALTERNATIVE ENERGY & EFFICIENCY ADVISOR
    
    Get recommendations for renewable energy and efficiency improvements.
    Tailored to Kenya's energy landscape.
    """
    client_ip = request.client.host
    if not check_rate_limit(client_ip):
        raise HTTPException(status_code=429, detail="Too many requests. Please wait a minute.")
    
    location_context = f" in {data.location}, Kenya" if data.location else " in Kenya"
    
    question = f"""ENERGY TRANSITION ANALYSIS

Analyze energy usage and recommend alternatives{location_context}:

CURRENT ENERGY SITUATION:
{data.current_energy}

BUDGET LEVEL: {data.budget_level.upper()}

Please provide:
1. CURRENT SITUATION ASSESSMENT
   - Estimated emissions/environmental impact
   - Cost and efficiency analysis

2. RENEWABLE ALTERNATIVES (suited for Kenya)
   - Solar potential and options
   - Wind possibilities (if applicable to location)
   - Biomass/biogas options
   - Geothermal (if in Rift Valley region)
   - Small hydro (if near water sources)

3. COMPARISON TABLE
   - Option | Initial Cost | Savings | Emissions Reduction | Payback Period

4. RECOMMENDED TRANSITION PLAN
   - Phase 1: Quick wins (immediate)
   - Phase 2: Medium-term upgrades (1-2 years)
   - Phase 3: Full transition (3-5 years)

5. AVAILABLE INCENTIVES
   - Kenya government programs
   - International climate finance
   - Tax benefits

6. EFFICIENCY IMPROVEMENTS
   - Low-cost efficiency measures
   - Behavioral changes"""

    result = await greenpulse_ai.ask(
        question=question,
        mode=data.mode,
        location=data.location if data.location else None,
        include_weather=True
    )
    
    if not result.get("success"):
        raise HTTPException(status_code=500, detail=result.get("error", "AI service error"))
    
    return {
        "analysis_type": "energy_advice",
        "current_energy": data.current_energy,
        "location": data.location,
        "budget_level": data.budget_level,
        **result
    }


@router.post("/future-scenario")
async def project_future_scenario(data: FutureScenarioRequest, request: Request):
    """
    🔮 ENVIRONMENTAL FUTURE SCENARIOS
    
    Predict land/environmental conditions 5-10+ years ahead.
    Show effects of action vs inaction.
    """
    client_ip = request.client.host
    if not check_rate_limit(client_ip):
        raise HTTPException(status_code=429, detail="Too many requests. Please wait a minute.")
    
    situation_context = f"\nCURRENT SITUATION: {data.current_situation}" if data.current_situation else ""
    action_context = f"\nPROPOSED ACTION: {data.proposed_action}" if data.proposed_action else ""
    
    question = f"""ENVIRONMENTAL FUTURE SCENARIO PROJECTION

Project environmental conditions {data.years} years into the future for this location:{situation_context}{action_context}

Please provide:
1. BASELINE PROJECTION (No action / status quo)
   - Land condition in {data.years} years
   - Water availability
   - Soil quality
   - Biodiversity outlook
   - Climate vulnerability

2. {"ACTION SCENARIO (" + data.proposed_action[:50] + "...)" if data.proposed_action else "POSITIVE ACTION SCENARIO"}
   - Projected outcomes with mitigation/action
   - Improvements vs baseline
   - Investment vs returns

3. COMPARISON: Action vs Inaction
   - Key metrics comparison table
   - Economic implications
   - Social/community impacts

4. IRREVERSIBLE RISKS
   - What damage cannot be undone?
   - Critical thresholds and tipping points

5. RECOMMENDED PATH
   - Optimal actions for best outcome
   - Timeline and milestones

6. CONFIDENCE LEVEL
   - Explain assumptions and uncertainties
   - Data sources and reliability

Note: These are projections based on climate models and regional patterns. Actual outcomes depend on many factors."""

    result = await greenpulse_ai.ask(
        question=question,
        mode=data.mode,
        location=data.location,
        include_weather=True
    )
    
    if not result.get("success"):
        raise HTTPException(status_code=500, detail=result.get("error", "AI service error"))
    
    return {
        "analysis_type": "future_scenario",
        "location": data.location,
        "projection_years": data.years,
        "current_situation": data.current_situation,
        "proposed_action": data.proposed_action,
        **result
    }


@router.post("/analyze-document")
async def analyze_document(
    request: Request,
    file: UploadFile = File(...),
    question: Optional[str] = Form(None),
    mode: str = Form("professional")
):
    """
    📄 DOCUMENT & REPORT ANALYSIS
    
    Upload environmental reports, EIAs, ESG documents, or monitoring data.
    Get comprehensive analysis including:
    - Key metrics extraction
    - Compliance assessment
    - Risk identification
    - Recommendations
    
    Supports: PDF, TXT, MD, CSV, JSON
    Max size: 10MB
    """
    client_ip = request.client.host
    if not check_rate_limit(client_ip):
        raise HTTPException(status_code=429, detail="Too many requests. Please wait a minute.")
    
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    
    file_content = await file.read()
    
    if len(file_content) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File too large. Maximum size is 10MB.")
    
    extracted_text = extract_text_from_file(file_content, file.filename)
    
    if not extracted_text or len(extracted_text) < 50:
        raise HTTPException(
            status_code=400, 
            detail="Could not extract sufficient text from the document."
        )
    
    # Build analysis prompt
    if question:
        analysis_question = f"""Analyze this document and answer the following question:

QUESTION: {question}

After answering the specific question, also provide:
1. Document Summary
2. Key Metrics Extracted
3. Compliance/Risk Issues Identified
4. Recommendations"""
    else:
        analysis_question = """Provide a comprehensive analysis of this environmental document:

1. DOCUMENT SUMMARY
   - Document type and purpose
   - Key entities mentioned
   - Date/period covered

2. KEY METRICS EXTRACTED
   - Emissions data (if present)
   - Land use figures
   - Water usage
   - Energy consumption
   - Any quantitative data

3. ENVIRONMENTAL IMPACT ASSESSMENT
   - Identified impacts (positive and negative)
   - Affected areas or ecosystems
   - Duration and severity of impacts

4. COMPLIANCE ASSESSMENT
   - Referenced regulations or standards
   - Compliance status indicators
   - Gaps or issues identified

5. RISK ANALYSIS
   - Environmental risks
   - Operational risks
   - Compliance risks
   - Risk ratings where possible

6. OPPORTUNITIES
   - Improvement opportunities
   - Cost savings potential
   - Sustainability wins

7. RECOMMENDATIONS
   - Immediate actions needed
   - Medium-term improvements
   - Long-term strategy suggestions

8. DATA QUALITY NOTE
   - What information is missing?
   - Limitations of this analysis"""
    
    result = await greenpulse_ai.ask(
        question=analysis_question,
        mode=mode if mode in ["community", "professional"] else "professional",
        document_content=extracted_text
    )
    
    if not result.get("success"):
        raise HTTPException(status_code=500, detail=result.get("error", "AI service error"))
    
    return {
        "analysis_type": "document_analysis",
        "filename": file.filename,
        "file_size_kb": round(len(file_content) / 1024, 1),
        "text_extracted_chars": len(extracted_text),
        "user_question": question,
        **result
    }


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
    """Check AI service status and available capabilities"""
    import os
    api_key = os.getenv("OPENROUTER_API_KEY")
    model = os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-2024-11-20")
    
    return {
        "status": "operational" if api_key else "not_configured",
        "model": model if api_key else None,
        "version": "2.0.0",
        "name": "GreenPulse Environmental Intelligence",
        "rate_limit": f"{MAX_REQUESTS_PER_MINUTE} requests/minute",
        "capabilities": {
            "intelligence": "General environmental Q&A with real data",
            "decision_analysis": "What-if scenario analysis",
            "risk_assessment": "Environmental risk scoring",
            "compliance_check": "Kenyan regulation guidance",
            "energy_advice": "Renewable energy recommendations",
            "future_scenarios": "5-10 year projections",
            "document_analysis": "Environmental report analysis",
            "chat": "Unified chat with optional file upload"
        },
        "data_sources": {
            "weather": "Google Weather API (real-time)",
            "climate": "NASA POWER (30-day historical)",
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
    List all GreenPulse AI capabilities with descriptions.
    Useful for frontend to show available features.
    """
    return {
        "name": "GreenPulse Environmental Intelligence",
        "tagline": "Kenya's AI-Powered Environmental Decision Support System",
        "capabilities": [
            {
                "id": "intelligence",
                "name": "Environmental Intelligence",
                "endpoint": "/api/ai/intelligence",
                "method": "POST",
                "description": "Ask any environmental question about Kenya. Get answers backed by real weather and climate data.",
                "example": "What's the current drought risk in Turkana?"
            },
            {
                "id": "decision_analysis",
                "name": "Decision Intelligence",
                "endpoint": "/api/ai/decision-analysis",
                "method": "POST",
                "description": "Analyze proposed actions before they happen. Get environmental impact predictions.",
                "example": "If we convert 50 hectares of forest to farmland in Nyandarua, what are the consequences?"
            },
            {
                "id": "risk_assessment",
                "name": "Environmental Risk Scoring",
                "endpoint": "/api/ai/risk-assessment",
                "method": "POST",
                "description": "Get clear risk scores (LOW/MEDIUM/HIGH/CRITICAL) for any Kenya location.",
                "example": "Assess environmental risks for manufacturing in Athi River"
            },
            {
                "id": "compliance_check",
                "name": "Regulatory Compliance",
                "endpoint": "/api/ai/compliance-check",
                "method": "POST",
                "description": "Check if activities comply with Kenyan environmental regulations (NEMA, EMCA).",
                "example": "What permits do I need to start a quarry in Machakos?"
            },
            {
                "id": "energy_advice",
                "name": "Energy Transition Advisor",
                "endpoint": "/api/ai/energy-advice",
                "method": "POST",
                "description": "Get renewable energy recommendations tailored to Kenya's energy landscape.",
                "example": "Help me transition my diesel-powered factory to renewables"
            },
            {
                "id": "future_scenarios",
                "name": "Future Projections",
                "endpoint": "/api/ai/future-scenario",
                "method": "POST",
                "description": "Predict environmental conditions 5-10 years ahead. Compare action vs inaction.",
                "example": "What will Laikipia's grasslands look like in 10 years without conservation?"
            },
            {
                "id": "document_analysis",
                "name": "Report Analysis",
                "endpoint": "/api/ai/analyze-document",
                "method": "POST",
                "description": "Upload environmental reports and get comprehensive analysis with compliance review.",
                "example": "Analyze this EIA report for compliance issues"
            },
            {
                "id": "chat",
                "name": "Unified Chat",
                "endpoint": "/api/ai/chat",
                "method": "POST",
                "description": "Single endpoint for questions, location context, and optional file upload.",
                "example": "Perfect for frontend chat interfaces"
            }
        ],
        "response_modes": {
            "community": "Simple, hopeful, practical language with Swahili mix. Best for farmers and communities.",
            "professional": "Formal, structured, data-driven. Best for businesses and reports."
        }
    }
