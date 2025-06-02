# agent/llm.py

from openai import OpenAI
import time
import json
from config import Config
from pydantic import BaseModel, ValidationError
from datetime import datetime
from typing import Optional, List

client = OpenAI(api_key=Config.OPENAI_API_KEY)

# -------------------------
# Pydantic response schema
# -------------------------

class LLMEvaluationResult(BaseModel):
    mood: Optional[str]
    fatigue_level: Optional[int]
    curiosity_score: Optional[int]
    tone: Optional[str]
    intent: Optional[str]
    time_budget: Optional[int]
    discipline_score: Optional[int]
    stress_level: Optional[int]
    sleep_score: Optional[int]


def flatten_if_wrapped(data: dict) -> dict:
    """If response is wrapped inside a single key, unwrap it."""
    if len(data) == 1 and isinstance(list(data.values())[0], dict):
        return list(data.values())[0]
    return data

def clean_llm_output(raw: dict) -> dict:
    def coerce_int(val, fallback=0):
        try:
            return int(val)
        except:
            return fallback

    def coerce_float(val, fallback=0.0):
        try:
            return float(val)
        except:
            return fallback

    cleaned = flatten_if_wrapped(raw)

    return {
        "mood": str(cleaned.get("mood", "neutral")),
        "fatigue_level": coerce_int(cleaned.get("fatigue_level")),
        "curiosity_score": coerce_int(cleaned.get("curiosity_score")),
        "discipline_score": coerce_int(cleaned.get("discipline_score")),
        "stress_level": coerce_int(cleaned.get("stress_level")),
        "sleep_score": coerce_int(cleaned.get("sleep_score")),
        "tone": str(cleaned.get("tone", "neutral")),
        "intent": str(cleaned.get("intent", "general")),
        "time_budget": coerce_int(cleaned.get("time_budget")),
    }


# -------------------------
# Prompt Template
# -------------------------

def build_prompt(eval_input: dict) -> str:
    user = eval_input.get("user_profile", {})
    feedback = eval_input.get("feedback", {})
    trends = eval_input.get("session_trends", {})

    prompt = f"""You are an intelligent evaluator. Use the following data to infer the user's current emotional and mental state, and produce scores for:

- mood: 1–10  
  Represents emotional state; 1 = very low/negative, 10 = very happy/positive

- fatigue_level: 1–10  
  Measures physical or mental tiredness; 1 = fully energized, 10 = extremely tired

- curiosity_score: 0–100  
  Indicates desire to explore, learn, and discover new things

- discipline_score: 0–100  
  Reflects self-control, consistency, and ability to focus without distractions

- stress_level: 1–10  
  Indicates how overwhelmed or anxious the user currently feels; 10 = extremely stressed

- sleep_score: 1–10  
  Measures perceived sleep quality and restfulness from recent nights

- tone: one of [playful, serious, thoughtful, energetic, relaxed, casual]  
  Captures current cognitive-emotional tone of the user

- intent: short tag (e.g. learn, explore, relax, catch-up, deep-focus)  
  Describes what the user is primarily trying to do right now

- time_budget: number (in minutes)  
  Estimated amount of time the user is willing to dedicate to content right now


Static Profile:
- Work Type: {user.get('work_type')}
- Personality: {', '.join(user.get('personality', []))}
- Aspirations: {', '.join(user.get('aspirations', []))}
- Routine: {user.get('routine')}
- Interests: {', '.join(user.get('interests', []))}
- Topics: {', '.join(user.get('topics', []))}

Latest Feedback:
- Sleep hours: {feedback.get("sleep_hours")}
- Meal quality: {feedback.get("meal_quality")}
- Productivity: {feedback.get("productivity_rating")}
- Stress tags: {', '.join(feedback.get("stress_tags", []))}
- Focus level: {feedback.get("focus_rating")}
- Additional comments: {feedback.get("opinion")}

Recent Session Trends:
- Avg Curiosity: {trends.get("avg_curiosity")}
- Curiosity change: {trends.get("curiosity_delta")}
- Avg Stress: {trends.get("avg_stress")}
- Fatigue change: {trends.get("fatigue_delta")}
- Tone stability: {"Stable" if trends.get("tone_stability") else "Varied"}

Now respond in strict JSON format, like this:
  "mood": "neutral",                     // string
  "fatigue_level": 5,                   // integer
  "curiosity_score": 50,               // integer
  "discipline_score": 70,              // integer
  "stress_level": 4,                   // integer
  "sleep_score": 6,                    // integer
  "tone": "thoughtful",                // string
  "intent": "career_growth",           // string
  "time_budget": 25,                   // integer
Avoid putting the response inside another field like "data" or "user_emotional_and_mental_state". Just return the JSON object directly.

""".strip()

    return prompt

# -------------------------
# LLM Evaluation w/ retry
# -------------------------

def evaluate_metrics_with_llm(eval_input: dict) -> dict:
    prompt = build_prompt(eval_input)

    for attempt in range(3):
        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=300,
            )

            content = response.choices[0].message.content
            parsed = json.loads(content)
            parsed_cleaned = clean_llm_output(parsed)
            validated = LLMEvaluationResult(**parsed_cleaned)
            print("[LLM RAW RESPONSE]", content)
            print("[LLM PARSED CLEANED]", parsed_cleaned)
            return validated.dict()

        except (json.JSONDecodeError, ValidationError) as e:
            print(f"[LLM FORMAT ERROR] Attempt {attempt + 1}:", str(e))
            time.sleep(1)

        except Exception as ex:
            print(f"[LLM ERROR] Attempt {attempt + 1}:", str(ex))
            time.sleep(1)

    print("[LLM] Fallback to default scores.")
    return {
        "mood": "neutral",                     # 1–10
        "fatigue_level": 5,                   # 1–10
        "curiosity_score": 50,               # 0–100
        "discipline_score": 50,              # 0–100
        "stress_level": 5,                   # 1–10
        "sleep_score": 5,                    # 1–10
        "tone": "neutral",                   # playful, serious, thoughtful, energetic, relaxed, casual
        "intent": "general",                 # short tag (learn, relax, catch-up, etc.)
        "time_budget": 15,                   # in minutes
    }

