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
    pip install -r requirements.txt
}


alias env:new=create_env
alias env:on=activate_env
alias env:reset=init


# Project helpers

build_all() {
    mkdir -p ./dist
    for d in py-*/ ; do
        pushd "${d}" &&
        python setup.py bdist_wheel &&
        popd
    done
    find . -name \*.whl -exec mv {} ./dist \;
}

clean_builds() {
    find . -type d -name dist -exec rm -r {} \;
    find . -type d -name build -exec rm -r {} \;
    find . -type d -name "*.egg-info" -exec rm -r {} \;
}

generate () {
    pushd "$1"
    . ./generate.sh "$2"
    popd
}
