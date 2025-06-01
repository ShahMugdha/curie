# content_selector/content_router.py

from content_sources.substack import fetch_substack_posts
from content_sources.medium import fetch_medium_posts
from content_sources.vsco import fetch_vsco_links
from content_sources.news_mix import fetch_news_articles

def fetch_all_content_by_context(context: dict, limit: int = 20):
    """
    Dynamically choose which content sources to fetch from
    based on user context (intent, tone, topics).
    """
    intent = context.get("intent", "explore")
    tone = context.get("tone", "neutral")
    topics = context.get("topics", [])

    content = []

    # Example mappings — you can refine these
    if intent in ["creative_inspo", "explore"]:
        content += fetch_vsco_links(limit=limit // 5)
        content += fetch_substack_posts(topic="art", limit=limit // 5)

    if intent in ["startup_tech", "career_growth", "ai_learning"]:
        content += fetch_medium_posts(topic=intent, limit=limit // 4)

    if "politics" in topics or "news" in topics or intent == "explore":
        content += fetch_news_articles(limit=limit // 4)

    if not content:
        # fallback
        content += fetch_medium_posts(limit=limit)

    return content[:limit]
