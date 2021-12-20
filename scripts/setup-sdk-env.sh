#!/usr/bin/env bash

# Create new python virtual environment
source "scripts/create-new-env.sh"

# Install requirements
cd "${ROOT}" &&
pip install -r "${ROOT:?}/requirements.sdk.dev.txt"
