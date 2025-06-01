from pydantic import BaseModel
from typing import Optional, List
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

    # Physical/Mental State
    sleep_feedback: Optional[str] = "Slept for 6-7 hours, feeling rested"
    stress_feedback: Optional[str] = "Mild stress due to work, manageable"
    meal_feedback: Optional[str] = "Ate 2 proper meals today, moderately healthy"
    focus_feedback: Optional[str] = "Able to focus well for the last 2 hours"
    opinion: Optional[str] = "Feeling curious and open to learning today"
    tags: Optional[List[str]] = ["focused", "open-minded"]

    # Cognitive + Interests
    books: Optional[str] = "Reading 'Deep Work' by Cal Newport"
    shows_movies: Optional[str] = "Watched a documentary on Netflix"
    recent_topics: Optional[str] = "Interested in productivity tools and AI startups"
    political_interest: Optional[str] = "Interested in economic reforms and tech policy"
    communities: Optional[str] = "Active on IndieHackers and r/Startups"
    influencers: Optional[str] = "Following Naval Ravikant and Ali Abdaal"

    # Behavioral
    productivity_feedback: Optional[str] = "Completed most planned tasks today"
    social_time_feedback: Optional[str] = "Spent some time with friends offline"
    study_time_feedback: Optional[str] = "Studied for 1 hour in the morning"
    reading_time_feedback: Optional[str] = "Read 20 pages post-lunch"
    break_time_feedback: Optional[str] = "Took two 10-minute breaks between work blocks"
    meal_time_followup: Optional[str] = "Lunch delayed by 30 mins, breakfast on time"

    source: Optional[str] = "reinforcement"
    ready_for_evaluation: Optional[bool] = True
