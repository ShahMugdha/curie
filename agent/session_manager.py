from datetime import datetime, timedelta

# In-memory session storage (replace with Redis/Supabase later)
session_store = {}

def start_feed_session(user_id: str):
    session_store[user_id] = {
        "start_time": datetime.now(),
        "expired": False
    }

def should_generate_feed(user_id: str) -> bool:
    session = session_store.get(user_id)
    if not session:
        return True
    elapsed = datetime.now() - session["start_time"]
    if elapsed > timedelta(minutes=30):
        session_store[user_id]["expired"] = True
        return False
    return True

def refresh_session(user_id: str):
    session_store[user_id] = {
        "start_time": datetime.now(),
        "expired": False
    }
