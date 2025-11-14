from supabase import create_client, Client
from config import settings

# Global supabase client instance
supabase: Client = None

def initialize_supabase():
    """Initialize Supabase client - called only when needed"""
    global supabase
    if supabase is None:
        try:
            supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
            print("✅ Supabase initialized successfully")
        except Exception as e:
            print(f"⚠️ Supabase initialization error: {e}")
            print(f"SUPABASE_URL: {settings.SUPABASE_URL}")
            print(f"SUPABASE_KEY: {settings.SUPABASE_KEY[:20]}...")
            raise
    return supabase

def get_supabase() -> Client:
    """Get Supabase client instance - initializes if needed"""
    return initialize_supabase()
