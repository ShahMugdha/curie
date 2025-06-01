# agent/llm.py

import openai
import time
import json
from config import Config
from pydantic import BaseModel, ValidationError
from datetime import datetime

openai.api_key = Config.OPENAI_API_KEY

# -------------------------
# Pydantic response schema
# -------------------------

class LLMEvaluationResult(BaseModel):
    mood: str
    fatigue_level: str
    curiosity_score: int
    tone: str
    intent: str
    time_budget: int
    discipline_score: int
    stress_level: int
    sleep_score: int

# -------------------------
# Prompt Template
# -------------------------

def build_prompt(eval_input: dict) -> str:
    user = eval_input.get("user_profile", {})
    feedback = eval_input.get("feedback", {})
    trends = eval_input.get("session_trends", {})

    prompt = f"""
You are an intelligent evaluator. Use the following data to infer the user's current emotional and mental state, and produce scores for:

- mood: 1–10  
  Represents emotional state; 1 = very low/negative, 10 = very happy/positive

- current_time: current time,

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

- discovery_style: one of [linear, exploratory, impulsive, research-driven, trend-aware]  
  Represents how the user tends to discover new content or ideas

- serendipity_flex: 0–1 (float)  
  Indicates how open the user is to unexpected or off-topic content; 0 = only focused, 1 = open to anything

- in_focus: boolean  
  Whether the user is currently inside one of their defined focus blocks

- in_break: boolean  
  Whether the user is currently on a scheduled break time

- slot_level: one of [deep, medium, shallow]  
  Represents the expected cognitive depth the user can handle based on routine and current time

- topics: list of strings  
  Personalized themes or domains of interest (e.g. productivity, philosophy, frontend)

- interests: list of strings  
  Broader long-term interests across categories (e.g. tech, cinema, history, finance)

- aspirations: list of strings  
  Goals or future ambitions (e.g. build a startup, publish a book, crack UPSC)

- personality: list of strings  
  Tags like [reflective, analytical, optimistic] inferred from user profile or resume

- discovery_style: string
  Indicates how adventurous or structured the user is in content discovery.

- work_type: string  
  Describes the user’s primary working context (e.g. student, freelancer, full-time employee)


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

Now respond with scores and labels in a JSON format.
""".strip()

    return prompt

# -------------------------
# LLM Evaluation w/ retry
# -------------------------

def evaluate_metrics_with_llm(eval_input: dict) -> dict:
    prompt = build_prompt(eval_input)

    for attempt in range(3):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=300,
            )

            content = response.choices[0].message["content"]
            parsed = json.loads(content)
            validated = LLMEvaluationResult(**parsed)
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
        "current_time": datetime.utcnow().isoformat(),

        # Extended fields
        "discovery_style": "linear",         # linear, exploratory, impulsive, etc.
        "serendipity_flex": 0.3,             # 0.0 to 1.0

        # Time-sensitive flags (set to safe defaults)
        "in_focus": False,
        "in_break": False,
        "slot_level": "shallow",            # deep, medium, shallow

        # Content relevance drivers (can be pulled from static profile if available)
        "topics": [],
        "interests": [],
        "aspirations": [],
        "personality": [],
        "work_type": "unknown"
    }

