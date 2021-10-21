#!/usr/bin/env bash

# Source environment variables
source "${ROOT}/scripts/_env.sh"

# Create new python virtual environment
source "${ROOT}/scripts/create-new-env.sh"

# Install requirements
cd "${ROOT}"
if [[ "$*" != *--ee* ]];
then
    pip install -r "${ROOT:?}/requirements.server.dev.txt"
else
    pip install -r "${ROOT:?}/requirements.server.ee.dev.txt"
fi
cd -
