# utils/session_trends.py

from typing import List, Dict
from statistics import mean

def summarize_trends(sessions: List[Dict]) -> Dict:
    """
    Analyzes recent sessions to detect trends in evaluation metrics.
    Returns average values, rate-of-change, or significant patterns.
    """

    if not sessions:
        return {}

    def avg(metric: str):
        values = [s.get(metric) for s in sessions if s.get(metric) is not None]
        return round(mean(values), 2) if values else None

    def delta(metric: str):
        values = [s.get(metric) for s in sessions if s.get(metric) is not None]
        return round(values[-1] - values[0], 2) if len(values) >= 2 else 0

    return {
        "avg_fatigue": avg("fatigue_level"),
        "avg_stress": avg("stress_level"),
        "avg_sleep": avg("sleep_score"),
        "avg_discipline": avg("discipline_score"),
        "avg_curiosity": avg("curiosity_score"),
        "tone_stability": len(set(s.get("tone") for s in sessions if s.get("tone"))) == 1,
        "curiosity_delta": delta("curiosity_score"),
        "fatigue_delta": delta("fatigue_level"),
    }
