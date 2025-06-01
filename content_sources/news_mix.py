def fetch_news_articles(limit=5):
    return [
        {"title": f"Top News {i+1}", "url": f"https://news.ycombinator.com/item?id={1000+i}", "type": "news"}
        for i in range(limit)
    ]
