# curie/models/passive_event.py

from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class PassiveEvent(BaseModel):
    user_id: str
    timestamp: Optional[datetime] = None  # time of the event
    source: str                           # e.g. "youtube.com"
    duration_seconds: int                # how long user stayed
    category: str                        # e.g. "news", "memes", "tech"
    topic_tags: Optional[List[str]] = [] # e.g. ["startups", "reactjs"]
    via: Optional[str] = "extension"     # e.g. "cookie", "extension", "feed-click"
    active: Optional[bool] = True        # was user actively engaged?
