import os
from google import genai
import json
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini
api_key = os.getenv("GEMINI_API_KEY")

async def analyze_incident_with_gemini(incident_description: str):
    if not api_key or api_key == "your_gemini_api_key_here":
        # Mock response if no key is provided yet
        return {
            "summary": "Mock summary: " + incident_description[:50],
            "risk_level": "HIGH",
            "risk_reason": "Mock reason",
            "recommended_actions": ["Action 1", "Action 2"],
            "urgency": "Immediate",
            "category": "Unauthorized Access"
        }

    prompt = f"""
You are an AI school security assistant.
Analyze the following security incident and respond ONLY with a JSON object. No markdown formatting outside the JSON block.

Incident:
{incident_description}

Return a JSON with these exact keys:
"summary": A brief 1-sentence summary.
"risk_level": One of: LOW, MEDIUM, HIGH, CRITICAL.
"risk_reason": Why you chose this risk level.
"recommended_actions": A list of 3-4 string actions.
"urgency": e.g., Immediate, High, Moderate, Low.
"category": The type of incident (e.g., Unauthorized Access, Medical, Fire, Dispute, etc.)
"""
    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model='gemini-3.5-flash',
            contents=prompt
        )
        text_resp = response.text.strip()
        
        # Strip potential markdown formatting if model didn't obey
        if text_resp.startswith("```json"):
            text_resp = text_resp[7:]
        if text_resp.startswith("```"):
            text_resp = text_resp[3:]
        if text_resp.endswith("```"):
            text_resp = text_resp[:-3]
            
        result = json.loads(text_resp.strip())
        return result
    except Exception as e:
        print(f"Gemini API Error: {e}")
        return {
            "summary": "Error analyzing incident",
            "risk_level": "UNKNOWN",
            "risk_reason": str(e),
            "recommended_actions": [],
            "urgency": "UNKNOWN",
            "category": "UNKNOWN"
        }
