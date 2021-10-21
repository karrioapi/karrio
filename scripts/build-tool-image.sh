#!/usr/bin/env bash

# Source environment variables
source "scripts/_env.sh"

echo "building dev tool image..."
docker build -f "${ROOT}/docker/dev.tool.Dockerfile" -t purplship/tools "${ROOT}"
