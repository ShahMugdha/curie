# curie/models/session.py

from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class UserSession(BaseModel):
    user_id: str
    feedback_id: Optional[str]
    timestamp: Optional[datetime] = None
    mood: Optional[str]
    fatigue_level: Optional[int]
    curiosity_score: Optional[int]
    tone: Optional[str]
    intent: Optional[str]
    time_budget: Optional[int]
    discipline_score: Optional[int]
    stress_level: Optional[int]
    sleep_score: Optional[int]
    status: str = "pending"
