from config import Config
from supabase import create_client

Config.validate()  # Optional safety check

supabase = create_client(Config.SUPABASE_URL, Config.SUPABASE_SERVICE_ROLE_KEY)
