import requests

def fetch_reddit(intent, tone):
    subreddit = "technology" if "tech" in intent else "internetisbeautiful"
    url = f"https://www.reddit.com/r/{subreddit}/top/.json?limit=5&t=week"

    headers = {"User-Agent": "curie-agent"}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return []

    data = response.json()
    return [
        {
            "title": post["data"]["title"],
            "url": f"https://reddit.com{post['data']['permalink']}",
            "source": "Reddit",
            "intent": intent,
            "tone": tone,
        }
        for post in data["data"]["children"]
    ]
