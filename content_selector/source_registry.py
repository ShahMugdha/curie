from typing import Callable, Dict, List
from content_sources.medium import fetch_medium_posts
from content_sources.substack import fetch_substack_posts
from content_sources.vsco import fetch_vsco_links
from content_sources.news_mix import fetch_news_articles
from content_sources.youtube import fetch_youtube_videos
from content_sources.reddit import fetch_reddit_posts
from content_sources.hackernews import fetch_hackernews_posts
from content_sources.goodreads import fetch_goodreads_books
from content_sources.spotify import fetch_spotify_episodes

CATEGORY_SOURCE_MAP: Dict[str, List[Callable[[int], List[dict]]]] = {
    "art": [
        lambda limit: fetch_vsco_links(limit),
        lambda limit: fetch_substack_posts("art", limit),
        lambda limit: fetch_youtube_videos("art inspiration", limit),
    ],
    "tech": [
        lambda limit: fetch_medium_posts("startup_tech", limit),
        lambda limit: fetch_hackernews_posts(limit),
        lambda limit: fetch_youtube_videos("tech news", limit),
    ],
    "ai": [
        lambda limit: fetch_medium_posts("ai_learning", limit),
        lambda limit: fetch_youtube_videos("AI concepts", limit),
        lambda limit: fetch_substack_posts("ml", limit),
    ],
    "news": [
        lambda limit: fetch_news_articles(limit),
        lambda limit: fetch_youtube_videos("current events", limit),
        lambda limit: fetch_reddit_posts(["worldnews", "politics"], limit // 2),
    ],
    "books": [
        lambda limit: fetch_youtube_videos("book review", limit),
        lambda limit: fetch_goodreads_books(limit),
        lambda limit: fetch_substack_posts("literature", limit),
    ],
    "sports": [
        lambda limit: fetch_youtube_videos("sports highlights", limit),
        lambda limit: fetch_reddit_posts(["sports", "soccer"], limit // 2),
        lambda limit: fetch_substack_posts("sports", limit),
    ],
    "music": [
        lambda limit: fetch_spotify_episodes("music", limit),
        lambda limit: fetch_youtube_videos("top music", limit),
        lambda limit: fetch_reddit_posts(["music", "listentothis"], limit // 2),
    ],
    "cinema": [
        lambda limit: fetch_youtube_videos("film essays", limit),
        lambda limit: fetch_reddit_posts(["movies", "TrueFilm"], limit // 2),
        lambda limit: fetch_substack_posts("cinema", limit),
    ],
}
