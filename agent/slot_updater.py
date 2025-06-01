from agent.mood_engine import infer_mood

def update_time_slots(old_slots: dict, feedback: dict, now: str) -> dict:
    updated = old_slots.copy()
    for slot in old_slots:
        start, end = slot.split("-")
        if start <= now <= end:
            updated[slot] = infer_mood(feedback)
            break
    return updated
