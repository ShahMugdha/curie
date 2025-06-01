from pydantic import BaseModel
from typing import List, Optional

class Routine(BaseModel):
    wake_time: str
    sleep_time: str
    breaks: List[str]
    focus_blocks: List[List[str]]

class UserProfile(BaseModel):
    email: str
    name: str
    routine: Routine
    interests: List[str]
    aspirations: List[str]
    personality: List[str]
    work_type: str
    topics: Optional[List[str]] = []

    # NEW: Passive data options
    allow_cookies: Optional[bool] = False
    allow_extension_tracking: Optional[bool] = False
