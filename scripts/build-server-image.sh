#!/usr/bin/env bash

# Source environment variables
source "scripts/_env.sh"

echo 'building server image...'
docker build -f "${ROOT}/docker/Dockerfile" -t purplship/server:$1 "${ROOT}" "${@:2}"
