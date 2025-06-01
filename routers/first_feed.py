# curie/routers/first_feed.py

from fastapi import APIRouter, HTTPException
from supabase_client import supabase
from content_selector.content_router import fetch_all_content_by_session
from datetime import datetime

router = APIRouter()

@router.get("/first-feed")
def generate_first_time_feed(user_id: str):
    # 1. Fetch user
    user_resp = supabase.table("users").select("*").eq("id", user_id).single().execute()
    user = user_resp.data

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # 2. Build default session
    context = {
        "topics": user.get("topics", []),
        "personality": user.get("personality", []),
    }

    pseudo_session = {
        "user_id": user_id,
        "intent": "explore",
        "tone": "neutral",
        "curiosity_score": 50,
        "discipline_score": 50,
        "stress_level": 50,
        "fatigue_level": 50,
        "sleep_score": 50,
        "time_budget": 30,
        "context": context,
        "created_at": datetime.utcnow().isoformat(),
    }

    # 3. Fetch content
    feed = fetch_all_content_by_session(pseudo_session, limit=20)

    return {
        "message": "Generated initial feed using static data only",
        "session_basis": pseudo_session,
        "feed": feed
    }
