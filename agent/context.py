# agent/context.py

from datetime import datetime

def find_slot_level(current_time: str, slot_map: dict) -> str:
    for slot, level in slot_map.items():
        start, end = slot.split("-")
        if start <= current_time <= end:
            return level
    return "medium"

def build_context(user_data: dict) -> dict:
    now = datetime.now()
    current_time = now.strftime("%H:%M")

    in_break = current_time in user_data.get("routine", {}).get("breaks", [])
    in_focus = any(
        start <= current_time <= end
        for (start, end) in user_data.get("routine", {}).get("focus_blocks", [])
    )
    slot_level = find_slot_level(current_time, user_data.get("time_slots", {}))

    return {
        "current_time": current_time,
        "in_focus": in_focus,
        "in_break": in_break,
        "slot_level": slot_level,
        "interests": user_data.get("interests", []),
        "aspirations": user_data.get("aspirations", []),
        "personality": user_data.get("personality", []),
        "work_type": user_data.get("work_type", "unknown"),
        "topics": user_data.get("topics", []),
        "discovery_style": user_data.get("discovery_style", "scrolling"),
        "serendipity_flex": user_data.get("serendipity_flex", 0.5),
        "curiosity_score": user_data.get("curiosity_score", 50),  # default neutral
    }
