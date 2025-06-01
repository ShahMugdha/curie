# curie/routers/feedback_prompt.py

from fastapi import APIRouter, HTTPException, Query
from datetime import datetime
from supabase_client import supabase
from models.feedback import FEEDBACK_TYPE_TO_FIELD

router = APIRouter()

@router.get("/feedback-questions")
def get_feedback_questions(user_id: str):
    now = datetime.now().strftime("%H:%M")

    # 1. Get user static data
    user_resp = supabase.table("users").select("*").eq("id", user_id).single().execute()
    user = user_resp.data

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    routine = user.get("routine", {})
    focus_blocks = routine.get("focus_blocks", [])
    break_times = routine.get("breaks", [])
    topics = user.get("interests", []) + user.get("aspirations", [])

    questions = []

    # 2. Check if they just finished a focus block
    for block in focus_blocks:
        start, end = block
        if start <= now <= end:
            questions.append({
                "type": "focus",
                "field": FEEDBACK_TYPE_TO_FIELD["focus"],
                "text": "How focused were you in the last hour?"
            })
            break

    # 3. Ask about sleep every morning
    if now < "10:00":
        questions.append({
            "type": "sleep",
            "field": FEEDBACK_TYPE_TO_FIELD["sleep"],
            "text": "How was your sleep last night?"
        })

    # 4. Ask about meals after a break
    for brk in break_times:
        if brk <= now <= brk[:2] + ":59":  # e.g. 13:00 to 13:59
            questions.append({
                "type": "meal",
                "field": FEEDBACK_TYPE_TO_FIELD["meal"],
                "text": "Did you eat properly during your last break?"
            })
            break

    # 5. Ask opinions on interest topics occasionally
    if "cinema" in topics or "philosophy" in topics:
        questions.append({
            "type": "opinion",
            "field": FEEDBACK_TYPE_TO_FIELD["opinion"],
            "text": "What’s something you've been reflecting on lately?"
        })

    # 6. Ask about current reading/watching
    questions.append({
        "type": "books",
        "field": FEEDBACK_TYPE_TO_FIELD["books"],
        "text": "Are you currently reading any book or article?"
    })
    questions.append({
        "type": "shows_movies",
        "field": FEEDBACK_TYPE_TO_FIELD["books"],
        "text": "Watched anything interesting recently?"
    })

    return {
        "questions": questions
    }
