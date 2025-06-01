from pydantic import BaseModel
from typing import List

class ContentItem(BaseModel):
    id: str
    title: str
    platform: str
    type: str
    intent_tags: List[str]
    topics: List[str]
    tone: str
    format: str
    duration_minutes: int
    link: str
    description: str
