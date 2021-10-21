#!/usr/bin/env bash

# Python virtual environment helpers
ROOT="$( cd "$( dirname $0 )/../" >/dev/null 2>&1 && pwd )"
BASE_DIR="${ROOT##*/}"
ENV_DIR=".venv"
DIST="${ROOT:?}/${ENV_DIR}/.dist"
EE_DIST="${ROOT:?}/${ENV_DIR}/.ee-dist"

mkdir -p "${DIST}" "${EE_DIST}"

## icon vars
cross="\xE2\x9D\x8C"
check="\xE2\x9C\x94"


clean_build_files() {
    find $1 -type d -name dist -prune -exec rm -r '{}' \; || true
    find $1 -type d -name build -prune -exec rm -r '{}' \; || true
    find $1 -type d -name "*.egg-info" -prune -exec rm -r '{}' \; || true
}

backup_wheels() {
    if [[ "$*" != *--ee* ]];
    then
        find "${1}/dist" -name \*.whl -prune -exec mv '{}' "${DIST}" \;
    else
        find "${1}/dist" -name \*.whl -prune -exec mv '{}' "${EE_DIST}" \;
    fi
}
