"""
Memory Bot - Discord personal knowledge base.
Simple, focused, shippable.
"""

import os
import sys
import asyncio
import discord
from discord import app_commands
from discord.ext import commands

import db
import claude_client
from prompts import ASK_SYSTEM_PROMPT, HELP_TEXT, ONBOARDING_DM

# ─────────────────────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────────────────────

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DEV_GUILD_ID = os.getenv("DEV_GUILD_ID")

# Validate required env vars early
def check_config():
    """Validate required configuration on startup."""
    errors = []

    if not DISCORD_TOKEN:
        errors.append("DISCORD_TOKEN is required. Get it from https://discord.com/developers/applications")

    if not os.getenv("ANTHROPIC_API_KEY"):
        errors.append("ANTHROPIC_API_KEY is required. Get it from https://console.anthropic.com/")

    if errors:
        print("Configuration errors:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        sys.exit(1)


# ─────────────────────────────────────────────────────────────
# Bot Setup
# ─────────────────────────────────────────────────────────────

intents = discord.Intents.default()
intents.message_content = True  # For future prefix commands if needed


class MemoryBot(commands.Bot):
    """Custom bot class with setup hook for command sync."""

    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)
        self.synced = False

    async def setup_hook(self):
        """Sync slash commands on startup."""
        if self.synced:
            return

        try:
            if DEV_GUILD_ID:
                # Fast sync to dev guild for testing
                guild = discord.Object(id=int(DEV_GUILD_ID))
                self.tree.copy_global_to(guild=guild)
                synced = await self.tree.sync(guild=guild)
                print(f"Synced {len(synced)} commands to dev guild {DEV_GUILD_ID}")
            else:
                # Global sync (can take up to 1 hour to propagate)
                synced = await self.tree.sync()
                print(f"Synced {len(synced)} commands globally (may take up to 1 hour to appear)")

            self.synced = True
        except Exception as e:
            print(f"Failed to sync commands: {e}", file=sys.stderr)


bot = MemoryBot()


# ─────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────

def truncate(text: str, max_len: int = 2000) -> str:
    """Truncate text to fit Discord's message limit."""
    if len(text) <= max_len:
        return text
    return text[:max_len - 3] + "..."


async def send_onboarding_dm(member: discord.Member):
    """Send onboarding DM to new members."""
    try:
        await member.send(ONBOARDING_DM)
        print(f"Sent onboarding DM to {member}")
    except discord.Forbidden:
        # User has DMs disabled
        pass
    except Exception as e:
        print(f"Failed to send onboarding DM: {e}")


# ─────────────────────────────────────────────────────────────
# Events
# ─────────────────────────────────────────────────────────────

@bot.event
async def on_ready():
    """Called when bot is connected and ready."""
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print(f"Connected to {len(bot.guilds)} guild(s)")

    # Initialize database
    db.init_db()
    memory_count = db.get_memory_count()
    print(f"Database ready: {memory_count} memories stored")

    if DEV_GUILD_ID:
        print(f"DEV MODE: Commands synced to guild {DEV_GUILD_ID}")
    else:
        print("PRODUCTION MODE: Commands synced globally")

    print("-" * 40)
    print("Memory Bot is ready!")


@bot.event
async def on_member_join(member: discord.Member):
    """Send onboarding DM when a new member joins."""
    await send_onboarding_dm(member)


# ─────────────────────────────────────────────────────────────
# Slash Commands
# ─────────────────────────────────────────────────────────────

@bot.tree.command(name="log", description="Save a memory to your personal knowledge base")
@app_commands.describe(text="What do you want to remember?")
async def log_cmd(interaction: discord.Interaction, text: str):
    """Store a new memory entry."""
    await interaction.response.defer(thinking=True)

    try:
        memory_id = db.add_memory(
            user_id=str(interaction.user.id),
            content=text,
            channel_id=str(interaction.channel_id) if interaction.channel_id else None
        )

        count = db.get_memory_count()
        await interaction.followup.send(
            f"Logged! (#{memory_id})\n"
            f"You now have **{count}** memories stored."
        )
        print(f"[log] User {interaction.user} stored memory #{memory_id}")

    except Exception as e:
        await interaction.followup.send(f"Failed to save memory: {e}")
        print(f"[log] Error: {e}", file=sys.stderr)


@bot.tree.command(name="search", description="Search your memories by keyword")
@app_commands.describe(query="What are you looking for?")
async def search_cmd(interaction: discord.Interaction, query: str):
    """Search memories using FTS5."""
    await interaction.response.defer(thinking=True)

    try:
        results = db.search_memories(query, limit=5)

        if not results:
            await interaction.followup.send(
                f"No memories found matching **{query}**.\n"
                "Try different keywords or use `/log` to store some memories first."
            )
            return

        lines = [f"**Found {len(results)} memories matching \"{query}\":**\n"]

        for r in results:
            # Truncate snippet for display
            snippet = r["snippet"][:150] + "..." if len(r["snippet"]) > 150 else r["snippet"]
            lines.append(f"**#{r['id']}** ({r['local_date']})\n> {snippet}\n")

        response = "\n".join(lines)
        await interaction.followup.send(truncate(response))
        print(f"[search] User {interaction.user} searched '{query}', found {len(results)} results")

    except Exception as e:
        await interaction.followup.send(f"Search failed: {e}")
        print(f"[search] Error: {e}", file=sys.stderr)


@bot.tree.command(name="ask", description="Ask a question about your memories")
@app_commands.describe(question="What would you like to know?")
async def ask_cmd(interaction: discord.Interaction, question: str):
    """Answer questions using Claude with memory context."""
    await interaction.response.defer(thinking=True)

    try:
        # Get relevant memories via search
        memories = db.search_memories(question, limit=10)

        # If no search results, try recent memories
        if not memories:
            memories = db.get_recent_memories(limit=10)

        # Ask Claude
        response = claude_client.ask_with_context(
            question=question,
            memories=memories,
            system_prompt=ASK_SYSTEM_PROMPT
        )

        await interaction.followup.send(truncate(response))
        print(f"[ask] User {interaction.user} asked: '{question[:50]}...'")

    except ValueError as e:
        # API key error
        await interaction.followup.send(f"Configuration error: {e}")
        print(f"[ask] Config error: {e}", file=sys.stderr)

    except Exception as e:
        await interaction.followup.send(f"Failed to answer: {e}")
        print(f"[ask] Error: {e}", file=sys.stderr)


@bot.tree.command(name="help", description="Learn how to use Memory Bot")
async def help_cmd(interaction: discord.Interaction):
    """Show help text."""
    await interaction.response.send_message(HELP_TEXT, ephemeral=True)
    print(f"[help] User {interaction.user} requested help")


@bot.tree.command(name="stats", description="Show your memory statistics")
async def stats_cmd(interaction: discord.Interaction):
    """Show memory count and basic stats."""
    await interaction.response.defer(thinking=True)

    try:
        count = db.get_memory_count()
        recent = db.get_recent_memories(limit=1)

        if recent:
            last_memory = recent[0]
            last_date = last_memory["local_date"]
            response = (
                f"**Your Memory Stats**\n\n"
                f"Total memories: **{count}**\n"
                f"Last entry: {last_date}\n\n"
                f"Use `/log` to add more memories!"
            )
        else:
            response = (
                f"**Your Memory Stats**\n\n"
                f"Total memories: **{count}**\n\n"
                f"Get started with `/log` to save your first memory!"
            )

        await interaction.followup.send(response)

    except Exception as e:
        await interaction.followup.send(f"Failed to get stats: {e}")


# ─────────────────────────────────────────────────────────────
# Error Handling
# ─────────────────────────────────────────────────────────────

@bot.tree.error
async def on_app_command_error(
    interaction: discord.Interaction,
    error: app_commands.AppCommandError
):
    """Global error handler for slash commands."""
    if isinstance(error, app_commands.CommandOnCooldown):
        await interaction.response.send_message(
            f"Please wait {error.retry_after:.1f}s before using this command again.",
            ephemeral=True
        )
    elif isinstance(error, app_commands.MissingPermissions):
        await interaction.response.send_message(
            "You don't have permission to use this command.",
            ephemeral=True
        )
    else:
        print(f"Command error: {error}", file=sys.stderr)
        if not interaction.response.is_done():
            await interaction.response.send_message(
                f"An error occurred: {error}",
                ephemeral=True
            )


# ─────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────

def main():
    """Entry point."""
    print("Memory Bot starting...")
    print("-" * 40)

    # Check config before starting
    check_config()

    # Ensure data directory exists
    db_path = os.getenv("DB_PATH", "/data/memory.db")
    db_dir = os.path.dirname(db_path)
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir, exist_ok=True)
        print(f"Created data directory: {db_dir}")

    # Run the bot
    bot.run(DISCORD_TOKEN)


if __name__ == "__main__":
    main()
