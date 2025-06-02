from content_selector.source_registry import CATEGORY_SOURCE_MAP
from typing import List, Dict
import random

def get_priority_tags_from_session(session: dict) -> List[str]:
    tags = set()
    intent = session.get("intent", "explore")
    tone = session.get("tone", "neutral")
    mood = session.get("mood", "neutral")
    curiosity = session.get("curiosity_score", 50)
    fatigue = session.get("fatigue_level", 50)
    discipline = session.get("discipline_score", 50)
    sleep = session.get("sleep_score", 50)
    stress = session.get("stress_level", 50)

    # Intent-driven tags
    if intent == "creative_inspo":
        tags.update(["art", "cinema", "music"])
    elif intent == "ai_learning":
        tags.update(["ai", "tech"])
    elif intent == "career_growth":
        tags.update(["tech", "books"])
    elif intent == "explore":
        tags.update(["news", "sports", "books", "cinema"])

    # 🔍 Curiosity
    if curiosity > 70:
        tags.update(["books", "news", "deep dive", "opinion"])
    elif curiosity < 40:
        tags.update(["music", "shorts", "cinema"])

    # 🛌 Sleep & Fatigue
    if sleep < 40 or fatigue > 70:
        tags.update(["music", "cinema", "relax", "shorts"])
    elif fatigue < 30 and sleep > 70:
        tags.update(["ai", "tech", "books", "explainer"])

    # 🔥 Stress
    if stress > 60:
        tags.update(["music", "cinema", "art", "feel-good"])
    elif stress < 30:
        tags.update(["debate", "news", "politics", "startup"])

    # 🧘‍♂️ Discipline
    if discipline < 40:
        tags.update(["motivational", "productivity", "routines"])
    elif discipline > 70:
        tags.update(["books", "career", "goals"])

    # 🎭 Tone
    if tone == "light":
        tags.update(["memes", "shorts", "cinema", "feel-good"])
    elif tone == "reflective":
        tags.update(["books", "deep dive", "storytelling"])
    elif tone == "intense":
        tags.update(["debate", "politics", "longform"])

    # 😊 Mood
    if mood == "tired":
        tags.update(["music", "cinema", "shorts"])
    elif mood == "energized":
        tags.update(["learning", "tech", "podcast", "career"])
    elif mood == "anxious":
        tags.update(["relax", "art", "music"])
    elif mood == "bored":
        tags.update(["memes", "trending", "weird facts"])

    return list(tags)

def fetch_all_content_by_session(session: dict, limit: int = 20) -> List[Dict]:
    tags = get_priority_tags_from_session(session)
    content = []

    selected_sources = []
    for tag in tags:
        if tag in CATEGORY_SOURCE_MAP:
            selected_sources.extend(CATEGORY_SOURCE_MAP[tag])

    if not selected_sources:
        selected_sources.extend(CATEGORY_SOURCE_MAP.get("news", []))

    random.shuffle(selected_sources)
    selected_sources = selected_sources[:5]
    per_source_limit = max(1, limit // len(selected_sources))

    time_budget = session.get("time_budget", 10)

    for fetcher in selected_sources:
        try:
            fetched_items = fetcher(per_source_limit)
            filtered = [item for item in fetched_items if item.get("duration", 5) <= time_budget]
            content.extend(filtered)
        except Exception as e:
            print(f"[Content Fetch Error] {e}")

    return content[:limit]
