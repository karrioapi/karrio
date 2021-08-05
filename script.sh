#!/usr/bin/env bash

# Python virtual environment helpers

ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
BASE_DIR="${PWD##*/}"
ENV_DIR=".venv"
DIST="${ROOT:?}/.dist"

export wheels=~/Wheels
export PIP_FIND_LINKS="https://git.io/purplship"
[[ -d "$wheels" ]] && export PIP_FIND_LINKS=file://${wheels}

## icon vars
cross="\xE2\x9D\x8C"
check="\xE2\x9C\x94"

activate_env() {
  echo "Activate $BASE_DIR"
  deactivate >/dev/null 2>&1
  # shellcheck source=src/script.sh
  source "${ROOT:?}/$ENV_DIR/$BASE_DIR/bin/activate"
}

create_env() {
  echo "create $BASE_DIR Python3 env"
  deactivate >/dev/null 2>&1
  rm -rf "${ROOT:?}/$ENV_DIR" || true
  mkdir -p "${ROOT:?}/$ENV_DIR"
  python3 -m venv "${ROOT:?}/$ENV_DIR/$BASE_DIR" &&
  activate_env &&
  pip install --upgrade pip
}

init() {
    create_env &&
    pip install -r requirements.dev.txt
}


alias env:new=create_env
alias env:on=activate_env
alias env:reset=init


# Project helpers

submodules() {
    find "${ROOT:?}" -type f -name "setup.py" ! -path "*$ENV_DIR/*" -exec dirname '{}' \;
}

backup() {
    echo "Listing submodules..."
    [[ -d "$wheels" ]] &&
    find "${DIST}" -not -path "*$ENV_DIR/*" -name \*.whl -prune -exec cp '{}' "$wheels" \; &&
    clean
}

build() {
    clean
	rm -rf "${DIST}"
	mkdir -p "${DIST}"

    echo "building wheels..."
    packages=($(submodules))
	for pkg in ${packages}; do
		cd ${pkg};
		output=$(python setup.py bdist_wheel 2>&1);
		r=$?;
		cd - > /dev/null;
		if [[ ${r} -eq 1 ]]; then
			echo "> building "$(basename ${pkg})" ${cross} \n $output"; return ${r};
		else
			echo "> building "$(basename ${pkg})" ${check} ";
		fi;
    done

	find . -mindepth 2 ! -path "*$ENV_DIR/*" -name \*.whl -prune -exec mv '{}' "${DIST}" \;
    backup
}

clean() {
    echo "cleaning build files..."
    find . -type d -not -path "*$ENV_DIR/*" -name dist -prune -exec rm -r '{}' \; || true
    find . -type d -not -path "*$ENV_DIR/*" -name build -prune -exec rm -r '{}' \; || true
    find . -type d -not -path "*$ENV_DIR/*" -name "*.egg-info" -prune -exec rm -r '{}' \; || true
}

upload() {
    pip install twine > /dev/null &&
	twine upload "${DIST}/*"
}

env:on || true
