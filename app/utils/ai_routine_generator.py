from groq import Groq
from typing import List, Dict
import json
from ..config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)

def genarate_ai_routine(
    mood_rating: int,
    emotions: List[str],
    note: str | None,
    preferred_time: str | None = None
) -> Dict:
    """
    personalized routine generate using AI
    Output: dict with name, duration, activities list
    """
    
    emotions_str = ", ".join(emotions) if emotions else "neutral"
    note_text = f"User note: {note}" if note else "No additional note."
    time_info = f"Preferred time: {preferred_time}" if preferred_time else "Any time of the day."

    prompt = f"""
You are an expert wellness coach creating a short, calming daily routine for a mental health app called Ayni Wellness.

User's current mood:
- Mood rating: {mood_rating}/10
- Emotions: {emotions_str}
- {note_text}
- {time_info}

Create ONE short personalized routine (20-40 minutes total) with 3-4 activities.
Focus on helping the user feel better based on their current state.

Available activity types (choose from these only):
- Meditation (e.g., Anxiety Relief, Gratitude, Sleep)
- Sound Healing (e.g., 528 Hz, Rain Sounds, Tibetan Bowls)
- Journaling (give a specific prompt)
- Podcast (short mindful episode suggestion)

Output strictly in JSON format:
{{
  "name": "Short meaningful routine name",
  "duration_minutes": total minutes,
  "scheduled_time": "suggested time like 07:00 AM or Evening",
  "activities": [
    {{
      "activity_type": "Meditation|Sound Healing|Journaling|Podcast",
      "title": "Clear title for user",
      "duration_minutes": number
    }}
  ]
}}

Make it calming, positive, and realistic. Keep language warm and supportive.
"""


    try:
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.1-8b-instant",
            temperature=0.7,
            max_tokens=500,
            response_format={"type": "json_object"}
        )
        
        raw_json = chat_completion.choices[0].message.content
        data = json.loads(raw_json)
        
        if "activities" not in data or len(data["activities"]) < 2:
            raise ValueError("Invalid AI response")
             
        return data

    
    except Exception as e:
            print(f"AI generation error: {e}")
            return {
                "name": "Gentle Evening Wind Down",
                "duration_minutes": 25,
                "scheduled_time": "Evening",
                "activities": [
                    {"activity_type": "Sound Healing", "title": "528 Hz Anxiety Relief Sound", "duration_minutes": 10},
                    {"activity_type": "Meditation", "title": "5-Minute Breathing for Calm", "duration_minutes": 5},
                    {"activity_type": "Journaling", "title": "What went well today?", "duration_minutes": 5},
                    {"activity_type": "Podcast", "title": "Short Mindful Moment Episode", "duration_minutes": 5}
                ]
            }