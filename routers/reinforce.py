from fastapi import APIRouter, HTTPException
from datetime import datetime

from models.feedback import UserFeedback
from agent.evaluation import evaluate_user_session
from supabase_client import supabase  # shared client

router = APIRouter()

@router.post("/reinforce")
def reinforce(feedback: UserFeedback):
    # 1. Insert feedback
    feedback_dict = feedback.dict()
    feedback_dict["timestamp"] = feedback_dict["timestamp"] or datetime.utcnow()

    insert_response = supabase.table("user_feedback").insert(feedback_dict).execute()
    if insert_response.error:
        raise HTTPException(status_code=500, detail="Failed to insert feedback")

    feedback_id = insert_response.data[0]["id"]

    # 2. Fetch user profile
    user_resp = supabase.table("users").select("*").eq("id", feedback.user_id).single().execute()
    user_data = user_resp.data
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")

    # 3. Get recent sessions for trend-based evaluation
    recent_sessions_resp = (
        supabase.table("user_sessions")
        .select("*")
        .eq("user_id", feedback.user_id)
        .order("created_at", desc=True)
        .limit(5)
        .execute()
    )
    recent_sessions = recent_sessions_resp.data if recent_sessions_resp.data else []

    # 4. Run evaluation
    evaluation_result = evaluate_user_session(user_data, feedback_dict, recent_sessions)

    # 5. Check if a pending session exists
    pending_resp = (
        supabase.table("user_sessions")
        .select("*")
        .eq("user_id", feedback.user_id)
        .eq("status", "pending")
        .order("created_at", desc=True)
        .limit(1)
        .execute()
    )

    now = datetime.utcnow()
    session_payload = {
        "user_id": feedback.user_id,
        "feedback_id": feedback_id,
        "created_at": now,
        "context": evaluation_result.get("context", {}),
        "mood": evaluation_result.get("mood"),
        "fatigue_level": evaluation_result.get("fatigue_level"),
        "curiosity_score": evaluation_result.get("curiosity_score"),
        "tone": evaluation_result.get("tone"),
        "intent": evaluation_result.get("intent"),
        "time_budget": evaluation_result.get("time_budget"),
        "discipline_score": evaluation_result.get("discipline_score"),
        "stress_level": evaluation_result.get("stress_level"),
        "sleep_score": evaluation_result.get("sleep_score"),
        "status": "pending"
    }

    # 6. Insert or update the pending session
    if pending_resp.data:
        session_id = pending_resp.data[0]["id"]
        update_response = supabase.table("user_sessions").update(session_payload).eq("id", session_id).execute()
        if update_response.error:
            raise HTTPException(status_code=500, detail="Failed to update pending session")
        session = update_response.data[0]
    else:
        insert_session = supabase.table("user_sessions").insert(session_payload).execute()
        if insert_session.error:
            raise HTTPException(status_code=500, detail="Failed to insert new session")
        session = insert_session.data[0]

    return {
        "message": "Feedback saved and session evaluated",
        "session": session,
        "context": evaluation_result.get("context")
    }
