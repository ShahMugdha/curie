import openai

intent_keywords = {
    "startup_tech": ["startup", "found", "scale", "MVP", "bootstrap"],
    "ai_learning": ["AI", "ml", "deep learning", "neural networks"],
    "career_growth": ["promotion", "interview", "resume", "upskill"],
    "creative_inspo": ["art", "design", "write", "paint", "film", "shoot"],
    "explore": []
}

def classify_aspiration(aspirations: list[str]) -> str:
    asp_string = " ".join(aspirations).lower()
    for category, keywords in intent_keywords.items():
        if any(k.lower() in asp_string for k in keywords):
            return category
    return "explore"

def classify_aspiration_gpt(aspirations: list[str]) -> str:
    prompt = f"""
    Based on the user's aspirations below, return one of these categories:
    ['startup_tech', 'ai_learning', 'career_growth', 'creative_inspo', 'explore']

    Aspirations:
    {', '.join(aspirations)}

    Category:"""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=10
    )
    return response['choices'][0]['message']['content'].strip().lower()
