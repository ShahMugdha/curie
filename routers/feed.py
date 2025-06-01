from fastapi import APIRouter, HTTPException
from supabase_client import supabase
from agent.content_selector.content_router import fetch_all_content_by_context

router = APIRouter()

@router.get("/feed")
def generate_feed(user_id: str):
    # 1. Fetch the latest PENDING session
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
        raise HTTPException(status_code=404, detail="No pending session found")

    session = session_resp.data[0]
    session_id = session["id"]

    # 2. Mark all current ACTIVE sessions as inactive
    supabase.table("user_sessions").update({"status": "inactive"}).eq("user_id", user_id).eq("status", "active").execute()

    # 3. Promote pending session to ACTIVE
    supabase.table("user_sessions").update({"status": "active"}).eq("id", session_id).execute()

    # 4. Fetch feed using intelligent context
    context = session["context"]
    feed = fetch_all_content_by_context(context)

    return {
        "session": session,
        "feed": feed
    }
