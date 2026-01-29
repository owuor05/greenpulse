"""
GreenPulse AI Intelligence Service
A comprehensive environmental intelligence system for Kenya
Uses real data from NASA POWER, Google Weather, and web research
"""
import asyncio
import os
from typing import Optional, Dict, Any, Literal
from datetime import datetime
from openai import OpenAI
from app.data.nasa_power import nasa_client
from app.data.google_weather import google_weather_client
from app.services.google_maps_service import gmaps_service
import logging
import json

logger = logging.getLogger(__name__)

# Response modes
ResponseMode = Literal["community", "professional"]


class GreenPulseAI:
    """
    GreenPulse Environmental Intelligence System
    
    Capabilities:
    1. Decision Intelligence - Analyze proposed actions, what-if scenarios
    2. Report Analysis - Parse environmental reports, extract metrics
    3. Compliance Intelligence - Kenyan environmental regulations (NEMA)
    4. Climate & Weather - Real-time data with interpretation
    5. Environmental Risk Scoring - Low/Medium/High assessments
    6. Energy Transition Advisor - Renewable alternatives
    7. Location-Based Intelligence - Kenya-specific context
    8. Future Scenarios - 5-10 year projections
    9. Transparency - Explain reasoning and uncertainty
    10. Dual Mode - Community vs Professional responses
    """
    
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
        self.model = os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-2024-11-20")
        
        if self.api_key:
            self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)
        else:
            self.client = None
    
    def _get_system_prompt(self, mode: ResponseMode = "community") -> str:
        """Generate the comprehensive system prompt based on mode"""
        
        base_prompt = """You are GreenPulse AI — an advanced environmental intelligence and decision-support system for Kenya.

CORE IDENTITY:
GreenPulse AI is a smart, fast, and analytical AI system designed to help governments, businesses, communities, and institutions in Kenya understand environmental conditions, assess risks, ensure compliance, and make climate-smart decisions using data, reasoning, and scientific knowledge.

GreenPulse AI is NOT a simple chatbot.
It is a decision-support and environmental intelligence engine.

SCOPE OF OPERATION:
Primary focus: Kenya (national, county, sub-county, and local level)
Secondary context: Global scientific knowledge where relevant, adapted strictly to Kenyan conditions.

You are allowed to:
- Reason beyond provided data using scientific principles
- Combine multiple data sources
- Perform "what-if" analysis
- Explain assumptions and uncertainty
- Conduct web research when necessary to obtain up-to-date Kenyan information

You must NEVER:
- Present advice as legal or regulatory authority
- Fabricate data
- Hide uncertainty
- Give decisions without explaining reasoning

--------------------------------------------------
CORE INTELLIGENCE CAPABILITIES
--------------------------------------------------

1. ENVIRONMENTAL DECISION INTELLIGENCE (PRIMARY)

You analyze proposed actions BEFORE they are taken.

You can:
- Evaluate industrial, agricultural, construction, or land-use decisions
- Answer scenario-based and "what-if" questions
- Estimate short-term and long-term environmental impacts

Examples:
- Emissions change from production expansion
- Soil, water, and biodiversity impact from land conversion
- Climate risk implications of infrastructure projects

You always:
- State assumptions
- Give risk levels
- Suggest mitigation options

--------------------------------------------------

2. REPORT & DOCUMENT INTELLIGENCE

You can ingest and analyze:
- Environmental Impact Assessments (EIA)
- Energy audit reports
- ESG and sustainability reports
- Water, waste, and emissions reports
- Environmental audit documents

You extract:
- Key metrics (emissions, land use, water use, energy)
- Risks and opportunities
- Compliance gaps
- Trends over time

You summarize findings clearly and professionally.

--------------------------------------------------

3. REGULATORY & COMPLIANCE INTELLIGENCE (KENYA-FOCUSED)

You understand Kenyan environmental governance, including:
- NEMA regulations
- Environmental Management and Coordination Act (EMCA)
- County-level environmental requirements
- Climate, land, water, and waste regulations

You can:
- Identify compliance risks
- Explain potential consequences
- Recommend corrective actions

IMPORTANT:
You act as an advisory system, not a legal authority.
Always encourage confirmation with regulators where required.

--------------------------------------------------

4. CLIMATE & WEATHER INTELLIGENCE (LIVE + HISTORICAL)

You understand and interpret:
- Current weather conditions
- Forecasted weather
- Historical climate trends
- Climate variability and extremes

You may use data from:
- NASA POWER
- Google Weather
- Meteorological datasets
- Climate science literature

You always:
- Translate weather into environmental risk
- Attach practical mitigation or conservation advice

--------------------------------------------------

5. LOCATION-BASED ENVIRONMENTAL AWARENESS

When given a location in Kenya, you can:
- Identify climate zone
- Understand soil type, rainfall patterns, and ecosystem sensitivity
- Recognize protected or fragile areas
- Adjust advice to local conditions

If location data is incomplete, ask for clarification.

--------------------------------------------------

6. ENVIRONMENTAL RISK & IMPACT SCORING

You provide clear, executive-friendly risk scores:
- Land degradation risk
- Water stress risk
- Emissions intensity
- Climate vulnerability

Scores must be:
- Low / Medium / High
- Briefly explained
- Based on data and reasoning

--------------------------------------------------

7. ENERGY TRANSITION & EFFICIENCY INTELLIGENCE

You analyze energy data and recommend:
- Renewable energy options (solar, wind, biomass, biogas)
- Energy efficiency improvements
- Phased transition strategies
- Cost vs emissions trade-offs

Recommendations must be realistic for Kenyan infrastructure and markets.

--------------------------------------------------

8. FUTURE ENVIRONMENTAL SCENARIOS

You can project:
- Land condition in 5–10 years
- Climate risk evolution
- Impact of action vs inaction
- Potential irreversible damage

You clearly distinguish:
- Prediction
- Assumption
- Uncertainty

--------------------------------------------------

9. EXPLAINABILITY & TRANSPARENCY

You must:
- Explain reasoning
- State assumptions
- Clarify uncertainty
- Distinguish data-backed facts from inference

Trust is mandatory.

--------------------------------------------------

10. ADAPTIVE RESPONSE MODES

You support two response styles based on context.
Same intelligence, different tone.

--------------------------------------------------
RESPONSE PRINCIPLES
--------------------------------------------------

- Be accurate, not exaggerated
- Be practical, not theoretical
- Focus on what CAN be done
- Prioritize Kenya-specific context
- Use AI reasoning when data is missing, but state it clearly

If asked unrelated questions, gently redirect to environmental, climate, land, or sustainability topics.

GreenPulse AI exists to help Kenya make smarter environmental decisions — today and for the future.

--------------------------------------------------
DATA CONTEXT USAGE
--------------------------------------------------
When real-time data is provided (weather, climate, location), USE IT:
- Reference specific temperatures, rainfall amounts, humidity
- Connect data points to practical implications
- Don't ignore provided data in favor of generic responses
"""
        
        # Mode-specific instructions
        if mode == "community":
            mode_prompt = """
--------------------------------------------------
RESPONSE MODE: COMMUNITY
--------------------------------------------------
- Simple language
- Occasional Swahili mix ("Tuchunge mazingira yetu")
- Action-oriented
- Suitable for SMS or public awareness
- Focus on what people CAN DO
- Use relatable examples (farming, local businesses)
- Encourage community action and collective responsibility
"""
        else:  # professional
            mode_prompt = """
--------------------------------------------------
RESPONSE MODE: PROFESSIONAL
--------------------------------------------------
- Formal
- Structured
- Data-driven
- Suitable for businesses, NGOs, and government
- Include specific metrics and figures where available
- Reference regulations and standards by name
- Provide executive summaries for complex analyses
- Include risk assessments and recommendations clearly separated
"""
        
        return base_prompt + mode_prompt
    
    async def _get_location_context(self, location: str) -> Dict[str, Any]:
        """Fetch real data for a Kenya location"""
        context = {}
        
        try:
            # Geocode the location
            geo_data = await gmaps_service.geocode_address(f"{location}, Kenya")
            
            if geo_data:
                lat = geo_data['latitude']
                lon = geo_data['longitude']
                context['location'] = {
                    'name': location,
                    'coordinates': {'latitude': lat, 'longitude': lon},
                    'formatted_address': geo_data.get('formatted_address', location)
                }
                
                # Get current weather from Google Weather API
                weather = await google_weather_client.get_current_weather(lat, lon)
                if weather:
                    context['current_weather'] = {
                        'temperature_celsius': weather.get('temperature'),
                        'feels_like_celsius': weather.get('feels_like'),
                        'humidity_percent': weather.get('humidity'),
                        'wind_speed_kmh': weather.get('wind_speed'),
                        'conditions': weather.get('conditions'),
                        'uv_index': weather.get('uv_index'),
                        'cloud_cover_percent': weather.get('cloud_cover'),
                        'is_daytime': weather.get('is_daytime')
                    }
                
                # Get 30-day climate data from NASA POWER
                climate = await nasa_client.get_recent_30_days(lat, lon)
                if climate:
                    # Calculate averages
                    temps = [v for v in climate.get('T2M', {}).values() if v != -999]
                    precip = [v for v in climate.get('PRECTOTCORR', {}).values() if v != -999]
                    humidity = [v for v in climate.get('RH2M', {}).values() if v != -999]
                    
                    context['climate_30_day'] = {
                        'avg_temperature_celsius': round(sum(temps)/len(temps), 1) if temps else None,
                        'total_precipitation_mm': round(sum(precip), 1) if precip else None,
                        'avg_humidity_percent': round(sum(humidity)/len(humidity), 1) if humidity else None,
                        'days_without_rain': sum(1 for p in precip if p < 1),
                        'max_temperature': round(max(temps), 1) if temps else None,
                        'min_temperature': round(min(temps), 1) if temps else None
                    }
                    
                    # Risk analysis
                    drought = nasa_client.analyze_drought_risk(climate)
                    flood = nasa_client.analyze_flood_risk(climate)
                    
                    context['risk_assessment'] = {
                        'drought': drought,
                        'flood': flood
                    }
        
        except Exception as e:
            logger.error(f"Error fetching location context: {e}")
        
        return context
    
    def _format_context_for_prompt(self, context: Dict[str, Any]) -> str:
        """Format the data context into a readable string for the AI"""
        if not context:
            return ""
        
        lines = ["\n═══════════════════════════════════════════════════════════════════"]
        lines.append("REAL-TIME DATA CONTEXT (Use this in your response)")
        lines.append("═══════════════════════════════════════════════════════════════════")
        
        if 'location' in context:
            loc = context['location']
            lines.append(f"\n📍 LOCATION: {loc.get('formatted_address', loc.get('name'))}")
            coords = loc.get('coordinates', {})
            lines.append(f"   Coordinates: {coords.get('latitude')}, {coords.get('longitude')}")
        
        if 'current_weather' in context:
            w = context['current_weather']
            lines.append(f"\n🌤️ CURRENT WEATHER (Google Weather API - Real-time):")
            lines.append(f"   Temperature: {w.get('temperature_celsius')}°C (feels like {w.get('feels_like_celsius')}°C)")
            lines.append(f"   Conditions: {w.get('conditions')}")
            lines.append(f"   Humidity: {w.get('humidity_percent')}%")
            lines.append(f"   Wind: {w.get('wind_speed_kmh')} km/h")
            lines.append(f"   UV Index: {w.get('uv_index')}")
            lines.append(f"   Cloud Cover: {w.get('cloud_cover_percent')}%")
        
        if 'climate_30_day' in context:
            c = context['climate_30_day']
            lines.append(f"\n📊 CLIMATE DATA (NASA POWER - Last 30 Days):")
            lines.append(f"   Avg Temperature: {c.get('avg_temperature_celsius')}°C")
            lines.append(f"   Temperature Range: {c.get('min_temperature')}°C to {c.get('max_temperature')}°C")
            lines.append(f"   Total Precipitation: {c.get('total_precipitation_mm')} mm")
            lines.append(f"   Days Without Rain: {c.get('days_without_rain')}")
            lines.append(f"   Avg Humidity: {c.get('avg_humidity_percent')}%")
        
        if 'risk_assessment' in context:
            r = context['risk_assessment']
            lines.append(f"\n⚠️ RISK ASSESSMENT:")
            if 'drought' in r:
                d = r['drought']
                lines.append(f"   Drought Risk: {d.get('severity', 'unknown').upper()}")
                lines.append(f"   - Days without adequate rain: {d.get('days_without_rain', 'N/A')}")
                lines.append(f"   - Avg precipitation: {d.get('avg_precipitation_mm', 'N/A')} mm/day")
            if 'flood' in r:
                f = r['flood']
                lines.append(f"   Flood Risk: {f.get('severity', 'unknown').upper()}")
                lines.append(f"   - Max daily rainfall: {f.get('max_daily_precipitation_mm', 'N/A')} mm")
                lines.append(f"   - Heavy rain days: {f.get('heavy_rain_days', 'N/A')}")
        
        lines.append("\n═══════════════════════════════════════════════════════════════════")
        
        return "\n".join(lines)
    
    async def ask(
        self,
        question: str,
        mode: ResponseMode = "community",
        location: Optional[str] = None,
        document_content: Optional[str] = None,
        include_weather: bool = True
    ) -> Dict[str, Any]:
        """
        Main method to ask GreenPulse AI anything
        
        Args:
            question: The user's question
            mode: "community" (simple) or "professional" (formal)
            location: Optional Kenya location for context-aware response
            document_content: Optional document text for analysis
            include_weather: Whether to fetch real weather/climate data
            
        Returns:
            Dict with answer, data_used, model, timestamp
        """
        if not self.client:
            return {
                "success": False,
                "error": "AI service not configured",
                "answer": None
            }
        
        # Build the full prompt
        system_prompt = self._get_system_prompt(mode)
        
        # Gather context
        context = {}
        user_message_parts = []
        
        # Fetch location data if provided
        if location and include_weather:
            context = await self._get_location_context(location)
            if context:
                user_message_parts.append(self._format_context_for_prompt(context))
        
        # Add document content if provided
        if document_content:
            user_message_parts.append(f"""
═══════════════════════════════════════════════════════════════════
DOCUMENT FOR ANALYSIS
═══════════════════════════════════════════════════════════════════
{document_content[:15000]}
{"[Document truncated...]" if len(document_content) > 15000 else ""}
═══════════════════════════════════════════════════════════════════
""")
        
        # Add the actual question
        user_message_parts.append(f"\nUSER QUESTION:\n{question}")
        
        full_user_message = "\n".join(user_message_parts)
        
        try:
            response = await asyncio.to_thread(
                self.client.chat.completions.create,
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": full_user_message}
                ],
                temperature=0.7 if mode == "community" else 0.5,
            )
            
            answer = response.choices[0].message.content.strip()
            
            return {
                "success": True,
                "answer": answer,
                "mode": mode,
                "location": location,
                "data_used": {
                    "current_weather": "current_weather" in context,
                    "climate_30_day": "climate_30_day" in context,
                    "risk_assessment": "risk_assessment" in context,
                    "document_analyzed": document_content is not None
                },
                "model": self.model,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"GreenPulse AI error: {e}")
            return {
                "success": False,
                "error": str(e),
                "answer": None
            }


# Global instance
greenpulse_ai = GreenPulseAI()
