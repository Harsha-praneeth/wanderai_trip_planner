import google.generativeai as genai
import json

def generate_trip(
    source,
    destination,
    days,
    budget_level,
    interests,
    places_to_visit="",
    language="English",
    api_key=""
):
    """
    Generate trip using user's Gemini API key with strict JSON validation.
    """
    if not api_key:
        raise Exception(
            "Please enter your Gemini API Key in the sidebar before generating a trip."
        )

    genai.configure(api_key=api_key)

    prompt = f"""
You are a professional travel planner. Create a detailed travel itinerary.

CRITICAL RULES:
- Return ONLY a single valid JSON object.
- DO NOT return HTML tags like <div>, <span>, or <p>.
- DO NOT return Markdown styling within descriptions.
- Descriptions must be purely plain text strings.

Source: {source}
Destination: {destination}
Days: {days}
Budget Level: {budget_level}
Interests: {', '.join(interests)}
Places User Wants To Visit: {places_to_visit}
Language: {language}

Format layout template to follow exactly:
{{
  "overview": {{
    "trip_name": "",
    "description": "",
    "route_optimization": ""
  }},
  "itinerary": [
    {{
      "day": 1,
      "theme": "",
      "activities": {{
        "morning": {{ "title": "", "description": "", "emoji": "" }},
        "afternoon": {{ "title": "", "description": "", "emoji": "" }},
        "evening": {{ "title": "", "description": "", "emoji": "" }}
      }}
    }}
  ],
  "costs": {{
    "accommodation": 0,
    "food": 0,
    "transportation": 0,
    "activities": 0,
    "total": 0
  }},
  "food_recommendations": [
    {{ "item": "", "type": "", "where_to_try": "" }}
  ],
  "packing_list": [],
  "travel_tips": []
}}
"""

    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(prompt)
        text = response.text.strip()

        # Strip standard markdown block wrappers if present
        if text.startswith("```json"):
            text = text.replace("```json", "").replace("```", "").strip()
        elif text.startswith("```"):
            text = text.replace("```", "").strip()

        return json.loads(text)

    except Exception as e:
        raise Exception(f"Gemini Error: {str(e)}")