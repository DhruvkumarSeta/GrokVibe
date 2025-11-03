from slack_sdk.web.async_client import AsyncWebClient
from app.config import SLACK_BOT_TOKEN
from app.grok import translate
from app.prompts import get_prompt
from app.redis_client import get_user_vibe, set_user_vibe

client = AsyncWebClient(token=SLACK_BOT_TOKEN)

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
            await client.chat_postMessage(
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
    await client.chat_postMessage(
        channel=channel,
        thread_ts=thread_ts,
        text=translated
    )
