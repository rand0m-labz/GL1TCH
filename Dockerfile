# 🧠 GL1TCH Base Image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first (optional for later dependencies)
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt || true

# Copy project files
COPY . .

# Make entrypoint executable
RUN chmod +x ./scripts/entrypoint.sh

# Environment variables
ENV PYTHONUNBUFFERED=1

# Start the agent
ENTRYPOINT ["./scripts/entrypoint.sh"]


