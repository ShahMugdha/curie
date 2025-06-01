import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

class Config:
    # Supabase
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

    # API Keys
    YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
    SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
    SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
    REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
    REDDIT_SECRET = os.getenv("REDDIT_SECRET")
    REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT")
    GOODREADS_API_KEY = os.getenv("GOODREADS_API_KEY")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    # Required variable check
    REQUIRED_VARS = [
        "SUPABASE_URL", "SUPABASE_SERVICE_ROLE_KEY",
        "YOUTUBE_API_KEY", "OPENAI_API_KEY"
    ]

    @classmethod
    def validate(cls):
        missing = [var for var in cls.REQUIRED_VARS if getattr(cls, var, None) is None]
        if missing:
            raise EnvironmentError(f"Missing required env vars: {', '.join(missing)}")

    @classmethod
    def get(cls, key: str):
        return getattr(cls, key, None)
