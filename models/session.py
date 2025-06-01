# curie/models/session.py

from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class EvaluationContext(BaseModel):
    current_time: str
    in_focus: bool
    in_break: bool
    slot_level: str
    interests: List[str]
    aspirations: List[str]
    personality: List[str]
    work_type: str
    topics: List[str]
    tone: str
    discovery_style: str
    serendipity_flex: float
    curiosity_score: int

class UserSession(BaseModel):
    user_id: str
    feedback_id: Optional[str]
    timestamp: Optional[datetime] = None  # defaults to now if not set
    context: EvaluationContext
    mood: Optional[str]
    fatigue_level: Optional[int]
    curiosity_score: Optional[int]
    tone: Optional[str]
    intent: Optional[str]
    time_budget: Optional[int]
    discipline_score: Optional[int]
    stress_level: Optional[int]
    sleep_score: Optional[int]
    active: bool = True
