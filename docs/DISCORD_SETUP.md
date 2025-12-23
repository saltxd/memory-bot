# Discord Bot Setup Guide

Complete guide to creating and configuring a Discord bot for Memory Bot.

## Step 1: Create a Discord Application

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click **"New Application"**
3. Name it "Memory Bot" (or whatever you prefer)
4. Click **"Create"**

## Step 2: Create the Bot

1. In your application, go to **"Bot"** in the left sidebar
2. Click **"Add Bot"**
3. Confirm by clicking **"Yes, do it!"**

### Configure Bot Settings

Under the Bot section:

- **Username**: Set your bot's display name
- **Icon**: Upload a profile picture (optional)
- **Public Bot**: Disable if you want only you to add it to servers
- **Privileged Gateway Intents**: Leave all disabled (not needed)

### Get Your Token

1. Click **"Reset Token"** (or "View Token" if first time)
2. Copy the token immediately - you can only see it once
3. Save it somewhere secure (you'll need it for `.env`)

**Never share your token or commit it to git!**

## Step 3: Configure OAuth2

1. Go to **"OAuth2"** → **"URL Generator"** in the left sidebar

2. Under **Scopes**, select:
   - `bot`
   - `applications.commands`

3. Under **Bot Permissions**, select:
   - `Send Messages`
   - `Use Slash Commands`

4. Copy the generated URL at the bottom

## Step 4: Invite the Bot

1. Open the generated URL in your browser
2. Select the server you want to add the bot to
3. Click **"Authorize"**
4. Complete the CAPTCHA

## Step 5: Get Your Guild ID (for Development)

For instant command updates during development:

1. Open Discord
2. Go to **User Settings** → **App Settings** → **Advanced**
3. Enable **Developer Mode**
4. Right-click on your server name in the server list
5. Click **"Copy Server ID"**

Add this to your `.env`:
```
DEV_GUILD_ID=123456789012345678
```

## Step 6: Configure and Run

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` with your values:
   ```
   DISCORD_TOKEN=your_bot_token_here
   ANTHROPIC_API_KEY=your_anthropic_key_here
   DEV_GUILD_ID=your_server_id_here
   ```

3. Start the bot:
   ```bash
   docker compose up -d
   ```

4. Check logs:
   ```bash
   docker compose logs -f
   ```

You should see:
```
Memory Bot starting...
----------------------------------------
Logged in as Memory Bot#1234 (ID: 123456789)
Connected to 1 guild(s)
Database ready: 0 memories stored
DEV MODE: Commands synced to guild 123456789
----------------------------------------
Memory Bot is ready!
```

## Step 7: Verify It Works

1. Go to your Discord server
2. Type `/` in any channel
3. You should see Memory Bot's commands:
   - `/log`
   - `/search`
   - `/ask`
   - `/help`
   - `/stats`

4. Try it:
   ```
   /log Testing my new memory bot!
   /search testing
   /ask What did I just log?
   ```

## Troubleshooting

### Commands not appearing

**If using DEV_GUILD_ID:**
- Make sure the ID is correct (right-click server → Copy Server ID)
- Restart the bot: `docker compose restart`
- Check logs for sync errors

**If NOT using DEV_GUILD_ID (global commands):**
- Global commands can take up to 1 hour to appear
- This is a Discord limitation, not a bug
- For development, always use DEV_GUILD_ID

### Bot offline

1. Check if container is running:
   ```bash
   docker compose ps
   ```

2. Check logs for errors:
   ```bash
   docker compose logs memory-bot
   ```

3. Common errors:
   - `DISCORD_TOKEN is required` → Token not set in `.env`
   - `Invalid token` → Token is wrong or expired (regenerate in Developer Portal)
   - `ANTHROPIC_API_KEY is required` → API key not set

### Permission errors

Make sure the bot has these permissions in your server:
- Send Messages
- Use Slash Commands

You can check in **Server Settings** → **Integrations** → **Memory Bot**

## Production Deployment

For production (not development):

1. Remove `DEV_GUILD_ID` from `.env` (or leave it empty)
2. Commands will sync globally (all servers where bot is invited)
3. First sync takes up to 1 hour
4. Subsequent updates also take up to 1 hour

This is a Discord rate limit for global commands. For a personal bot, using DEV_GUILD_ID is fine even in "production" since you control the servers.

## Security Notes

- Never share your bot token
- Never commit `.env` to git
- Regenerate token if compromised (in Developer Portal → Bot → Reset Token)
- Consider making your bot private (Developer Portal → Bot → disable "Public Bot")
