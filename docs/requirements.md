# GrokVibe - Requirements Document (MVP)

## Overview
GrokVibe is a Slack/Teams bot that translates user messages between different "vibes" (e.g., professional, cyberpunk) using xAI's Grok API. The MVP focuses on core translation functionality to prove the concept quickly, with minimal features for fast deployment and testing.

### Core Value Proposition
- **Forward Translation**: User inputs raw, chaotic messages; bot remixes them into a chosen vibe while preserving intent.
- **Reverse Translation**: Translate polished "boss-speak" back to raw language.
- **Goal**: Increase engagement in communication channels by making interactions more fun and contextually appropriate.

## Functional Requirements

### 1. Message Translation
- **FR1.1**: Bot must detect and process messages triggered by app mentions (e.g., `@bot message`).
- **FR1.2**: Support forward translation: Remix raw input into specified vibe (default: "pro").
- **FR1.3**: Support reverse translation: Flag messages with ">>" to translate back to raw/unfiltered style.
- **FR1.4**: Vibe options (initial set):
  - Pro: Professional, concise business English.
  - Nerdy: Sci-fi humor, fun but clear.
  - Cyberpunk: Gritty, neon-lit noir.
  - UK Slang: Cheeky British pub chat.
  - Unfiltered: Raw Grok voice (curses optional, toggleable).
- **FR1.5**: Command syntax: `/vibe [vibe] [message]` or default vibe for plain mentions.

### 2. User Preferences
- **FR2.1**: Allow users to set default vibe per channel (e.g., `/vibe set default:cyberpunk`).
- **FR2.2**: Persist preferences in lightweight storage (Redis).

### 3. Error Handling and Fallbacks
- **FR3.1**: Provide fallback response if API fails (e.g., return original message with error note).
- **FR3.2**: Implement basic rate limiting and safe mode (auto-pro for sensitive content).

## Non-Functional Requirements

### 1. Performance
- **NFR1.1**: Translation response time < 5 seconds (API-dependent).
- **NFR1.2**: Support concurrent users in a test channel (no high-scale optimization yet).

### 2. Usability
- **NFR2.1**: Simple, intuitive commands; no complex UI.
- **NFR2.2**: Bot responds in-thread to maintain conversation flow.

### 3. Security
- **NFR3.1**: Secure API keys and tokens via environment variables.
- **NFR3.2**: No data persistence beyond user prefs; comply with Slack/Teams policies.

### 4. Reliability
- **NFR4.1**: Uptime via free-tier hosting; handle basic errors gracefully.

## Technical Requirements

### 1. Tech Stack
- **TR1.1**: Backend: Python with Flask or FastAPI.
- **TR1.2**: AI: xAI Grok API (beta access).
- **TR1.3**: Integration: Slack Bolt SDK (primary); Microsoft Bot Framework (future).
- **TR1.4**: Storage: Redis (free tier).
- **TR1.5**: Hosting: Vercel or Replit (free tier for MVP).

### 2. Dependencies
- **TR2.1**: slack-bolt, requests, python-dotenv, redis.

### 3. API Integration
- **TR3.1**: Grok API endpoint: `https://api.x.ai/v1/chat/completions` (confirm and update as needed).
- **TR3.2**: Payload structure: Model (grok-4 or grok-beta), messages array, max_tokens=150, temperature=0.7.

## MVP Scope
- **In Scope**:
  - Basic translation for Slack.
  - 5 vibe options.
  - Default vibe setting.
  - Reverse translation with ">>" flag.
  - Local testing and free-tier deployment.
- **Out of Scope**:
  - Teams integration.
  - Advanced UI/dashboard.
  - Multi-region localization beyond UK.
  - Paid scaling features.

## Success Criteria
- **SC1**: Deploy to test Slack channel.
- **SC2**: Achieve 5+ positive reactions ("this slaps") on translations.
- **SC3**: No critical bugs in core flow; <10% API failure rate.
- **SC4**: Build and deploy within 1-2 days.

## Assumptions and Risks
- **Assumptions**:
  - xAI Grok API beta access is available and stable.
  - Free tiers suffice for MVP testing.
- **Risks**:
  - API rate limits or changes could delay deployment.
  - User adoption may vary; monitor engagement closely.
  - Mitigations: Fallbacks, logging, iterative testing.

## Next Steps
- Review and approve this document.
- Proceed to implementation per build plan in `idea` file.
- Iterate based on test feedback.