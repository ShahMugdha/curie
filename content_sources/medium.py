# content_sources/medium.py
import feedparser

MEDIUM_FEEDS = [
    "https://medium.com/feed/topic/technology",
    "https://medium.com/feed/topic/self",
    "https://towardsdatascience.com/feed"
]

def fetch_medium_posts(max_items=5):
    posts = []
    for url in MEDIUM_FEEDS:
        feed = feedparser.parse(url)
        for entry in feed.entries[:max_items]:
            posts.append({
                "title": entry.title,
                "url": entry.link,
                "source": "Medium",
                "summary": entry.get("summary", ""),
                "type": "article"
            })
    return posts
