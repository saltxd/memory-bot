# Memory Bot

### Your Personal AI Memory System

**Log anything. Search naturally. Remember everything.**

Memory Bot is a self-hosted Discord bot that acts as your second brain. Log thoughts, notes, meetings, ideas—anything—and retrieve them later using natural language search or AI-powered questions.

```
You:    /log Met with Sarah about Q1 roadmap. She wants dark mode prioritized.
Bot:    Logged! (#42) You now have 847 memories stored.

You:    /ask What did Sarah say about Q1?
Bot:    Sarah mentioned she wants dark mode prioritized for Q1 [#42].
        This aligns with the user feedback you logged last week [#38].
```

---

## Features

| Command | Description |
|---------|-------------|
| `/log <text>` | Save anything to your memory bank |
| `/search <query>` | Find memories by keyword (instant full-text search) |
| `/ask <question>` | Ask questions and get AI answers with citations |
| `/stats` | View your memory count and last entry |
| `/help` | Quick command reference |

**What makes it great:**

- **Instant Search** — SQLite FTS5 full-text search finds memories in milliseconds
- **AI-Powered Recall** — Ask natural questions like "What did I decide about the API?"
- **Citation Support** — AI responses reference specific memories by ID so you can verify
- **Timezone Aware** — Dates display in your local timezone
- **Zero Maintenance** — Single SQLite file, no external databases
- **Privacy First** — Self-hosted, your data never leaves your server

---

## Quick Start

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) installed and running
- A Discord account
- An [Anthropic API key](https://console.anthropic.com/)

### 1. Clone & Configure

```bash
git clone https://github.com/YOUR_USERNAME/memory-bot.git
cd memory-bot
cp .env.example .env
```

Edit `.env` and add your credentials:

```env
DISCORD_TOKEN=your_discord_bot_token
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

> Need help getting these? See the [detailed setup guide](SETUP.md).

### 2. Start the Bot

```bash
docker compose up -d
```

### 3. Invite to Your Server

Use this URL template (replace `YOUR_CLIENT_ID` with your bot's Application ID):

```
https://discord.com/api/oauth2/authorize?client_id=YOUR_CLIENT_ID&permissions=2147485696&scope=bot%20applications.commands
```

**That's it!** Start logging with `/log` and searching with `/search`.

---

## Example Usage

**Daily logging:**
```
/log Shipped the new auth flow. Took 3 days, but tests are passing.
/log Idea: add keyboard shortcuts to the dashboard
/log 1:1 with Mike - he's blocked on the API docs, needs examples
```

**Finding information:**
```
/search auth flow
/search Mike blocked
```

**Asking questions:**
```
/ask What features did I ship this week?
/ask What's blocking Mike?
/ask What ideas have I logged for the dashboard?
```

---

## Why Self-Host?

| Benefit | Description |
|---------|-------------|
| **Privacy** | Your thoughts stay on your server. No third-party access. |
| **Cost Effective** | Pay only for Claude API usage (~$0.001 per query with Haiku) |
| **Customizable** | Modify prompts, add commands, integrate with your tools |
| **No Limits** | Store unlimited memories, no subscription tiers |
| **Data Ownership** | Export anytime—it's just a SQLite file |

---

## Configuration

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `DISCORD_TOKEN` | Yes | — | Bot token from Discord Developer Portal |
| `ANTHROPIC_API_KEY` | Yes | — | API key from Anthropic Console |
| `ANTHROPIC_MODEL` | No | `claude-3-5-haiku-latest` | Claude model for `/ask` |
| `CLAUDE_MAX_TOKENS` | No | `1024` | Max tokens in AI responses |
| `TIMEZONE` | No | `America/Denver` | Your timezone for date display |
| `DEV_GUILD_ID` | No | — | Server ID for instant command sync |

See [.env.example](.env.example) for detailed descriptions.

---

## System Requirements

| Resource | Minimum | Recommended |
|----------|---------|-------------|
| **RAM** | 256 MB | 512 MB |
| **Storage** | 100 MB | 1 GB+ (grows with memories) |
| **CPU** | 1 core | Any modern CPU |
| **Network** | Outbound HTTPS | For Discord & Claude API |

Runs great on a Raspberry Pi, cheap VPS, or your local machine.

---

## Data & Backups

Your memories live in `./data/memory.db` — a single SQLite file.

**Backup:**
```bash
cp data/memory.db backups/memory-$(date +%Y%m%d).db
```

**View logs:**
```bash
docker compose logs -f
```

**Stop the bot:**
```bash
docker compose down
```

---

## Development

For faster iteration during development, set `DEV_GUILD_ID` to your test server:

```env
DEV_GUILD_ID=123456789012345678
```

Commands sync instantly to that server instead of waiting up to 1 hour for global propagation.

**Run locally (without Docker):**
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python bot.py
```

---

## Documentation

- **[SETUP.md](SETUP.md)** — Detailed installation walkthrough with screenshots
- **[CONTRIBUTING.md](CONTRIBUTING.md)** — Guidelines for contributors

---

## Tech Stack

- **[Python 3.12](https://python.org)** — Runtime
- **[discord.py](https://discordpy.readthedocs.io/)** — Discord API wrapper
- **[Anthropic Claude](https://anthropic.com)** — AI for natural language Q&A
- **[SQLite + FTS5](https://sqlite.org/fts5.html)** — Fast full-text search
- **[Docker](https://docker.com)** — Containerized deployment

---

## License

MIT License — see [LICENSE](LICENSE) for details.

---

<p align="center">
  <b>Built for people who think faster than they can organize.</b>
</p>
