# GrokVibe

A Slack bot that translates messages between different "vibes" using xAI's Grok API.

**Want to add this to your own Slack workspace?** Follow the [Quick Setup Guide](#quick-setup-guide) below - it takes ~15 minutes!

> 💡 **This is an MVP!** See [VISION.md](docs/VISION.md) for the full roadmap: automatic translation of ALL messages, browser extensions, and a personalized communication layer for modern workspaces.

## Features

- **5 Translation Vibes**: Professional, Nerdy, Cyberpunk, UK Slang, Unfiltered
- **Reverse Translation**: Convert formal text back to casual (`>>`)
- **User Preferences**: Set default vibes with `/vibe set [vibe]`
- **One-time Override**: `/vibe [vibe] [message]`

## Live Demo

Try these commands in any Slack workspace where you've installed the bot:

**Translate with default vibe:**
```
@grokvibe fix this mess
```

**One-time vibe override:**
```
@grokvibe /vibe cyberpunk make this sound cool
```

**Set your default vibe:**
```
@grokvibe /vibe set nerdy
```

**Reverse translation (formal → casual):**
```
@grokvibe >> I would appreciate your assistance with this matter
```

## Tech Stack

- **Backend**: FastAPI (Python 3.12)
- **AI**: xAI Grok API (grok-2-1212)
- **Database**: Upstash Redis (free tier)
- **Integration**: Slack Events API
- **Hosting**: Railway (free tier available)

---

## Quick Setup Guide

Follow these steps to add GrokVibe to your own Slack workspace. **Total time: ~15 minutes.**

### Step 1: Get Your API Keys (5 min)

#### 1.1 Get Grok API Key
1. Go to [x.ai/api](https://x.ai/api)
2. Sign up and get your API key (starts with `xai-`)
3. Add credits (minimum $5 recommended for testing)

#### 1.2 Create Upstash Redis Database
1. Go to [upstash.com](https://upstash.com) and sign up (free tier available)
2. Create a new Redis database
3. Copy the connection URL (starts with `rediss://`)

#### 1.3 Create Slack App
1. Go to [api.slack.com/apps](https://api.slack.com/apps)
2. Click **"Create New App"** → **"From scratch"**
3. Name it "GrokVibe" and select your workspace
4. Under **"OAuth & Permissions"**, add these Bot Token Scopes:
   - `app_mentions:read`
   - `chat:write`
5. Click **"Install to Workspace"**
6. Copy the **Bot User OAuth Token** (starts with `xoxb-`)
7. Under **"Basic Information"**, copy the **Signing Secret**

### Step 2: Deploy to Railway (5 min)

#### 2.1 Fork This Repository
1. Click the **Fork** button on GitHub
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/grokvibe.git`

#### 2.2 Deploy to Railway
1. Go to [railway.app](https://railway.app) and sign up with GitHub
2. Click **"New Project"** → **"Deploy from GitHub repo"**
3. Select your forked `grokvibe` repository
4. Railway will auto-detect Python and start deploying

#### 2.3 Add Environment Variables in Railway
In the Railway dashboard, go to **Variables** and add:

```bash
SLACK_BOT_TOKEN=xoxb-your-token-here
SLACK_SIGNING_SECRET=your-signing-secret-here
GROK_API_KEY=xai-your-key-here
GROK_API_URL=https://api.x.ai/v1/chat/completions
REDIS_URL=rediss://your-upstash-url-here
```

Railway will automatically redeploy with these variables.

### Step 3: Connect Slack to Railway (5 min)

#### 3.1 Get Your Railway URL
1. In Railway dashboard, click **"Settings"** → **"Domains"**
2. Click **"Generate Domain"**
3. Copy your app URL (e.g., `https://your-app.up.railway.app`)

#### 3.2 Configure Slack Event Subscriptions
1. Go back to [api.slack.com/apps](https://api.slack.com/apps)
2. Select your "GrokVibe" app
3. Click **"Event Subscriptions"** in the sidebar
4. Toggle **"Enable Events"** to ON
5. In **"Request URL"**, enter: `https://your-app.up.railway.app/slack/events`
6. Wait for the green **"Verified ✓"** checkmark
7. Under **"Subscribe to bot events"**, add: `app_mention`
8. Click **"Save Changes"**

### Step 4: Test in Slack! (1 min)

1. Open your Slack workspace
2. In any channel, invite the bot: `/invite @grokvibe`
3. Try a command: `@grokvibe this is a test`
4. The bot should respond with a professional translation!

---

## Available Vibes

| Vibe | Description | Example |
|------|-------------|---------|
| `pro` | Professional, business-ready | "I would appreciate your assistance" |
| `nerdy` | Tech/sci-fi references | "Engaging warp drive humor protocol" |
| `cyberpunk` | Edgy, hacker aesthetic | "Jack into the matrix, choom" |
| `uk_slang` | British colloquialisms | "Brilliant! Let's crack on" |
| `unfiltered` | Raw, casual tone | "Yeah, let's just do it" |

---

## Local Development (Optional)

Want to run locally for development?

### 1. Install Dependencies

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment

Copy `.env.example` to `.env` and fill in:

```bash
SLACK_BOT_TOKEN=xoxb-...
SLACK_SIGNING_SECRET=...
GROK_API_KEY=xai-...
GROK_API_URL=https://api.x.ai/v1/chat/completions
REDIS_URL=rediss://default:password@host.upstash.io:6379
PORT=8000
```

### 3. Run Locally

```bash
uvicorn app.main:app --reload --port 8000
```

### 4. Expose with ngrok

```bash
ngrok http 8000
```

Use the ngrok URL in Slack Event Subscriptions for local testing.

---

## Troubleshooting

### Bot doesn't respond
- Check Railway logs for errors
- Verify all environment variables are set correctly
- Ensure Slack Event Subscriptions URL is verified (green checkmark)
- Make sure bot is invited to the channel: `/invite @grokvibe`

### "Invalid signature" errors
- Double-check your `SLACK_SIGNING_SECRET` in Railway
- Ensure you copied the entire secret correctly

### Grok API errors
- Verify your `GROK_API_KEY` is correct (starts with `xai-`)
- Check you have sufficient credits at [x.ai](https://x.ai)
- Confirm `GROK_API_URL` is set to `https://api.x.ai/v1/chat/completions`

### Redis connection issues
- Ensure `REDIS_URL` starts with `rediss://` (double 's' for SSL)
- Verify the URL is from Upstash and includes credentials
- Check Upstash dashboard to confirm database is active

### Railway deployment fails
- Check Railway build logs for specific errors
- Verify `requirements.txt` and `runtime.txt` are present
- Ensure `Procfile` exists with: `web: uvicorn app.main:app --host 0.0.0.0 --port $PORT`

---

## Cost Estimate

All services offer free tiers suitable for personal/testing use:

| Service | Free Tier | Cost After Free Tier |
|---------|-----------|---------------------|
| Railway | 500 hours/month | ~$5/month for hobby projects |
| Upstash Redis | 10,000 commands/day | Pay per command (~$0.20/10K) |
| xAI Grok API | No free tier | ~$5 per million tokens |

**Estimated monthly cost for light usage**: $5-10/month

---

## Advanced Usage

### Custom Vibes

Want to add your own vibe? Edit `app/prompts.py`:

```python
VIBE_PROMPTS = {
    "pro": "...",
    "nerdy": "...",
    "your_custom_vibe": "Translate this into [your style description]",
}
```

Then redeploy to Railway (auto-deploys on git push).

### Rate Limiting

For production use with many users, consider adding rate limiting:
```bash
pip install slowapi
```

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for implementation details.

## Project Structure

```
grokvibe/
├── app/                  # Application code
│   ├── main.py          # FastAPI app & Slack webhook
│   ├── config.py        # Environment variables
│   ├── grok.py          # Grok API client
│   ├── redis_client.py  # Redis operations
│   ├── slack_handlers.py # Event processing
│   └── prompts.py       # Vibe templates
├── tests/               # Test scripts
├── docs/                # Documentation
├── requirements.txt     # Python dependencies
├── runtime.txt          # Python version (3.12)
└── Procfile            # Railway deployment config
```

## Documentation

- **[VISION.md](docs/VISION.md)** - Product vision and roadmap 🚀
- [ARCHITECTURE.md](docs/ARCHITECTURE.md) - System design
- [TASKS.md](docs/TASKS.md) - Development tasks
- [STATUS.md](docs/STATUS.md) - Current progress
- [requirements.md](docs/requirements.md) - MVP requirements

## License

MIT
