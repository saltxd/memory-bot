"""
Anthropic Claude API client for memory-bot.
Simple, focused, no abstractions.
"""

import os
from anthropic import Anthropic

# Config with sensible defaults
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-3-5-haiku-latest")
MAX_TOKENS = int(os.getenv("CLAUDE_MAX_TOKENS", "1024"))


def get_client() -> Anthropic:
    """Get an Anthropic client instance."""
    if not ANTHROPIC_API_KEY:
        raise ValueError(
            "ANTHROPIC_API_KEY environment variable is required. "
            "Get your API key at https://console.anthropic.com/"
        )
    return Anthropic(api_key=ANTHROPIC_API_KEY)


def ask_with_context(
    question: str,
    memories: list[dict],
    system_prompt: str
) -> str:
    """
    Ask Claude a question with memory context.

    Args:
        question: The user's question
        memories: List of memory dicts with id, local_date, content
        system_prompt: System instructions for Claude

    Returns:
        Claude's response text
    """
    client = get_client()

    # Format memories as context
    if memories:
        context_lines = []
        for m in memories:
            context_lines.append(f"[#{m['id']} | {m['local_date']}] {m['content']}")
        context = "\n".join(context_lines)
        user_message = f"""Here are relevant memories from my personal log:

---
{context}
---

Based on these memories, please answer my question:
{question}"""
    else:
        user_message = f"""I don't have any relevant memories stored yet.

Question: {question}

Please let me know that I should log some information first using /log before I can ask questions about it."""

    response = client.messages.create(
        model=ANTHROPIC_MODEL,
        max_tokens=MAX_TOKENS,
        system=system_prompt,
        messages=[
            {"role": "user", "content": user_message}
        ]
    )

    return response.content[0].text


def check_api_key() -> bool:
    """Verify the API key is valid by making a minimal request."""
    try:
        client = get_client()
        # Minimal request to verify key works
        client.messages.create(
            model=ANTHROPIC_MODEL,
            max_tokens=10,
            messages=[{"role": "user", "content": "Hi"}]
        )
        return True
    except Exception:
        return False
