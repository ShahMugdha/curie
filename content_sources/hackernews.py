def fetch_hackernews_stories(limit=5):
    return [
        {"title": f"Hacker News Story {i+1}", "url": f"https://news.ycombinator.com/item?id={2000+i}", "type": "article"}
        for i in range(limit)
    ]
