import random

def rank_content_by_tone_and_novelty(content_pool, user_context, user_history):
    tone = user_context["tone"]
    seen_links = user_history.get("seen_links", [])

    filtered = [
        c for c in content_pool if c["tone"] == tone and c["link"] not in seen_links
    ]

    if not filtered:
        filtered = [c for c in content_pool if c["link"] not in seen_links]

    return random.sample(filtered, k=min(3, len(filtered)))
