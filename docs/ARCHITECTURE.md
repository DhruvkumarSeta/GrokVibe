# GrokVibe - MVP Architecture Document

## Executive Summary
GrokVibe is a Slack bot that translates messages between different "vibes" using xAI's Grok API. This architecture focuses on shipping fast with minimal complexity - just the essentials to get the bot working.

**MVP Goal**: Message in → Grok translate → Message out. That's it.

---

## 1. File & Folder Structure

```
grokvibe/
├── .env                          # Environment variables (not in git)
├── .env.example                  # Template for environment variables
├── .gitignore                    # Git ignore rules
├── requirements.txt              # Python dependencies (minimal)
├── runtime.txt                   # Python version for Railway
├── Procfile                      # Railway deployment config
├── README.md                     # Setup instructions
├── requirements.md               # Requirements specification
├── ARCHITECTURE.md               # This file
│
└── app/
    ├── __init__.py              # Package init
    ├── main.py                  # FastAPI app + all routes
    ├── config.py                # Configuration (loads .env)
    ├── grok.py                  # Grok API client
    ├── redis_client.py          # Redis operations
    ├── slack_handlers.py        # Slack event handlers
    └── prompts.py               # Vibe prompt templates
```

### Why So Simple?
- **8 files total** - Easy to understand and debug
- **No deep nesting** - Everything in one `app/` folder
- **Single responsibility** - Each file does one thing
- **Fast to build** - Can finish in 2-3 hours

---

## 2. System Architecture

### Component Flow

```
User in Slack
    ↓
@grokvibe fix this mess
    ↓
Slack sends webhook → FastAPI (/slack/events)
    ↓
Verify Slack signature
    ↓
Extract message text
    ↓
Check Redis for user's default vibe (fallback: "pro")
    ↓
Build prompt with vibe template
    ↓
Call Grok API
    ↓
Post translated message back to Slack
    ↓
Done!
```

### Error Handling (Simple)
- **Grok API fails?** → Return original message with note
- **Redis fails?** → Use default vibe ("pro")
- **Slack verification fails?** → Return 401
- **Anything else?** → Log error, return original message

---

## 3. API Endpoints

```
GET  /              → "GrokVibe is running"
GET  /health        → {status: "ok"}
POST /slack/events  → Main webhook for Slack events
```

That's it. No other endpoints needed for MVP.

---

## 4. Environment Variables

### `.env` (Required Variables Only)

```bash
# Slack
SLACK_BOT_TOKEN=xoxb-your-bot-token
SLACK_SIGNING_SECRET=your-signing-secret

# Grok API
GROK_API_KEY=xai-your-api-key
GROK_API_URL=https://api.x.ai/v1/chat/completions

# Redis (Upstash)
REDIS_URL=redis://default:password@host:port

# Server
PORT=8000
```

### `.env.example`

```bash
SLACK_BOT_TOKEN=xoxb-...
SLACK_SIGNING_SECRET=...
GROK_API_KEY=xai-...
GROK_API_URL=https://api.x.ai/v1/chat/completions
REDIS_URL=redis://localhost:6379
PORT=8000
```

---

## 5. Dependencies (Minimal)

### `requirements.txt`

```txt
# Core
fastapi==0.109.0
uvicorn[standard]==0.27.0
python-dotenv==1.0.0

# Slack
slack-sdk==3.26.2

# HTTP client for Grok
httpx==0.26.0

# Redis
redis==5.0.1

# Security (for Slack signature verification)
cryptography==42.0.0
```

**7 packages total.** No testing, no logging libraries, no extras.

### `runtime.txt`

```
python-3.11
```

---

## 6. Configuration (`app/config.py`)

```python
import os
from dotenv import load_dotenv

load_dotenv()

# Slack
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_SIGNING_SECRET = os.getenv("SLACK_SIGNING_SECRET")

# Grok
GROK_API_KEY = os.getenv("GROK_API_KEY")
GROK_API_URL = os.getenv("GROK_API_URL", "https://api.x.ai/v1/chat/completions")

# Redis
REDIS_URL = os.getenv("REDIS_URL")

# Server
PORT = int(os.getenv("PORT", 8000))
```

Simple. No Pydantic, no validation. Just read environment variables.

---

## 7. Redis Schema (Minimal)

### User Preferences

```
Key: user:{slack_user_id}
Type: String
Value: vibe name (e.g., "cyberpunk")

Example:
  SET user:U12345 "cyberpunk"
  GET user:U12345  → "cyberpunk"
```

That's it. One key per user. No hashes, no complex structures.

---

## 8. Vibe Prompts (`app/prompts.py`)

```python
VIBES = {
    "pro": """Translate this to professional, concise business English. Keep it direct and actionable.

Message: {text}

Professional version:""",

    "nerdy": """Remix this with sci-fi/tech humor. Keep it clear but fun. Think Star Trek or general nerd culture.

Message: {text}

Nerdy version:""",

    "cyberpunk": """Transform this to cyberpunk style: gritty, neon-lit, street slang. Think Neuromancer or Blade Runner.

Message: {text}

Cyberpunk version:""",

    "uk_slang": """Rewrite in cheeky British pub slang. Use 'proper', 'mate', 'bollocks', etc. Keep it work-appropriate.

Message: {text}

British version:""",

    "unfiltered": """Keep the raw, honest voice. Be direct and clear, drop corporate speak.

Message: {text}

Unfiltered version:"""
}

REVERSE_PROMPT = """Translate this formal message back to raw, unfiltered language. Be direct, drop the polish.

Message: {text}

Raw version:"""

def get_prompt(text: str, vibe: str = "pro", reverse: bool = False) -> str:
    if reverse:
        return REVERSE_PROMPT.format(text=text)
    template = VIBES.get(vibe, VIBES["pro"])
    return template.format(text=text)
```

---

## 9. Grok Client (`app/grok.py`)

```python
import httpx
from app.config import GROK_API_KEY, GROK_API_URL

async def translate(prompt: str) -> str:
    """Call Grok API and return translated text."""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                GROK_API_URL,
                headers={
                    "Authorization": f"Bearer {GROK_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "grok-beta",
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": 150,
                    "temperature": 0.7
                }
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print(f"Grok API error: {e}")
        return None
```

---

## 10. Redis Client (`app/redis_client.py`)

```python
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
```

---

## 11. Slack Handlers (`app/slack_handlers.py`)

```python
from slack_sdk import WebClient
from app.config import SLACK_BOT_TOKEN
from app.grok import translate
from app.prompts import get_prompt
from app.redis_client import get_user_vibe, set_user_vibe

client = WebClient(token=SLACK_BOT_TOKEN)

async def handle_app_mention(event: dict):
    """Handle @grokvibe mentions."""
    text = event.get("text", "")
    user_id = event.get("user")
    channel = event.get("channel")
    thread_ts = event.get("thread_ts") or event.get("ts")

    # Remove bot mention
    text = text.split(">", 1)[-1].strip()

    # Check for reverse translation
    reverse = text.startswith(">>")
    if reverse:
        text = text[2:].strip()

    # Check for vibe command: /vibe set pro
    if text.startswith("/vibe set "):
        vibe = text.split()[-1].lower()
        if vibe in ["pro", "nerdy", "cyberpunk", "uk_slang", "unfiltered"]:
            set_user_vibe(user_id, vibe)
            client.chat_postMessage(
                channel=channel,
                thread_ts=thread_ts,
                text=f"Default vibe set to *{vibe}*"
            )
            return

    # Check for one-time vibe: /vibe cyberpunk fix this mess
    vibe = None
    if text.startswith("/vibe "):
        parts = text.split(maxsplit=2)
        if len(parts) >= 3:
            vibe = parts[1].lower()
            text = parts[2]

    # Get user's default vibe if not specified
    if not vibe:
        vibe = get_user_vibe(user_id)

    # Build prompt and translate
    prompt = get_prompt(text, vibe, reverse)
    translated = await translate(prompt)

    # Fallback if translation fails
    if not translated:
        translated = f"{text}\n\n_[Translation unavailable - showing original]_"

    # Post to Slack
    client.chat_postMessage(
        channel=channel,
        thread_ts=thread_ts,
        text=translated
    )
```

---

## 12. Main App (`app/main.py`)

```python
import hmac
import hashlib
import time
from fastapi import FastAPI, Request, HTTPException
from app.config import SLACK_SIGNING_SECRET
from app.slack_handlers import handle_app_mention

app = FastAPI()

def verify_slack_request(body: bytes, timestamp: str, signature: str) -> bool:
    """Verify request is from Slack."""
    if abs(time.time() - int(timestamp)) > 60 * 5:
        return False

    sig_basestring = f"v0:{timestamp}:{body.decode()}"
    my_signature = "v0=" + hmac.new(
        SLACK_SIGNING_SECRET.encode(),
        sig_basestring.encode(),
        hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(my_signature, signature)

@app.get("/")
def root():
    return {"message": "GrokVibe is running"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/slack/events")
async def slack_events(request: Request):
    body = await request.body()
    headers = request.headers

    # Verify Slack signature
    timestamp = headers.get("X-Slack-Request-Timestamp", "")
    signature = headers.get("X-Slack-Signature", "")

    if not verify_slack_request(body, timestamp, signature):
        raise HTTPException(status_code=401, detail="Invalid signature")

    # Parse JSON
    data = await request.json()

    # Handle URL verification challenge
    if data.get("type") == "url_verification":
        return {"challenge": data.get("challenge")}

    # Handle app_mention events
    event = data.get("event", {})
    if event.get("type") == "app_mention":
        await handle_app_mention(event)

    return {"ok": True}
```

---

## 13. Deployment

### `Procfile`

```
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### `.gitignore`

```
__pycache__/
*.pyc
.env
.DS_Store
venv/
env/
```

### Railway Setup

1. Create account at railway.app
2. New Project → Deploy from GitHub
3. Add environment variables (from .env)
4. Deploy automatically
5. Copy the Railway URL (e.g., `https://grokvibe-production.up.railway.app`)

---

## 14. Slack App Setup

### Step 1: Create Slack App
1. Go to api.slack.com/apps
2. Create New App → From scratch
3. Name: "GrokVibe"
4. Pick your workspace

### Step 2: Bot Token Scopes
Go to **OAuth & Permissions**, add these scopes:
- `app_mentions:read` - Listen for @mentions
- `chat:write` - Send messages
- `channels:history` - Read messages (optional)

### Step 3: Install to Workspace
- Click "Install to Workspace"
- Copy the **Bot User OAuth Token** → `SLACK_BOT_TOKEN`

### Step 4: Event Subscriptions
1. Enable Events
2. Request URL: `https://your-railway-url.up.railway.app/slack/events`
3. Subscribe to bot events:
   - `app_mention` - When bot is mentioned
4. Save Changes

### Step 5: Get Signing Secret
- Go to **Basic Information**
- Copy **Signing Secret** → `SLACK_SIGNING_SECRET`

### Step 6: Invite Bot to Channel
In Slack: `/invite @GrokVibe`

---

## 15. Upstash Redis Setup

1. Go to upstash.com
2. Create account (free tier)
3. Create Redis Database
4. Copy the connection URL → `REDIS_URL`

Format: `redis://default:password@host:port`

---

## 16. Testing Locally

### Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file (copy from .env.example and fill in values)
cp .env.example .env
nano .env

# Run locally
uvicorn app.main:app --reload --port 8000
```

### Expose to Slack (ngrok)
```bash
# Install ngrok: https://ngrok.com/download
ngrok http 8000

# Copy the HTTPS URL (e.g., https://abc123.ngrok.io)
# Update Slack Event Subscriptions URL to: https://abc123.ngrok.io/slack/events
```

### Test Translation
1. Go to Slack channel where bot is invited
2. Type: `@grokvibe this code is totally broken`
3. Bot should respond with professional version
4. Try: `@grokvibe /vibe cyberpunk this code is broken`
5. Try: `@grokvibe /vibe set cyberpunk` (sets default)

---

## 17. Command Reference

### For Users in Slack

```
# Basic translation (uses default vibe)
@grokvibe your message here

# One-time vibe
@grokvibe /vibe cyberpunk your message here

# Set default vibe
@grokvibe /vibe set cyberpunk

# Reverse translation (formal → raw)
@grokvibe >> The implementation requires immediate attention
```

### Available Vibes
- `pro` - Professional business English
- `nerdy` - Sci-fi/tech humor
- `cyberpunk` - Gritty noir style
- `uk_slang` - British pub chat
- `unfiltered` - Raw and direct

---

## 18. Troubleshooting

### Bot doesn't respond
1. Check Railway logs: `railway logs` or dashboard
2. Verify bot is invited to channel: `/invite @GrokVibe`
3. Check Slack Event Subscriptions URL is correct
4. Verify environment variables are set

### "Invalid signature" error
- Check `SLACK_SIGNING_SECRET` is correct (from Slack app Basic Information)
- Ensure timestamp validation works (server time must be accurate)

### Grok API errors
- Verify `GROK_API_KEY` is valid
- Check API URL is correct
- Look for error messages in logs

### Redis connection fails
- Verify `REDIS_URL` format: `redis://default:password@host:port`
- Check Upstash dashboard for database status
- Ensure TLS is included in URL if required

---

## 19. What We SKIPPED for MVP

These are intentionally NOT included to ship faster:

❌ Rate limiting
❌ Response caching
❌ Metrics/analytics
❌ Safe mode/content filtering
❌ Unit tests
❌ Structured logging
❌ Advanced error handling
❌ Channel-level preferences
❌ Custom vibes
❌ Multi-language support

**Add these ONLY after MVP works and has users.**

---

## 20. Success Criteria

MVP is successful when:
- ✅ Deploy to Slack workspace
- ✅ Bot responds to @mentions within 5 seconds
- ✅ All 5 vibes work correctly
- ✅ Users can set default vibe
- ✅ Reverse translation works with `>>`
- ✅ Get 5+ positive reactions on translations

---

## 21. Next Steps After MVP

1. **Monitor usage** - Which vibes are most popular?
2. **Gather feedback** - What do users want?
3. **Add features** - Based on actual usage, not assumptions
4. **Scale** - Only if needed (free tier handles 10-20 users easily)

---

## Summary

**Total files to create: 8**
**Total dependencies: 7**
**Deployment platforms: 2** (Railway + Upstash)
**Time to build: 2-3 hours**

This is a lean, focused MVP. No over-engineering. Ship fast, learn, iterate.

**Ready to code?** Start with `app/config.py` and work through each file!
