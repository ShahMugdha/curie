def fetch_goodreads_books(limit=5):
    return [
        {"title": f"Goodreads Book {i+1}", "url": f"https://goodreads.com/book/show/{i+1}", "type": "book"}
        for i in range(limit)
    ]
