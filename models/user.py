from pydantic import BaseModel, Field
from typing import List, Optional

class Routine(BaseModel):
    wake_time: str = Field(..., example="07:00")
    sleep_time: str = Field(..., example="23:00")
    breaks: List[str] = Field(..., example=["13:00", "17:30"])
    focus_blocks: List[List[str]] = Field(..., example=[["09:00", "11:00"], ["15:00", "17:00"]])

class UserProfile(BaseModel):
    email: str = Field(..., example="shahmugdha15@gmail.com")
    name: str = Field(..., example="Mugdha Shah")
    routine: Routine
    interests: List[str] = Field(..., example=["cinema", "music", "books"])
    aspirations: List[str] = Field(..., example=["career_growth", "creative_inspo"])
    personality: List[str] = Field(..., example=["curious", "reflective"])
    work_type: str = Field(..., example="independent")
    topics: Optional[List[str]] = Field(default=[], example=["ai", "startups", "philosophy"])

    # Passive data permissions
    allow_cookies: Optional[bool] = Field(default=False, example=True)
    allow_extension_tracking: Optional[bool] = Field(default=False, example=True)
