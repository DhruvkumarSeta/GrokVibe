import redis
from app.config import REDIS_URL

# Global Redis connection
r = redis.from_url(REDIS_URL, decode_responses=True)

def get_user_vibe(user_id: str) -> str:
    """Get user's default vibe, fallback to 'pro'."""
    try:
        vibe = r.get(f"user:{user_id}")
        return vibe if vibe else "pro"
    except:
        return "pro"

def set_user_vibe(user_id: str, vibe: str) -> bool:
    """Set user's default vibe."""
    try:
        r.set(f"user:{user_id}", vibe)
        return True
    except:
        return False
