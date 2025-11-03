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

    # Respond to Slack immediately
    event_type = data.get("event", {}).get("type")

    # Process app_mention in background
    if event_type == "app_mention":
        import asyncio
        event = data.get("event", {})
        asyncio.create_task(handle_app_mention(event))

    return {"ok": True}
