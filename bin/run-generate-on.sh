#!/usr/bin/env bash

# Source environment variables
source "bin/_env.sh"

# Activate python virtual environment
source "${ROOT}/bin/activate-env.sh" || exit 1

cd "$1" && ./generate.sh && cd -
