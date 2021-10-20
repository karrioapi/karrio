#!/usr/bin/env bash

# Python virtual environment helpers
ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
BASE_DIR="${ROOT##*/}"
ENV_DIR=".venv"

# prepare virtual environment directory
echo 'prepare env directory ...'
deactivate >/dev/null 2>&1
rm -rf "${ROOT:?}/$ENV_DIR"
mkdir -p "${ROOT:?}/$ENV_DIR"

# create virtual environment
echo "creating $BASE_DIR env ..."
python3 -m venv "${ROOT:?}/$ENV_DIR/$BASE_DIR"

echo "activating $BASE_DIR env ..."
source "${ROOT:?}/$ENV_DIR/$BASE_DIR/bin/activate"

# install requirements
echo "installing requirements ..."
pip install --upgrade pip poetry wheel > /dev/null
