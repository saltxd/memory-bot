# Memory Bot

A Discord bot that acts as your personal knowledge base. Log anything, search it later, ask questions about it.

## Features

- **/log** - Save memories (notes, thoughts, tasks, anything)
- **/search** - Find memories by keyword using SQLite FTS5
- **/ask** - Ask questions and get AI-powered answers with citations
- **/help** - Quick reference
- **/stats** - See your memory count

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Discord Bot Token ([create one](https://discord.com/developers/applications))
- Anthropic API Key ([get one](https://console.anthropic.com/))

### 1. Clone and Configure

```bash
git clone https://github.com/YOUR_USERNAME/memory-bot.git
cd memory-bot
cp .env.example .env
```

Edit `.env` with your tokens:

```
DISCORD_TOKEN=your_discord_token_here
ANTHROPIC_API_KEY=your_anthropic_key_here
```

### 2. Start the Bot

```bash
docker compose up -d
```

### 3. Invite to Your Server

Generate an invite URL with these permissions:
- `applications.commands` (for slash commands)
- `bot` with permissions:
  - Send Messages
  - Use Slash Commands

Or use this template (replace `YOUR_CLIENT_ID`):
```
https://discord.com/api/oauth2/authorize?client_id=YOUR_CLIENT_ID&permissions=2147485696&scope=bot%20applications.commands
```

### 4. Use It

```
/log Met with Alex about the Q1 roadmap
/log Idea: add dark mode to the dashboard
/search roadmap
/ask What did I discuss with Alex?
```

## Development Mode

For instant command updates during development, set `DEV_GUILD_ID` to your test server's ID:

```env
DEV_GUILD_ID=123456789012345678
```

Commands sync instantly to that server. Without this, global commands take up to 1 hour to propagate.

To find your server ID:
1. Enable Developer Mode in Discord (Settings → App Settings → Advanced)
2. Right-click your server name → Copy Server ID

## Configuration

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `DISCORD_TOKEN` | Yes | - | Your Discord bot token |
| `ANTHROPIC_API_KEY` | Yes | - | Your Anthropic API key |
| `ANTHROPIC_MODEL` | No | `claude-3-5-haiku-latest` | Claude model to use |
| `CLAUDE_MAX_TOKENS` | No | `1024` | Max response length |
| `TIMEZONE` | No | `America/Denver` | Timezone for dates |
| `DEV_GUILD_ID` | No | - | Guild ID for dev (instant sync) |

## Data Storage

Memories are stored in `./data/memory.db` (SQLite). This directory is mounted as a volume, so your data persists across container restarts.

To backup:
```bash
cp data/memory.db memory-backup-$(date +%Y%m%d).db
```

## Logs

```bash
docker compose logs -f
```

## License

MIT

---

Built with [discord.py](https://discordpy.readthedocs.io/) and [Claude](https://www.anthropic.com/claude).
