#!/bin/bash
set -e

echo "=== Setting up Sale AI in GitHub Codespaces ==="

# Ensure backend .env exists
if [ ! -f backend/.env ]; then
  cp backend/.env.example backend/.env
  echo "-> Created backend/.env from backend/.env.example"
fi

# Build and start Docker containers
echo "-> Deploying Docker containers via docker compose..."
docker compose --env-file backend/.env up -d --build

echo "=== Deployment Complete ==="
echo "Frontend is running on port 3000"
echo "Backend API is running on port 8000"
