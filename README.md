# GrokVibe

A Slack bot that translates messages between different "vibes" using xAI's Grok API.

**Status**: ✅ Deployed and running on Railway
**Production URL**: https://web-production-f9d41.up.railway.app

## Features

- **5 Translation Vibes**: Professional, Nerdy, Cyberpunk, UK Slang, Unfiltered
- **Reverse Translation**: Convert formal text back to casual (`>>`)
- **User Preferences**: Set default vibes with `/vibe set [vibe]`
- **One-time Override**: `/vibe [vibe] [message]`

## Tech Stack

- **Backend**: FastAPI (Python 3.12)
- **AI**: xAI Grok API (grok-2-1212)
- **Database**: Upstash Redis
- **Integration**: Slack Events API
- **Hosting**: Railway

## Quick Start

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

## Usage in Slack

**Translate with default vibe:**
```
@grokvibe fix this mess
```

**One-time vibe override:**
```
@grokvibe /vibe cyberpunk make this sound cool
```

**Set default vibe:**
```
@grokvibe /vibe set nerdy
```

**Reverse translation (formal → casual):**
```
@grokvibe >> I would appreciate your assistance with this matter
```

## Deployment

See [docs/TASKS.md](docs/TASKS.md) for full deployment instructions (Task #15-17).

### Railway Deployment

1. Push to GitHub
2. Connect Railway to your repo
3. Add environment variables in Railway dashboard
4. Deploy automatically on push

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

- [ARCHITECTURE.md](docs/ARCHITECTURE.md) - System design
- [TASKS.md](docs/TASKS.md) - Development tasks
- [STATUS.md](docs/STATUS.md) - Current progress
- [requirements.md](docs/requirements.md) - MVP requirements

## License

MIT
