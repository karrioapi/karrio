#!/usr/bin/env bash

# Python virtual environment helpers

ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
BASE_DIR="${PWD##*/}"
ENV_DIR=".venv"

activate_env() {
  echo "Activate $BASE_DIR"
  deactivate || true
  # shellcheck source=src/script.sh
  source "${ROOT:?}/$ENV_DIR/$BASE_DIR/bin/activate"
}

create_env() {
  echo "create $BASE_DIR Python3 env"
  deactivate || true
  rm -rf "${ROOT:?}/$ENV_DIR" || true
  mkdir -p "${ROOT:?}/$ENV_DIR"
  python3 -m venv "${ROOT:?}/$ENV_DIR/$BASE_DIR" &&
  activate_env &&
  pip install --upgrade pip
}


alias env:new=create_env
alias env:on=activate_env


# Project helpers

build() {
  pushd "$1"
    clean_builds
    python setup.py bdist_wheel
    backup_wheels
  popd
}

clean_builds() {
  find . -type d -not -path "*$ENV_DIR/*" -name dist -exec rm -r {} \; || true
  find . -type d -not -path "*$ENV_DIR/*" -name build -exec rm -r {} \; || true
  find . -type d -not -path "*$ENV_DIR/*" -name "*.egg-info" -exec rm -r {} \; || true
}

env:on || true
