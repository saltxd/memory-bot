# Setup Guide

This guide walks you through setting up Memory Bot from scratch. Follow each step carefully.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Create a Discord Bot](#create-a-discord-bot)
3. [Get an Anthropic API Key](#get-an-anthropic-api-key)
4. [Configure the Bot](#configure-the-bot)
5. [Start the Bot](#start-the-bot)
6. [Invite the Bot to Your Server](#invite-the-bot-to-your-server)
7. [Verify It's Working](#verify-its-working)
8. [Troubleshooting](#troubleshooting)

---

## Prerequisites

Before starting, ensure you have:

- **Docker Desktop** installed and running
  - [Download for Mac](https://docs.docker.com/desktop/install/mac-install/)
  - [Download for Windows](https://docs.docker.com/desktop/install/windows-install/)
  - [Download for Linux](https://docs.docker.com/desktop/install/linux-install/)

- **A Discord account** — [Sign up free](https://discord.com/)

- **A Discord server** where you have admin permissions (or create a new one)

---

## Create a Discord Bot

### Step 1: Open the Discord Developer Portal

Go to: **https://discord.com/developers/applications**

Sign in with your Discord account if prompted.

### Step 2: Create a New Application

1. Click the **"New Application"** button (top right)
2. Enter a name: `Memory Bot` (or whatever you prefer)
3. Accept the Terms of Service
4. Click **"Create"**

### Step 3: Get Your Application ID

On the **General Information** page:
- Find **"Application ID"**
- Click **"Copy"** — you'll need this later for the invite URL

### Step 4: Create a Bot User

1. Click **"Bot"** in the left sidebar
2. Click **"Add Bot"** → **"Yes, do it!"**
3. Your bot is created!

### Step 5: Get Your Bot Token

On the Bot page:
1. Click **"Reset Token"** → **"Yes, do it!"**
2. Click **"Copy"** to copy the token
3. **Save this token securely** — you won't be able to see it again!

> **Warning:** Never share your bot token publicly. Anyone with the token can control your bot.

### Step 6: Enable Message Content Intent

Still on the Bot page:
1. Scroll down to **"Privileged Gateway Intents"**
2. Enable **"Message Content Intent"** (toggle it ON)
3. Click **"Save Changes"** if prompted

This allows the bot to read message content for future features.

### Step 7: Configure OAuth2 Permissions

1. Click **"OAuth2"** in the left sidebar
2. Then click **"URL Generator"**
3. Under **"Scopes"**, check:
   - `bot`
   - `applications.commands`
4. Under **"Bot Permissions"**, check:
   - `Send Messages`
   - `Use Slash Commands`
5. Copy the generated URL at the bottom — you'll use this to invite the bot

---

## Get an Anthropic API Key

Memory Bot uses Claude (by Anthropic) for AI-powered question answering.

### Step 1: Create an Anthropic Account

Go to: **https://console.anthropic.com/**

Sign up for an account if you don't have one.

### Step 2: Add Credits

1. Go to **Settings** → **Billing**
2. Add a payment method
3. Add credits ($5 minimum, lasts a long time with Haiku model)

> **Cost estimate:** The default Haiku model costs ~$0.25 per million input tokens. A typical `/ask` query costs less than $0.001.

### Step 3: Generate an API Key

1. Go to **Settings** → **API Keys**
2. Click **"Create Key"**
3. Name it something like `memory-bot`
4. Click **"Create"**
5. **Copy the key** — it starts with `sk-ant-`
6. Save it securely — you won't see it again!

---

## Configure the Bot

### Step 1: Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/memory-bot.git
cd memory-bot
```

### Step 2: Create Your Environment File

```bash
cp .env.example .env
```

### Step 3: Edit the Environment File

Open `.env` in your favorite editor:

```bash
nano .env
# or
code .env
# or
vim .env
```

Fill in the required values:

```env
# REQUIRED: Your Discord bot token (from Step 5 above)
DISCORD_TOKEN=your_discord_bot_token_here

# REQUIRED: Your Anthropic API key (from Step 3 above)
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

Optional settings you might want to change:

```env
# Change the AI model (default is fast and cheap)
ANTHROPIC_MODEL=claude-3-5-haiku-latest

# Change your timezone for date display
TIMEZONE=America/New_York

# For development: instant command sync to a specific server
DEV_GUILD_ID=123456789012345678
```

Save and close the file.

---

## Start the Bot

### Using Docker (Recommended)

```bash
docker compose up -d
```

The `-d` flag runs it in the background (detached mode).

**Check if it's running:**

```bash
docker compose logs -f
```

You should see output like:

```
memory-bot-1  | Memory Bot starting...
memory-bot-1  | ----------------------------------------
memory-bot-1  | Logged in as Memory Bot#1234 (ID: 123456789)
memory-bot-1  | Connected to 0 guild(s)
memory-bot-1  | Database ready: 0 memories stored
memory-bot-1  | PRODUCTION MODE: Commands synced globally
memory-bot-1  | ----------------------------------------
memory-bot-1  | Memory Bot is ready!
```

Press `Ctrl+C` to stop watching logs (bot keeps running).

### Without Docker

If you prefer running without Docker:

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create data directory
mkdir -p data
export DB_PATH=./data/memory.db

# Run the bot
python bot.py
```

---

## Invite the Bot to Your Server

### Step 1: Get Your Invite URL

Use the URL you generated earlier, or create one with this template:

```
https://discord.com/api/oauth2/authorize?client_id=YOUR_APPLICATION_ID&permissions=2147485696&scope=bot%20applications.commands
```

Replace `YOUR_APPLICATION_ID` with your Application ID from Step 3 of creating the Discord bot.

### Step 2: Invite the Bot

1. Open the invite URL in your browser
2. Select the server you want to add the bot to
3. Click **"Authorize"**
4. Complete the CAPTCHA if prompted

### Step 3: Verify the Bot Joined

Check your server — you should see the bot in the member list (it may appear offline for a moment).

---

## Verify It's Working

In any channel where the bot can see messages:

1. Type `/` — you should see Memory Bot's commands appear
2. Try `/help` — should show the help message
3. Try `/log Test memory` — should confirm it was saved
4. Try `/search Test` — should find your memory
5. Try `/ask What did I log?` — should get an AI response

If slash commands don't appear:
- Wait a few minutes (global commands can take up to 1 hour to propagate)
- Try refreshing Discord (Ctrl+R or Cmd+R)
- Check the bot logs for errors

---

## Troubleshooting

### Bot won't start

**Check Docker is running:**
```bash
docker info
```
If this fails, start Docker Desktop.

**Check for errors:**
```bash
docker compose logs
```

**Common errors:**

| Error | Solution |
|-------|----------|
| `DISCORD_TOKEN is required` | Add your Discord token to `.env` |
| `ANTHROPIC_API_KEY is required` | Add your Anthropic key to `.env` |
| `Improper token has been passed` | Your Discord token is invalid — regenerate it |
| `401 Unauthorized` | Anthropic API key is invalid — create a new one |

### Commands don't appear

- **Wait up to 1 hour** — Global command sync takes time
- **Use DEV_GUILD_ID** — For instant sync to your test server:
  1. Enable Developer Mode in Discord (Settings → Advanced)
  2. Right-click your server → Copy Server ID
  3. Add `DEV_GUILD_ID=your_server_id` to `.env`
  4. Restart the bot: `docker compose restart`

### Bot is offline in Discord

- Check if the container is running: `docker compose ps`
- Check logs for errors: `docker compose logs -f`
- Verify your Discord token is correct

### "/ask" returns errors

- Check your Anthropic API key is valid
- Verify you have credits in your Anthropic account
- Check logs for specific error messages

### Port conflicts (if running multiple bots)

This bot doesn't expose any ports — it only makes outbound connections. No port conflicts should occur.

### Data persistence issues

Memories are stored in `./data/memory.db`. Ensure:
- The `data` directory exists
- Docker has permission to write to it
- The volume is mounted correctly in `docker-compose.yml`

---

## Getting Help

If you're still stuck:

1. Check the [GitHub Issues](https://github.com/YOUR_USERNAME/memory-bot/issues)
2. Open a new issue with:
   - What you tried
   - The error message
   - Your OS and Docker version

---

## Next Steps

- **Add memories** — Start logging your thoughts with `/log`
- **Explore search** — Find patterns with `/search`
- **Ask questions** — Use `/ask` for AI-powered recall
- **Customize** — Edit `prompts.py` to change AI behavior
- **Contribute** — See [CONTRIBUTING.md](CONTRIBUTING.md)
