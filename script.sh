#!/usr/bin/env bash

# Python virtual environment helpers

ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
BASE_DIR="${PWD##*/}"
ENV_DIR=".venv"
DIST="${ROOT:?}/.dist"

## icon vars
cross="\xE2\x9D\x8C"
check="\xE2\x9C\x94"

export wheels=~/Wheels
export PIP_FIND_LINKS="https://git.io/purplship"
[[ -d "$wheels" ]] && export PIP_FIND_LINKS="${PIP_FIND_LINKS} file://${wheels}"

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
  pip install --upgrade pip > /dev/null
}

init() {
  create_env &&
  pip install -r requirements.txt > /dev/null
}


alias env:new=create_env
alias env:on=activate_env
alias env:reset=init


# Project helpers

generate () {
  pushd "$1"
  . ./generate.sh "$2"
  popd
}

clean_builds() {
	echo "Clean up..."
    find . -type d -not -path "*$ENV_DIR/*" -name dist -prune -exec rm -r '{}' \; || true
    find . -type d -not -path "*$ENV_DIR/*" -name build -prune -exec rm -r '{}' \; || true
    find . -type d -not -path "*$ENV_DIR/*" -name "*.egg-info" -prune -exec rm -r '{}' \; || true
}

backup_wheels() {
  echo "Backup..."
  # shellcheck disable=SC2154
  [[ -d "$wheels" ]] &&
  find "${DIST}" -name \*.whl -exec cp '{}' "$wheels" \; &&
  clean_builds
}

build() {
  echo "Building..."
  clean_builds
  rm -rf "${DIST}"
  mkdir -p "${DIST}"

  for pkg in $(find "${ROOT:?}" -type f -name "pyproject.toml" ! -path "*$ENV_DIR/*" -exec dirname '{}' \;); do
    cd ${pkg};
	output=$(poetry build 2>&1);
	r=$?;
	cd - > /dev/null;
	if [[ ${r} -eq 1 ]]; then
		echo "> building "$(basename ${pkg})" ${cross} \n $output"; return ${r};
	else
		echo "> building "$(basename ${pkg})" ${check} ";
	fi;
  done

  find . -maxdepth 3 -mindepth 3 -not -path "*$ENV_DIR/*" -name \*.whl -prune -exec mv '{}' "${DIST}" \;
  backup_wheels
}

upload() {
	twine upload "${DIST}/*"
}

env:on || true
