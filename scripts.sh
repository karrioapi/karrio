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

init() {
    create_env &&
    pip install -r "${ROOT:?}/requirements.txt" &&
    pip install -r "${ROOT:?}/requirements.dev.txt" &&
    install_all
}


alias env:new=create_env
alias env:on=activate_env
alias env:reset=init


# Project helpers

install_all() {
    pip install -e "${ROOT:?}/purpleserver/core" &&
    pip install -e "${ROOT:?}/purpleserver/proxy" &&
    pip install -e "${ROOT:?}/purpleserver"
}

run_server() {
  if [[ "$1" == "-i" ]]; then
    install_all
  fi
  purplship makemigrations &&
  purplship migrate &&
  (echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'demo')" | purplship shell) > /dev/null 2>&1;
  purplship runserver
}

clean_builds() {
    find . -type d -not -path "*$ENV_DIR/*" -name dist -exec rm -r {} \; || true
    find . -type d -not -path "*$ENV_DIR/*" -name build -exec rm -r {} \; || true
    find . -type d -not -path "*$ENV_DIR/*" -name "*.egg-info" -exec rm -r {} \; || true
}

backup_wheels() {
    # shellcheck disable=SC2154
    [ -d "$wheels" ] &&
    find . -not -path "*$ENV_DIR/*" -name \*.whl -exec mv {} "$wheels" \; &&
    clean_builds
}

build() {
  pushd "$1" || false &&
  python setup.py bdist_wheel
  popd || true
}

build_all() {
  clean_builds
  build "${ROOT:?}/purpleserver/core"
  build "${ROOT:?}/purpleserver/proxy"
  build "${ROOT:?}/purpleserver"
  backup_wheels
}


alias run=run_server

env:on || true
