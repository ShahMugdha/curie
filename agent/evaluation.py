# agent/evaluation.py

from agent.llm import evaluate_metrics_with_llm
from utils.session_trends import summarize_trends
from typing import Optional
from pydantic import BaseModel

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

def evaluate_user_session(user_data: dict, feedback: dict, recent_sessions: list[dict] = []) -> dict:
    # Analyze trends
    session_trends = summarize_trends(recent_sessions)

    # Merge all into LLM input
    eval_input = {
        "user_profile": user_data,
        "feedback": feedback,
        "session_trends": session_trends
    }

    # Evaluate using LLM
    evaluation = evaluate_metrics_with_llm(eval_input)

    # Validate + return
    context = LLMEvaluationResult(**evaluation).dict()
    return {
        **evaluation,
        "context": context
    }
