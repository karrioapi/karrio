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
    pip install -r "${ROOT:?}/requirements.dev.txt"
}


alias env:new=create_env
alias env:on=activate_env
alias env:reset=init


# Project helpers

# shellcheck disable=SC2120
test() {
  cd "${ROOT:?}"
  r=$(coverage run -m unittest discover -f -v "${ROOT:?}/tests"; echo $?)
  cd -
  return "$r"
}

typecheck() {
  cd "${ROOT:?}"
  for submodule in $(find "purplship" -type f -name "__init__.py" -exec dirname '{}' \;); do
    mypy "$submodule" || return $?
  done
  cd -
}

check() {
    typecheck && test
}

build() {
    python setup.py bdist_wheel
}

generate() {
    # shellcheck disable=SC1090
    . "${ROOT:?}/generate.sh"
}

env:on || true
