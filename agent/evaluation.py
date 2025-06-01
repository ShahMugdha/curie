# agent/evaluation.py

from agent.llm import evaluate_metrics_with_llm
from utils.session_trends import summarize_trends
from models.session import EvaluationContext

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
    context = EvaluationContext(**evaluation).dict()
    return {
        **evaluation,
        "context": context
    }
