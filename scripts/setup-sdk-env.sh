#!/usr/bin/env bash

# Create new python virtual environment
source "scripts/create-new-env.sh"

# Install requirements
cd "${ROOT}/sdk" &&
poetry install || exit 1
cd -

cd "${ROOT}" &&
pip install -r requirements.sdk.dev.txt
cd -
