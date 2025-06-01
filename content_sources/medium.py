def fetch_medium_posts(topic="startup", limit=5):
    # Medium does not have a public API; use RSS or scraping if needed
    return [
        {"title": f"Medium Post {i+1} on {topic}", "url": f"https://medium.com/topic/{topic}/post{i+1}", "type": "article"}
        for i in range(limit)
    ]
