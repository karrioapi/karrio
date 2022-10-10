#!/usr/bin/env bash

# Create new python virtual environment
source "scripts/create-new-env.sh"

# Install requirements
cd "${ROOT}"
    pip install -r "${ROOT:?}/requirements.server.dev.txt"
cd -

if [[ "$*" == *--cloud* ]];
then
    pip install -r "${CLOUD_REQUIREMENTS:?}"
fi


# Export environment variables
source "scripts/server.sh"

mkdir -p $LOG_DIR
