#!/bin/bash

# Ensure we're in the karrio directory
cd "$(dirname "$0")"

echo "Stopping Karrio services..."

# Stop all Karrio containers
docker compose -f docker/docker-compose.yml down

echo "Karrio services stopped" 