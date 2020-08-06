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
    pip install --upgrade pip wheel
}

submodules() {
    find "${ROOT:?}/extensions" -type f -name "setup.py" ! -path "*$ENV_DIR/*" -exec dirname {} \;
}

install_submodules() {
    pip install -e "${ROOT:?}[dev]" &&
    for module in $(submodules); do
      echo "installing ${module}..."
      pip install -e "${module}" || break
    done
}

init() {
    create_env &&
    pip install -r "${ROOT:?}/requirements.txt" &&
    install_submodules
}


alias env:new=create_env
alias env:on=activate_env
alias env:reset=init


# Project helpers

# shellcheck disable=SC2120
test() {
    if [[ "$1" == "-i" ]]; then
      install_submodules
    fi
    cd "${ROOT:?}"
    r=$(coverage run -m unittest discover -f -v "${ROOT:?}/tests")
    cd -
    $r || false
}

typecheck() {
    for module in $(submodules); do
      mypy "${module}/purplship" --no-strict-optional --no-warn-return-any --no-warn-unused-configs || break
    done
}

check() {
    typecheck && test
}

backup_wheels() {
    # shellcheck disable=SC2154
    [ -d "$wheels" ] &&
    find . -not -path "*$ENV_DIR/*" -name \*.whl -exec mv {} "$wheels" \; &&
    clean_builds
}

build() {
    clean_builds
    for module in $(submodules); do
      cd "${module}"
      python setup.py bdist_wheel
      popd
    done
    python "${ROOT:?}/setup.py" bdist_wheel
    backup_wheels
}

updaterelease() {
    git tag -f -a "$1"
    git push -f --tags
}

clean_builds() {
    find . -type d -not -path "*$ENV_DIR/*" -name dist -exec rm -r {} \; || true
    find . -type d -not -path "*$ENV_DIR/*" -name build -exec rm -r {} \; || true
    find . -type d -not -path "*$ENV_DIR/*" -name "*.egg-info" -exec rm -r {} \; || true
}

cli() {
  python "${ROOT:?}/cli.py" "$@"
}

env:on || true
