intent_keywords = {
    "startup_tech": ["startup", "found", "scale", "MVP", "bootstrap"],
    "ai_learning": ["AI", "ml", "deep learning", "neural networks"],
    "career_growth": ["promotion", "interview", "resume", "upskill"],
    "creative_inspo": ["art", "design", "write", "paint", "film", "shoot"],
    "explore": []
}

def classify_aspiration(aspirations):
    asp_string = " ".join(aspirations).lower()
    for category, keywords in intent_keywords.items():
        if any(k in asp_string for k in keywords):
            return category
    return "explore"
