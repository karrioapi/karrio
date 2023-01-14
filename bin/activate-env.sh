#!/usr/bin/env bash

# Source environment variables
source "bin/_env.sh"

# activate Python virtual environment
echo "activating $BASE_DIR env ..."
source "${ROOT:?}/$ENV_DIR/$BASE_DIR/bin/activate"
