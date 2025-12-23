FROM python:3.12-slim

WORKDIR /app

# Install dependencies first for layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY bot.py db.py claude_client.py prompts.py ./

# Create data directory
RUN mkdir -p /data

# Set environment defaults
ENV PYTHONUNBUFFERED=1
ENV DB_PATH=/data/memory.db

CMD ["python", "bot.py"]
