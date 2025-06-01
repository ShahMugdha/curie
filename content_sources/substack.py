def fetch_substack_posts(topic="productivity", limit=5):
    # Substack does not offer a public API; simulated data or scraping required
    return [
        {"title": f"Substack Article {i+1} on {topic}", "url": f"https://substack.com/@{topic}/post{i+1}", "type": "article"}
        for i in range(limit)
    ]
