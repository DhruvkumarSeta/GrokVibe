# GrokVibe MVP Development Plan

Based on the [ARCHITECTURE.md](ARCHITECTURE.md), here's a granular task breakdown for building the MVP in 2-3 hours.

---

## Phase 1: Setup & Foundation (45 minutes)

### Task 1: Project Structure & Dependencies
**Objective**: Set up the basic project structure and install all required dependencies.

**Files to create**:
- `/home/dhruv/Documents/grokvibe/.gitignore`
- `/home/dhruv/Documents/grokvibe/requirements.txt`
- `/home/dhruv/Documents/grokvibe/runtime.txt`
- `/home/dhruv/Documents/grokvibe/Procfile`
- `/home/dhruv/Documents/grokvibe/.env.example`
- `/home/dhruv/Documents/grokvibe/app/__init__.py`

**Acceptance Criteria**:
- [ ] All files created with correct content from architecture
- [ ] Virtual environment created: `python -m venv venv`
- [ ] Virtual environment activated
- [ ] Dependencies install without errors: `pip install -r requirements.txt`
- [ ] `pip list` shows all 7 packages installed

**Dependencies**: None (first task)

**Rollback**:
```bash
deactivate
rm -rf venv
rm requirements.txt runtime.txt Procfile .gitignore app/
```

**Estimated time**: 15 minutes

---

### Task 2: Configuration Module
**Objective**: Create the configuration loader that reads environment variables.

**Files to create**:
- `/home/dhruv/Documents/grokvibe/app/config.py`
- `/home/dhruv/Documents/grokvibe/.env` (with placeholder values)

**Acceptance Criteria**:
- [ ] `app/config.py` created with content from section 6 of architecture
- [ ] `.env` created with template from section 4
- [ ] Can import config: `python -c "from app.config import SLACK_BOT_TOKEN; print('Config loaded')"` succeeds
- [ ] Config variables are accessible but show placeholder values

**Dependencies**: Task 1 (project structure)

**Rollback**:
```bash
rm app/config.py .env
```

**Estimated time**: 10 minutes

---

### Task 3: Basic FastAPI App
**Objective**: Create the minimal FastAPI application with health check endpoints.

**Files to create**:
- `/home/dhruv/Documents/grokvibe/app/main.py` (partial - just health endpoints)

**Acceptance Criteria**:
- [ ] `app/main.py` created with FastAPI initialization
- [ ] Root endpoint (`/`) implemented
- [ ] Health endpoint (`/health`) implemented
- [ ] App starts: `uvicorn app.main:app --reload --port 8000`
- [ ] Browser test: `http://localhost:8000` returns `{"message": "GrokVibe is running"}`
- [ ] Browser test: `http://localhost:8000/health` returns `{"status": "ok"}`

**Dependencies**: Task 2 (config module)

**Rollback**:
```bash
# Kill the running server (Ctrl+C)
rm app/main.py
```

**Estimated time**: 15 minutes

---

## Phase 2: Redis Integration (30 minutes)

### Task 4: Upstash Redis Setup
**Objective**: Create Upstash Redis instance and verify connection.

**External setup** (no code changes):
1. Go to upstash.com
2. Sign up / log in
3. Create new Redis database (free tier)
4. Copy connection URL

**Files to modify**:
- `/home/dhruv/Documents/grokvibe/.env` (add real `REDIS_URL`)

**Acceptance Criteria**:
- [ ] Upstash Redis database created
- [ ] Connection URL copied to `.env` as `REDIS_URL`
- [ ] Test connection: `python -c "import redis; from app.config import REDIS_URL; r = redis.from_url(REDIS_URL, decode_responses=True); r.ping(); print('Redis connected')"`
- [ ] Ping succeeds without errors

**Dependencies**: Task 2 (config module)

**Rollback**:
- Remove `REDIS_URL` from `.env`
- Optionally delete Upstash database

**Estimated time**: 10 minutes

---

### Task 5: Redis Client Module
**Objective**: Create Redis client with user preference functions.

**Files to create**:
- `/home/dhruv/Documents/grokvibe/app/redis_client.py`

**Acceptance Criteria**:
- [ ] `app/redis_client.py` created with content from section 10
- [ ] Manual test: Set a test preference
  ```python
  from app.redis_client import set_user_vibe, get_user_vibe
  set_user_vibe("test_user", "cyberpunk")
  print(get_user_vibe("test_user"))  # Should print "cyberpunk"
  ```
- [ ] Test fallback: `print(get_user_vibe("nonexistent"))` returns `"pro"`
- [ ] Verify in Upstash dashboard: Key `user:test_user` exists with value `cyberpunk`

**Dependencies**: Task 4 (Redis setup)

**Rollback**:
```bash
rm app/redis_client.py
# Clean up test data in Upstash dashboard or run:
# python -c "from app.redis_client import r; r.delete('user:test_user')"
```

**Estimated time**: 15 minutes

---

## Phase 3: Grok API Integration (45 minutes)

### Task 6: xAI Grok API Setup
**Objective**: Get Grok API key and verify access.

**External setup**:
1. Go to x.ai/api
2. Sign up / log in
3. Generate API key
4. Copy API key

**Files to modify**:
- `/home/dhruv/Documents/grokvibe/.env` (add real `GROK_API_KEY`)

**Acceptance Criteria**:
- [ ] API key obtained from x.ai
- [ ] `GROK_API_KEY` added to `.env`
- [ ] Verify API key format starts with appropriate prefix
- [ ] Check Grok API docs to confirm endpoint URL is correct

**Dependencies**: Task 2 (config module)

**Rollback**:
- Remove `GROK_API_KEY` from `.env`
- Revoke API key from x.ai dashboard if needed

**Estimated time**: 10 minutes

---

### Task 7: Prompts Module
**Objective**: Create vibe prompt templates.

**Files to create**:
- `/home/dhruv/Documents/grokvibe/app/prompts.py`

**Acceptance Criteria**:
- [ ] `app/prompts.py` created with content from section 8
- [ ] All 5 vibes defined: pro, nerdy, cyberpunk, uk_slang, unfiltered
- [ ] `REVERSE_PROMPT` defined
- [ ] Test import: `python -c "from app.prompts import get_prompt, VIBES; print(len(VIBES))"`
- [ ] Output shows `5` vibes
- [ ] Test prompt generation:
  ```python
  from app.prompts import get_prompt
  prompt = get_prompt("fix this bug", "cyberpunk")
  print("cyberpunk" in prompt.lower() or "neuromancer" in prompt.lower())  # True
  ```

**Dependencies**: None (standalone module)

**Rollback**:
```bash
rm app/prompts.py
```

**Estimated time**: 10 minutes

---

### Task 8: Grok API Client
**Objective**: Create async Grok API client with translation function.

**Files to create**:
- `/home/dhruv/Documents/grokvibe/app/grok.py`

**Acceptance Criteria**:
- [ ] `app/grok.py` created with content from section 9
- [ ] Test translation (create test script `test_grok.py`):
  ```python
  import asyncio
  from app.prompts import get_prompt
  from app.grok import translate

  async def test():
      prompt = get_prompt("this code is broken", "pro")
      result = await translate(prompt)
      print(f"Translation: {result}")
      assert result is not None
      assert len(result) > 0

  asyncio.run(test())
  ```
- [ ] Test succeeds and returns professional translation
- [ ] Test error handling: temporarily break API key in `.env`, verify function returns `None`

**Dependencies**: Task 6 (Grok API key), Task 7 (prompts)

**Rollback**:
```bash
rm app/grok.py test_grok.py
```

**Estimated time**: 20 minutes

---

## Phase 4: Slack Integration (60 minutes)

### Task 9: Slack App Creation
**Objective**: Create Slack app and configure basic settings.

**External setup** (follow section 14 of architecture):
1. Go to api.slack.com/apps
2. Create New App → From scratch
3. Name: "GrokVibe", pick workspace
4. Add Bot Token Scopes: `app_mentions:read`, `chat:write`
5. Install to workspace
6. Copy Bot User OAuth Token
7. Copy Signing Secret from Basic Information

**Files to modify**:
- `/home/dhruv/Documents/grokvibe/.env` (add `SLACK_BOT_TOKEN` and `SLACK_SIGNING_SECRET`)

**Acceptance Criteria**:
- [ ] Slack app created in workspace
- [ ] Bot token scopes added
- [ ] App installed to workspace
- [ ] `SLACK_BOT_TOKEN` added to `.env` (starts with `xoxb-`)
- [ ] `SLACK_SIGNING_SECRET` added to `.env`
- [ ] Bot appears in workspace app list

**Dependencies**: Task 2 (config module)

**Rollback**:
- Remove tokens from `.env`
- Optionally delete Slack app from api.slack.com/apps

**Estimated time**: 15 minutes

---

### Task 10: Slack Handlers Module
**Objective**: Create Slack event handler with message processing logic.

**Files to create**:
- `/home/dhruv/Documents/grokvibe/app/slack_handlers.py`

**Acceptance Criteria**:
- [ ] `app/slack_handlers.py` created with content from section 11
- [ ] Import test: `python -c "from app.slack_handlers import handle_app_mention, client; print('Handlers loaded')"`
- [ ] No import errors
- [ ] Code includes:
  - Bot mention parsing
  - Reverse translation detection (`>>`)
  - `/vibe set` command handling
  - One-time vibe command handling
  - Default vibe retrieval from Redis
  - Translation call to Grok
  - Slack message posting

**Dependencies**: Task 5 (Redis client), Task 8 (Grok client), Task 9 (Slack app)

**Rollback**:
```bash
rm app/slack_handlers.py
```

**Estimated time**: 15 minutes

---

### Task 11: Slack Verification & Event Endpoint
**Objective**: Complete `main.py` with Slack signature verification and event webhook.

**Files to modify**:
- `/home/dhruv/Documents/grokvibe/app/main.py` (add complete content from section 12)

**Acceptance Criteria**:
- [ ] `app/main.py` updated with full content from section 12
- [ ] `verify_slack_request()` function added
- [ ] `/slack/events` POST endpoint added
- [ ] URL verification challenge handler included
- [ ] `app_mention` event handler integrated
- [ ] Server restarts successfully: `uvicorn app.main:app --reload --port 8000`
- [ ] No import or syntax errors

**Dependencies**: Task 10 (Slack handlers), Task 3 (basic FastAPI app)

**Rollback**:
```bash
git checkout app/main.py  # If using git
# OR restore from Task 3 version (just health endpoints)
```

**Estimated time**: 15 minutes

---

### Task 12: Local Testing with ngrok
**Objective**: Expose local server to Slack using ngrok and verify webhook.

**Setup** (follow section 16 of architecture):
1. Install ngrok (ngrok.com/download)
2. Run ngrok: `ngrok http 8000`
3. Copy HTTPS URL (e.g., `https://abc123.ngrok.io`)
4. Update Slack App Event Subscriptions:
   - Enable Events
   - Request URL: `https://abc123.ngrok.io/slack/events`
   - Subscribe to: `app_mention`
   - Save Changes

**Acceptance Criteria**:
- [ ] FastAPI server running: `uvicorn app.main:app --reload --port 8000`
- [ ] ngrok running in separate terminal
- [ ] Slack Event URL verification succeeds (green checkmark)
- [ ] Check ngrok web interface (http://127.0.0.1:4040) shows successful POST to `/slack/events`
- [ ] No signature verification errors in FastAPI logs

**Dependencies**: Task 11 (event endpoint complete)

**Rollback**:
```bash
# Stop ngrok (Ctrl+C)
# Remove Event Subscriptions URL from Slack app
# Keep server running for next task
```

**Estimated time**: 15 minutes

---

## Phase 5: End-to-End Testing (30 minutes)

### Task 13: Basic Translation Test
**Objective**: Test core translation flow with all vibes.

**Testing steps**:
1. Invite bot to test channel: `/invite @GrokVibe`
2. Test basic translation (default vibe):
   - Send: `@grokvibe this code is completely broken`
   - Verify: Bot responds in professional tone
3. Test cyberpunk vibe:
   - Send: `@grokvibe /vibe cyberpunk this code is broken`
   - Verify: Bot responds with cyberpunk style
4. Test each vibe (pro, nerdy, uk_slang, unfiltered)

**Acceptance Criteria**:
- [ ] Bot successfully added to channel
- [ ] Bot responds to @mention within 5 seconds
- [ ] Default translation uses "pro" vibe
- [ ] All 5 vibes produce different translations
- [ ] Translations are relevant to original message
- [ ] Bot posts in thread (if mention was in thread)
- [ ] No error messages in FastAPI logs

**Dependencies**: Task 12 (ngrok setup complete)

**Rollback**:
- No rollback needed (testing only)
- Review logs if failures occur

**Estimated time**: 15 minutes

---

### Task 14: Preference & Reverse Translation Test
**Objective**: Test user preference storage and reverse translation.

**Testing steps**:
1. Set default vibe:
   - Send: `@grokvibe /vibe set cyberpunk`
   - Verify: Bot confirms "Default vibe set to *cyberpunk*"
2. Test default vibe is used:
   - Send: `@grokvibe fix this deployment issue`
   - Verify: Bot responds in cyberpunk style (without specifying vibe)
3. Check Redis:
   - Verify in Upstash dashboard: Key `user:{your_slack_user_id}` = `cyberpunk`
4. Test reverse translation:
   - Send: `@grokvibe >> The implementation requires immediate attention`
   - Verify: Bot translates to casual/raw language
5. Change default vibe:
   - Send: `@grokvibe /vibe set pro`
   - Verify: Subsequent messages use pro vibe

**Acceptance Criteria**:
- [ ] `/vibe set` command works for all vibes
- [ ] Confirmation message appears
- [ ] Redis stores preference correctly
- [ ] Default vibe persists across messages
- [ ] Reverse translation (`>>`) produces casual tone
- [ ] Can change default vibe multiple times
- [ ] Invalid vibes are handled gracefully (falls back to "pro")

**Dependencies**: Task 13 (basic translation working)

**Rollback**:
- Clean up test preferences in Redis:
  ```python
  from app.redis_client import r
  r.delete("user:YOUR_SLACK_USER_ID")
  ```

**Estimated time**: 15 minutes

---

## Phase 6: Deployment (45 minutes)

### Task 15: Railway Deployment Setup
**Objective**: Deploy application to Railway and configure environment.

**Setup** (follow section 13 of architecture):
1. Create Railway account (railway.app)
2. Install Railway CLI or use GitHub integration
3. Create new project
4. Connect GitHub repo (recommended) OR deploy via CLI

**For GitHub integration**:
- Push code to GitHub
- Railway → New Project → Deploy from GitHub
- Select repository

**For CLI deployment**:
```bash
railway login
railway init
railway up
```

5. Add environment variables in Railway dashboard:
   - `SLACK_BOT_TOKEN`
   - `SLACK_SIGNING_SECRET`
   - `GROK_API_KEY`
   - `GROK_API_URL`
   - `REDIS_URL`
   - `PORT` (Railway auto-sets this)

**Acceptance Criteria**:
- [ ] Railway project created
- [ ] Code deployed successfully
- [ ] All environment variables set in Railway
- [ ] Deployment build succeeds
- [ ] Health check passes: `curl https://your-app.railway.app/health`
- [ ] Returns `{"status": "ok"}`
- [ ] Railway logs show "Application startup complete"

**Dependencies**: All previous tasks complete

**Rollback**:
```bash
# Delete Railway deployment
railway down
# Or delete project from Railway dashboard
```

**Estimated time**: 20 minutes

---

### Task 16: Production Slack Configuration
**Objective**: Update Slack app to use Railway URL and verify production bot.

**Setup**:
1. Copy Railway app URL (e.g., `https://grokvibe-production.up.railway.app`)
2. Go to Slack app settings (api.slack.com/apps)
3. Event Subscriptions → Edit Request URL
4. Update to: `https://your-railway-app.up.railway.app/slack/events`
5. Save Changes (should verify successfully)

**Testing**:
1. In Slack channel: `@grokvibe this is a production test`
2. Verify bot responds
3. Check Railway logs for request

**Acceptance Criteria**:
- [ ] Slack Event Subscriptions URL updated to Railway
- [ ] URL verification passes (green checkmark)
- [ ] Bot responds to @mention in Slack
- [ ] Railway logs show incoming POST requests
- [ ] No signature verification errors
- [ ] Response time < 5 seconds
- [ ] All vibes work in production
- [ ] Preference setting works in production

**Dependencies**: Task 15 (Railway deployment)

**Rollback**:
- Update Slack Event URL back to ngrok URL
- Keep Railway deployment for debugging

**Estimated time**: 15 minutes

---

### Task 17: README Documentation
**Objective**: Create user-facing documentation for setup and usage.

**Files to create**:
- `/home/dhruv/Documents/grokvibe/README.md`

**Content to include**:
1. Project overview
2. Features list
3. Quick start guide
4. Environment variables needed
5. Local development setup
6. Deployment instructions
7. Usage examples (Slack commands)
8. Troubleshooting section
9. Success criteria reference

**Acceptance Criteria**:
- [ ] `README.md` created
- [ ] Includes all setup steps from architecture
- [ ] Slack command examples with expected outputs
- [ ] Links to architecture document
- [ ] Troubleshooting section covers common issues
- [ ] Markdown formatting is correct (preview in editor)
- [ ] Ready for GitHub repository

**Dependencies**: Task 16 (production verified)

**Rollback**:
```bash
rm README.md
```

**Estimated time**: 10 minutes

---

## Phase 7: Final Verification (15 minutes)

### Task 18: Complete MVP Testing Checklist
**Objective**: Run through all success criteria from requirements.

**Testing checklist** (from section 20 of architecture):

**Basic functionality**:
- [ ] Bot responds to @mentions
- [ ] Response time < 5 seconds
- [ ] All 5 vibes work (pro, nerdy, cyberpunk, uk_slang, unfiltered)
- [ ] Reverse translation (`>>`) works
- [ ] `/vibe set [vibe]` stores preference
- [ ] Default vibe persists for user
- [ ] Bot posts in threads correctly

**Error handling**:
- [ ] Invalid vibe name falls back to "pro"
- [ ] Grok API timeout shows fallback message
- [ ] Redis failure uses "pro" vibe
- [ ] Bot handles mentions without text gracefully

**Integration tests**:
- [ ] Multiple users can set different preferences
- [ ] Preferences don't conflict between users
- [ ] Bot works in multiple channels
- [ ] Works in threads and main channel

**Performance**:
- [ ] Check Railway metrics (CPU, memory)
- [ ] Review response times in logs
- [ ] Test concurrent requests (2-3 users simultaneously)

**Acceptance Criteria**:
- [ ] All items in checklist pass
- [ ] No critical bugs found
- [ ] Bot is stable for 10+ consecutive messages
- [ ] Ready for real user testing

**Dependencies**: Task 16 (production deployment)

**Rollback**: N/A (testing only)

**Estimated time**: 15 minutes

---

## Summary

**Total Tasks**: 18
**Total Estimated Time**: 2-3 hours
**Phases**: 7

### Critical Path:
```
Task 1 → Task 2 → Task 3 (Basic App)
              ↓
Task 4 → Task 5 (Redis)
              ↓
Task 6 → Task 7 → Task 8 (Grok)
              ↓
Task 9 → Task 10 → Task 11 → Task 12 (Slack)
              ↓
Task 13 → Task 14 (Testing)
              ↓
Task 15 → Task 16 (Deploy)
              ↓
Task 17 → Task 18 (Docs & Final Test)
```

### Time Breakdown by Phase:
- **Phase 1** (Setup): 45 min
- **Phase 2** (Redis): 30 min
- **Phase 3** (Grok): 45 min
- **Phase 4** (Slack): 60 min
- **Phase 5** (Testing): 30 min
- **Phase 6** (Deploy): 45 min
- **Phase 7** (Final): 15 min

**Total**: ~4 hours (including buffer for troubleshooting)

### Quick Start Order:
1. Run Tasks 1-3 together (setup)
2. Task 4-5 (get Redis working)
3. Tasks 6-8 (get Grok working)
4. Tasks 9-12 (integrate Slack)
5. Tasks 13-14 (test thoroughly)
6. Tasks 15-16 (deploy)
7. Tasks 17-18 (document & verify)

### Parallel Opportunities:
- Task 4 (Upstash signup) can happen during Task 1-2
- Task 6 (Grok API signup) can happen during Task 4-5
- Task 9 (Slack app creation) can happen during Task 7-8

This plan ensures each task is:
- ✅ Small enough (15-30 min)
- ✅ Testable immediately
- ✅ Has clear success criteria
- ✅ Can be rolled back safely
- ✅ Builds incrementally toward working MVP

Ready to start with Task 1?
