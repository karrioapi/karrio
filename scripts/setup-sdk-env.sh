#!/usr/bin/env bash

# Create new python virtual environment
source "scripts/create-new-env.sh"

# Install requirements
cd "${ROOT}" &&
if [[ "$*" != *--insiders* ]];
then
    pip install -r "${ROOT:?}/requirements.sdk.dev.txt"
else
    pip install -r "${ROOT:?}/requirements.sdk.insiders.dev.txt"
fi
cd -
