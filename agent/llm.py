# agent/llm.py

import openai
import time
import json
from config import Config
from pydantic import BaseModel, ValidationError

openai.api_key = Config.OPENAI_API_KEY

# -------------------------
# Pydantic response schema
# -------------------------

class LLMEvaluationResult(BaseModel):
    mood: str
    fatigue_level: int
    tone: str
    curiosity_score: int
    stress_level: int
    sleep_score: int
    discipline_score: int
    time_budget: int
    intent: str

# -------------------------
# Prompt Template
# -------------------------

def build_prompt(eval_input: dict) -> str:
    user = eval_input.get("user_profile", {})
    feedback = eval_input.get("feedback", {})
    trends = eval_input.get("session_trends", {})

    prompt = f"""
You are an intelligent evaluator. Use the following data to infer the user's current emotional and mental state, and produce scores for:

- mood (1-10)
- fatigue_level (1-10)
- curiosity_score (1-100)
- discipline_score (1-100)
- stress_level (1-10)
- sleep_score (1-10)
- tone (one of: playful, serious, thoughtful, energetic, relaxed)
- intent (short tag)
- time_budget (in minutes)

Static Profile:
- Work Type: {user.get('work_type')}
- Personality: {', '.join(user.get('personality', []))}
- Aspirations: {', '.join(user.get('aspirations', []))}
- Discovery Style: {user.get('discovery_style')}
- Serendipity Flex: {user.get('serendipity_flex')}
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
        "mood": "neutral",
        "fatigue_level": 50,
        "tone": "neutral",
        "curiosity_score": 50,
        "stress_level": 50,
        "sleep_score": 50,
        "discipline_score": 50,
        "time_budget": 15,
        "intent": "general"
    }
