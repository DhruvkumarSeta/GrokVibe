import redis
from app.config import REDIS_URL

# Lazy Redis connection - only connect when env var is set
_redis_client = None

def get_redis():
    """Get or create Redis connection (lazy initialization)."""
    global _redis_client
    if _redis_client is None and REDIS_URL:
        _redis_client = redis.from_url(REDIS_URL, decode_responses=True)
    return _redis_client

def get_user_vibe(user_id: str) -> str:
    """Get user's default vibe, fallback to 'pro'."""
    try:
        r = get_redis()
        if r is None:
            return "pro"
        vibe = r.get(f"user:{user_id}")
        return vibe if vibe else "pro"
    except:
        return "pro"

def set_user_vibe(user_id: str, vibe: str) -> bool:
    """Set user's default vibe."""
    try:
        r = get_redis()
        if r is None:
            return False
        r.set(f"user:{user_id}", vibe)
        return True
    except:
        return False
