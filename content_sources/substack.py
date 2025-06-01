# content_sources/substack.py
import feedparser

SUBSTACK_FEEDS = [
    "https://noahpinion.substack.com/feed",
    "https://slowboring.substack.com/feed",
    "https://every.to/feed"
]

def fetch_substack_posts(max_items=5):
    articles = []
    for feed_url in SUBSTACK_FEEDS:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries[:max_items]:
            articles.append({
                "title": entry.title,
                "url": entry.link,
                "source": "Substack",
                "summary": entry.summary,
                "type": "article"
            })
    return articles
