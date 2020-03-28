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
    pip install -r requirements.txt &&
    pip install -r requirements.dev.txt &&
    pip install -e .
}


alias env:new=create_env
alias env:on=activate_env
alias env:reset=init


# Project helpers

# shellcheck disable=SC2120
test() {
    pip install -e .
    pushd tests || exit
    python -m unittest -v "$@"
    popd || exit
}

typecheck() {
    mypy purplship/ --no-strict-optional --no-warn-return-any --no-warn-unused-configs
}

check() {
    typecheck && test 
}

backup_wheels() {
    [ -d "$WHEEL_STORE" ] &&
    find . -name \*.whl -exec mv {} "$WHEEL_STORE" \; &&
    clean_builds
}

build_package() {
    clean_builds
    python setup.package.py bdist_wheel
    backup_wheels
}

build_freight() {
    clean_builds
    python setup.freight.py bdist_wheel
    backup_wheels
}

build_core() {
    clean_builds
    python setup.core.py bdist_wheel
    backup_wheels
}

build() {
    clean_builds
    python setup.py bdist_wheel
    backup_wheels
}

updaterelease() {
    git tag -f -a "$1"
    git push -f --tags
}

clean_builds() {
    find . -type d -name dist -exec rm -r {} \; || true
    find . -type d -name build -exec rm -r {} \; || true
    find . -type d -name "*.egg-info" -exec rm -r {} \; || true
}
