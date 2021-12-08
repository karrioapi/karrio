#!/usr/bin/env bash

# Source environment variables
source "scripts/_env.sh"

echo 'building insiders cloud image...'
docker build -f "${ROOT}/docker/Dockerfile" \
    -t registry.gitlab.com/purplship/cloud:$1 \
    --build-arg REQUIREMENTS="requirements.insiders.txt" \
    --build-arg REGISTRY_TOKEN="${REGISTRY_TOKEN}" \
    --build-arg REGISTRY_TOKEN_NAME="${REGISTRY_TOKEN_NAME}" \
    "${ROOT}" "${@:2}"
