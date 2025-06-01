def fetch_spotify_podcasts(query="technology", limit=5):
    return [
        {"title": f"Spotify Podcast {i+1} on {query}", "url": f"https://open.spotify.com/show/{query}{i+1}", "type": "audio"}
        for i in range(limit)
    ]
