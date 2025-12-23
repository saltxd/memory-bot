# Contributing to Memory Bot

Thanks for your interest in contributing! This document outlines how to get started.

## Code of Conduct

Be kind, be helpful, be respectful. We're all here to build something useful.

## Getting Started

### 1. Fork and Clone

```bash
git clone https://github.com/YOUR_USERNAME/memory-bot.git
cd memory-bot
```

### 2. Set Up Development Environment

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env
```

### 3. Configure for Development

Edit `.env` and add:
- Your Discord bot token
- Your Anthropic API key
- `DEV_GUILD_ID` set to your test server (for instant command sync)

### 4. Run Locally

```bash
# Create data directory
mkdir -p data
export DB_PATH=./data/memory.db

# Run the bot
python bot.py
```

## Project Structure

```
memory-bot/
├── bot.py           # Discord bot and slash commands
├── db.py            # SQLite database operations
├── claude_client.py # Anthropic API integration
├── prompts.py       # System prompts and help text
├── requirements.txt # Python dependencies
├── Dockerfile       # Container build
├── docker-compose.yml
└── data/            # SQLite database (gitignored)
```

## How to Contribute

### Reporting Bugs

1. Check if the issue already exists
2. Create a new issue with:
   - Clear title describing the problem
   - Steps to reproduce
   - Expected vs actual behavior
   - Your environment (OS, Python version, Docker version)

### Suggesting Features

1. Open an issue with the `enhancement` label
2. Describe:
   - What problem does this solve?
   - How would it work?
   - Are there alternatives?

### Submitting Code

1. **Create a branch** for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following the style guidelines below

3. **Test your changes** thoroughly:
   - Run the bot locally
   - Test affected commands
   - Check logs for errors

4. **Commit with clear messages**:
   ```bash
   git commit -m "Add: new /export command for memory backup"
   ```

5. **Push and create a Pull Request**:
   ```bash
   git push origin feature/your-feature-name
   ```

## Style Guidelines

### Python

- Follow PEP 8
- Use type hints where helpful
- Keep functions focused and small
- Add docstrings for public functions

### Code Philosophy

This project values:

- **Simplicity** — No unnecessary abstractions
- **Readability** — Clear over clever
- **Minimal dependencies** — Every dependency is a liability
- **Single-file modules** — Each file should do one thing well

### Commit Messages

Format: `Type: brief description`

Types:
- `Add:` New feature
- `Fix:` Bug fix
- `Update:` Enhancement to existing feature
- `Remove:` Removing code/feature
- `Refactor:` Code restructuring (no behavior change)
- `Docs:` Documentation only

Examples:
```
Add: /export command for memory backup
Fix: FTS5 search failing on special characters
Update: improve /ask response formatting
Docs: add troubleshooting section to SETUP.md
```

## Areas for Contribution

### Good First Issues

- Improve error messages
- Add more helpful tips to `/help`
- Write tests
- Improve documentation

### Medium Complexity

- Add `/delete` command to remove memories
- Add `/export` command to export memories as JSON
- Add memory categories/tags
- Improve search ranking

### Larger Projects

- Multi-user support (per-user memory isolation)
- Web interface for browsing memories
- Memory summarization (daily/weekly digests)
- Integration with other platforms

## Testing

Currently, the project doesn't have automated tests. This is a great area for contribution!

To manually test:
1. Run the bot with `DEV_GUILD_ID` set
2. Test each slash command
3. Check edge cases (empty inputs, special characters, long text)
4. Verify database integrity

## Questions?

- Open an issue for general questions
- Tag maintainers if you need help with your PR

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
