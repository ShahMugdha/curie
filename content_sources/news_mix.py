# content_sources/news_mix.py
import feedparser

RSS_FEEDS = {
    "bbc_world": "http://feeds.bbci.co.uk/news/world/rss.xml",
    "espn": "https://www.espn.com/espn/rss/news",
    "history_today": "https://www.historytoday.com/rss.xml"
}

def fetch_news_articles(max_items=3):
    all_articles = []
    for label, url in RSS_FEEDS.items():
        feed = feedparser.parse(url)
        for entry in feed.entries[:max_items]:
            all_articles.append({
                "title": entry.title,
                "url": entry.link,
                "source": label,
                "type": "article"
            })
    return all_articles
