#!/bin/bash

# Ensure we're in the karrio directory
cd "$(dirname "$0")"

echo "Starting Karrio services..."

# Ensure the docker/.env file exists and is properly configured
if [ ! -f "docker/.env" ]; then
  echo "The docker/.env file doesn't exist. Please create it first."
  exit 1
fi

# Clean up any existing services first
docker compose -f docker/docker-compose.yml down

# Start services with the correct configuration
docker compose -f docker/docker-compose.yml up -d

echo "Waiting for services to start..."
sleep 5

# Check if services are running
if docker ps | grep -q "karrio.api"; then
  echo "✅ Karrio API is running on http://localhost:5003"
  echo "✅ Karrio Dashboard is running on http://localhost:3002"
  echo "🔑 Default login: admin@example.com / demo"
  echo "💾 PostgreSQL is running on port 5434"
  echo "🔄 Redis is running on port 6379 (internally) and mapped to external port 6380"
else
  echo "❌ Error: Karrio services failed to start"
  echo "Check logs with: docker logs karrio.api"
fi

echo "Karrio started successfully!"
echo "API is running on http://localhost:5003"
echo "Dashboard is running on http://localhost:3002"
echo "Login with: admin@example.com / demo" 