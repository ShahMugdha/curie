from config import Config
import requests

def fetch_youtube_results(query, max_results=5):
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "q": query,
        "maxResults": max_results,
        "key": Config.YOUTUBE_API_KEY,
        "type": "video"
    }
    response = requests.get(url, params=params)
    return response.json()
