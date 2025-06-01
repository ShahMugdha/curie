import requests
import os
from config import Config

YOUTUBE_API_KEY = Config.get("YOUTUBE_API_KEY")

def fetch_youtube_videos(query: str, limit: int = 5):
    if not YOUTUBE_API_KEY:
        raise ValueError("Missing YOUTUBE_API_KEY in config")

    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "q": query,
        "type": "video",
        "maxResults": limit,
        "key": YOUTUBE_API_KEY
    }

    response = requests.get(url, params=params)
    if not response.ok:
        print("YouTube API error:", response.text)
        return []

    data = response.json().get("items", [])
    results = []

    for item in data:
        video_id = item["id"]["videoId"]
        snippet = item["snippet"]

        results.append({
            "title": snippet["title"],
            "url": f"https://www.youtube.com/watch?v={video_id}",
            "thumbnail": snippet["thumbnails"]["high"]["url"],
            "type": "video",
            "source": "youtube",
            "duration_est": "short" if "shorts" in snippet["title"].lower() else "medium",
            "tags": [snippet["channelTitle"]],
        })

    return results
