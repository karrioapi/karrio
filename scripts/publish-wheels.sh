#!/usr/bin/env bash

# Source environment variables
source "scripts/_env.sh"

# Activate python virtual environment
source "${ROOT}/scripts/activate-env.sh" || exit 1

echo 'uploading wheels...'
pip install twine &&
twine upload "${DIST}/*"
