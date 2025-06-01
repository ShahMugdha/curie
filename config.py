import os
from dotenv import load_dotenv

# Load .env into environment
load_dotenv()

class Config:
    # Supabase
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

    # API Keys
    YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
    SOUNDCLOUD_CLIENT_ID = os.getenv("SOUNDCLOUD_CLIENT_ID")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    # Optional checks
    REQUIRED_VARS = [
        "SUPABASE_URL", "SUPABASE_SERVICE_ROLE_KEY",
        "YOUTUBE_API_KEY", "SOUNDCLOUD_CLIENT_ID", "OPENAI_API_KEY"
    ]

    @classmethod
    def validate(cls):
        missing = [var for var in cls.REQUIRED_VARS if getattr(cls, var, None) is None]
        if missing:
            raise EnvironmentError(f"Missing required env vars: {', '.join(missing)}")
