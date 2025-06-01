import requests
import time
from typing import List
from config import Config

AUTH_URL = "https://www.reddit.com/api/v1/access_token"
BASE_URL = "https://oauth.reddit.com"
_token_info = {"access_token": None, "expires_at": 0}

def get_reddit_token():
    if _token_info["access_token"] and _token_info["expires_at"] > time.time():
        return _token_info["access_token"]

    auth = requests.auth.HTTPBasicAuth(Config.REDDIT_CLIENT_ID, Config.REDDIT_SECRET)
    data = {"grant_type": "client_credentials"}
    headers = {"User-Agent": Config.REDDIT_USER_AGENT}

    res = requests.post(AUTH_URL, auth=auth, data=data, headers=headers)
    res.raise_for_status()
    token_json = res.json()

    _token_info["access_token"] = token_json["access_token"]
    _token_info["expires_at"] = time.time() + token_json["expires_in"]
    return _token_info["access_token"]

def fetch_reddit_posts(subreddit: str = "interestingasfuck", limit: int = 10) -> List[dict]:
    token = get_reddit_token()
    headers = {
        "Authorization": f"bearer {token}",
        "User-Agent": Config.REDDIT_USER_AGENT
    }

    url = f"{BASE_URL}/r/{subreddit}/hot?limit={limit}"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    posts = response.json()["data"]["children"]

    return [
        {
            "title": post["data"]["title"],
            "url": f"https://reddit.com{post['data']['permalink']}",
            "type": "article",
            "source": "reddit",
            "score": post["data"]["score"]
        }
        for post in posts
    ]
