#!/bin/bash
set -e

echo "=== Setting up Sale AI in GitHub Codespaces ==="

# Ensure backend .env exists
if [ ! -f backend/.env ]; then
  cp backend/.env.example backend/.env
  echo "-> Created backend/.env from backend/.env.example"
fi

# Inject GEMINI_API_KEY if present in codespace environment
if [ -n "$GEMINI_API_KEY" ]; then
  sed -i "s|^GEMINI_API_KEY=.*|GEMINI_API_KEY=${GEMINI_API_KEY}|" backend/.env
  echo "-> Configured GEMINI_API_KEY from environment"
fi

# Build and start Docker containers
echo "-> Deploying Docker containers via docker compose..."
docker compose --env-file backend/.env up -d --build

echo "=== Deployment Complete ==="
echo "Frontend is running on port 3000"
echo "Backend API is running on port 8000"
