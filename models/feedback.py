# curie/models/feedback.py

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Mapping of question "type" to actual feedback model field names
FEEDBACK_TYPE_TO_FIELD = {
    "sleep": "sleep_feedback",
    "meal": "meal_feedback",
    "focus": "focus_feedback",
    "opinion": "opinion",
    "books": "books",
    "shows_movies": "shows_movies",
    "recent_topics": "recent_topics",
    "political_interest": "political_interest",
    "communities": "communities",
    "influencers": "influencers",
    "productivity": "productivity_feedback",
    "study_time": "study_time_feedback",
    "reading_time": "reading_time_feedback",
    "social_time": "social_time_feedback",
    "break_time": "break_time_feedback",
    "meal_time": "meal_time_followup",
}

class UserFeedback(BaseModel):
    user_id: str
    timestamp: Optional[datetime] = None
    
    sleep_feedback: Optional[str] = None
    stress_feedback: Optional[str] = None
    meal_feedback: Optional[str] = None
    focus_feedback: Optional[str] = None
    opinion: Optional[str] = None
    tags: Optional[list[str]] = []

    # Cognitive + Interests
    books: Optional[str] = None
    shows_movies: Optional[str] = None
    recent_topics: Optional[str] = None
    political_interest: Optional[str] = None
    communities: Optional[str] = None
    influencers: Optional[str] = None

    # Behavioral
    productivity_feedback: Optional[str] = None
    social_time_feedback: Optional[str] = None
    study_time_feedback: Optional[str] = None
    reading_time_feedback: Optional[str] = None
    break_time_feedback: Optional[str] = None
    meal_time_followup: Optional[str] = None

    source: Optional[str] = "reinforcement"
    ready_for_evaluation: Optional[bool] = True
