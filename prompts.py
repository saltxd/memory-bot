"""
System prompts for memory-bot.
Keep them focused and useful.
"""

ASK_SYSTEM_PROMPT = """You are a helpful personal memory assistant. The user has logged various thoughts, notes, and information over time, and you help them recall and synthesize this information.

Your role:
1. Answer questions based on the provided memory context
2. Cite specific memory IDs when referencing information (use format: [#ID])
3. Be concise but thorough
4. If memories don't contain enough info to answer, say so clearly
5. Suggest what additional information might help if relevant

Response format:
- Start with a direct answer to the question
- Include relevant details from memories with citations
- Use bullet points for clarity when listing multiple items
- Keep responses under 1500 characters (Discord limit)

Example citation: "You mentioned working on the API refactor [#42] and completing it on Friday [#47]."
"""

HELP_TEXT = """**Memory Bot - Your Personal Knowledge Base**

Store anything, search it later, ask questions about it.

**Commands:**

`/log <text>`
Save a memory. Log thoughts, notes, tasks, anything.
> Example: `/log Met with Sarah about Q1 planning. Action: send budget by Friday`

`/search <query>`
Find memories by keyword. Shows top 5 matches with IDs.
> Example: `/search budget meeting`

`/ask <question>`
Ask a question and get an AI-powered answer based on your memories.
> Example: `/ask What did Sarah and I discuss about Q1?`

`/help`
Show this message.

**Tips:**
- Log frequently - short notes are fine
- Include dates, names, and context for better recall
- Use /search to find specific entries
- Use /ask for synthesis and summaries

**Privacy:** Your memories are stored locally and only you can access them.
"""

ONBOARDING_DM = """Hey! I'm **Memory Bot** - your personal knowledge base.

I help you remember things by storing notes and letting you search or ask questions about them later.

**Quick start:**
1. Go to any channel where I'm active
2. Type `/log Had coffee with Alex, discussed the new project timeline`
3. Later, use `/search Alex` or `/ask What did Alex and I talk about?`

**Commands:**
- `/log <text>` - Save a memory
- `/search <query>` - Find by keyword
- `/ask <question>` - AI-powered Q&A over your memories
- `/help` - Full help

That's it! Start logging and I'll help you remember everything.
"""
