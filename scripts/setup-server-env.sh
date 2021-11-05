#!/usr/bin/env bash

# Create new python virtual environment
source "scripts/create-new-env.sh"

# Install requirements
cd "${ROOT}"
if [[ "$*" != *--insiders* ]];
then
    pip install -r "${ROOT:?}/requirements.server.dev.txt"
else
    pip install -r "${ROOT:?}/requirements.server.insiders.dev.txt"
fi
cd -


# Export environment variables
source "scripts/server.sh"

mkdir -p $LOG_DIR
