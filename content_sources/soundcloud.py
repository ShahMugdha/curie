import os
import requests

SOUNDCLOUD_CLIENT_ID = os.getenv("SOUNDCLOUD_CLIENT_ID")

def fetch_soundcloud(intent, tone, duration):
    query = f"{intent} {tone}"
    url = f"https://api-v2.soundcloud.com/search/tracks?q={query}&client_id={SOUNDCLOUD_CLIENT_ID}&limit=5"

    response = requests.get(url)
    if response.status_code != 200:
        return []

    data = response.json()
    return [
        {
            "title": item["title"],
            "url": item["permalink_url"],
            "source": "SoundCloud",
            "duration_sec": item["duration"] // 1000,
            "intent": intent,
            "tone": tone,
        }
        for item in data.get("collection", [])
    ]
