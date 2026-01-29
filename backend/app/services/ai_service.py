"""
OpenRouter AI Service for Terraguard
Uses DeepSeek R1 0528 (Free) model
"""
import httpx
from app.config import settings
import json

class OpenRouterService:
    """
    AI service using OpenRouter API with DeepSeek R1 (free)
    """
    
    def __init__(self):
        self.api_key = settings.OPENROUTER_API_KEY
        self.base_url = settings.OPENROUTER_BASE_URL
        self.model = settings.OPENROUTER_MODEL
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://terraguard.com",
            "X-Title": "Terraguard Climate AI"
        }
    
    async def generate_alert_summary(self, risk_data: dict) -> dict:
        """
        Generate AI summary for climate risk alert with conservation focus
        
        Args:
            risk_data: Dict containing region, risk_type, climate_data
            
        Returns:
            Dict with summary, causes, preventive_measures, immediate_actions
        """
        prompt = f"""
You are Terraguard AI - Africa's land conservation and climate resilience expert.

MISSION: Combat land degradation through education and practical conservation advice.

Analyze this climate risk and provide actionable information that INCLUDES land conservation measures:

Region: {risk_data.get('region')}
Risk Type: {risk_data.get('risk_type')}
Climate Data: {json.dumps(risk_data.get('data', {}), indent=2)}

Provide your response in this exact JSON format:
{{
  "summary": "2-5 sentence explanation of what is happening and its impact on land/soil",
  "causes": "2-5 sentence explanation including any land degradation factors",
  "preventive_measures": [
    "Land conservation measure (e.g., plant cover crops, build terraces)",
    "Soil protection technique",
    "Tree planting or vegetation-based solution",
    "Water conservation or management technique",
    "Community-based environmental action"
  ],
  "immediate_actions": [
    "What people should do right now to protect land and soil",
    "Action to prevent erosion or degradation",
    "Community mobilization step",
    "Soil/vegetation protection action",
    "Resource conservation measure"
  ]
}}

IMPORTANT:
- ALWAYS include land conservation, soil protection, and tree planting advice
- Connect weather events to land management actions
- Example: "Heavy rain expected - protect topsoil by planting cover crops or building contour lines"
- Use simple, hopeful, practical language
- NO emojis
- Mix English and Swahili phrases naturally where appropriate
- Focus on what people CAN DO to protect their land

Keep language accessible for SMS users. Emphasize: "Plant one tree, save your soil."
"""
        
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": "You are Terraguard AI - providing climate risk analysis with a focus on land conservation, soil protection, and rehabilitation for African communities. Combat land degradation through every alert. Be practical, hopeful, and action-oriented."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.7
            # No max_tokens - AI generates complete conservation advice naturally
        }
        
        async with httpx.AsyncClient(timeout=60.0) as client:  # 60s timeout for complete responses
            response = await client.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=payload
            )
            response.raise_for_status()
            
            result = response.json()
            content = result['choices'][0]['message']['content']
            
            # Parse JSON response
            try:
                parsed = json.loads(content)
                return parsed
            except json.JSONDecodeError:
                # Fallback if AI doesn't return valid JSON
                return {
                    "summary": content[:200],
                    "causes": "Climate data analysis in progress",
                    "preventive_measures": [
                        "Monitor weather conditions regularly",
                        "Prepare emergency water supplies",
                        "Implement soil conservation measures",
                        "Diversify crop selection",
                        "Stay connected with local agricultural advisories"
                    ],
                    "immediate_actions": [
                        "Stay informed about current conditions",
                        "Follow local advisories and warnings",
                        "Secure essential resources",
                        "Contact local agricultural extension officers",
                        "Document any damage or concerns"
                    ]
                }
    
    async def chat_response(self, user_message: str, context: dict = None) -> str:
        """
        Generate AI response for user chat (SMS/Telegram)
        
        Args:
            user_message: User's question
            context: Optional context (location, history, etc.)
            
        Returns:
            AI response string
        """
        system_context = """You are Terraguard AI - Africa's land conservation and climate resilience assistant.

CORE MISSION: Combat land degradation through education, awareness, and community engagement.

FOCUS ON:
- Land degradation causes and solutions (deforestation, overgrazing, erosion)
- Soil conservation and rehabilitation (terracing, tree planting, mulching)
- Community-based environmental care
- Practical conservation advice with every climate alert
- Region-specific tree species and restoration techniques

TONE: Simple, hopeful, and practical. Mix English and Swahili naturally.
NO EMOJIS. Be encouraging about conservation efforts.

Every answer should connect to land protection, soil health, or environmental stewardship."""
        
        if context:
            system_context += f"\n\nUser context: {json.dumps(context)}"
        
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": system_context
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            "temperature": 0.7
            # No max_tokens - AI provides appropriate length based on question complexity
        }
        
        async with httpx.AsyncClient(timeout=60.0) as client:  # 60s timeout for detailed conservation education
            response = await client.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=payload
            )
            response.raise_for_status()
            
            result = response.json()
            return result['choices'][0]['message']['content']
    
    async def chat_response_with_system(self, user_message: str, system_prompt: str, context: dict = None) -> str:
        """
        Generate AI response with custom system prompt
        
        Args:
            user_message: User's question
            system_prompt: Custom system instructions
            context: Optional context
            
        Returns:
            AI response string
        """
        # System prompt already contains all necessary guidelines
        # AI is smart enough to determine appropriate response length
        
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            "temperature": 0.7
            # No max_tokens limit - AI will naturally follow word count instructions in prompt
        }
        
        async with httpx.AsyncClient(timeout=60.0) as client:  # Increased timeout for comprehensive analysis
            response = await client.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=payload
            )
            response.raise_for_status()
            
            result = response.json()
            return result['choices'][0]['message']['content']
    
    async def generate_crop_recommendation(self, location: str, climate_data: dict) -> list:
        """
        Generate crop recommendations based on location and climate
        
        Args:
            location: Region name
            climate_data: Recent climate data
            
        Returns:
            List of recommended crops with explanations
        """
        prompt = f"""
Based on the following climate data for {location}, recommend 5 suitable crops to plant:

Climate Data:
{json.dumps(climate_data, indent=2)}

Return a JSON array of 5 crops with this format:
[
  {{
    "crop": "Crop name",
    "reason": "One sentence why this crop is suitable",
    "season": "Best planting season"
  }}
]
"""
        
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": "You are an agricultural expert for African regions. Recommend practical, drought-resistant, and climate-appropriate crops."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.7
            # No max_tokens - AI provides complete crop knowledge naturally
        }
        
        async with httpx.AsyncClient(timeout=60.0) as client:  # 60s timeout for comprehensive recommendations
            response = await client.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=payload
            )
            response.raise_for_status()
            
            result = response.json()
            content = result['choices'][0]['message']['content']
            
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                # Fallback recommendations
                return [
                    {"crop": "Sorghum", "reason": "Drought-resistant and adaptable", "season": "Short rains"},
                    {"crop": "Millet", "reason": "Thrives in low rainfall areas", "season": "Any season"},
                    {"crop": "Cowpeas", "reason": "Nitrogen-fixing and nutritious", "season": "Short rains"},
                    {"crop": "Cassava", "reason": "Hardy and reliable staple crop", "season": "Long rains"},
                    {"crop": "Pigeon peas", "reason": "Drought-tolerant legume", "season": "Long rains"}
                ]

# Global instance
ai_service = OpenRouterService()
