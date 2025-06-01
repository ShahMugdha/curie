# routers/feed.py

from fastapi import APIRouter, HTTPException, Query
from supabase_client import supabase
from content_selector.content_router import fetch_all_content_by_session

router = APIRouter()

@router.get("/feed")
def generate_feed(user_id: str = Query(...)):
    # 1. Get latest pending session
    session_resp = (
        supabase.table("user_sessions")
        .select("*")
        .eq("user_id", user_id)
        .eq("status", "pending")
        .order("created_at", desc=True)
        .limit(1)
        .execute()
    )

    if not session_resp.data:
        raise HTTPException(status_code=404, detail="No pending session found.")

    session = session_resp.data[0]

    # 2. Use session context for content sourcing
    context = session.get("context", {})
    if not context:
        raise HTTPException(status_code=400, detail="Missing context in session.")

    content = fetch_all_content_by_session(session, limit=20)

    # 3. Mark session as active
    supabase.table("user_sessions").update({"status": "active"}).eq("id", session["id"]).execute()

    return {
        "message": "Feed generated successfully",
        "session": session,
        "context": context,
        "feed": content
    }
