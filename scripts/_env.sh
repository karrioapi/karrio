#!/usr/bin/env bash

# Python virtual environment helpers
ROOT="$( pwd )"
BASE_DIR="${ROOT##*/}"
ENV_DIR=".venv"
LOG_DIR=".karrio"
DIST="${ROOT:?}/${ENV_DIR}/dist"
EE_DIST="${ROOT:?}/${ENV_DIR}/insiders-dist"

mkdir -p "${DIST}" "${EE_DIST}" "${LOG_DIR}"

## icon vars
cross=$'\u274c'
check=$'\u2714'


clean_build_files() {
    find $1 -type d -name dist -prune -exec rm -r '{}' \; || true
    find $1 -type d -name build -prune -exec rm -r '{}' \; || true
    # find $1 -type d -name "*.egg-info" -prune -exec rm -r '{}' \; || true
}

backup_wheels() {
    if [[ "$*" != *--insiders* ]];
    then
        find "${1}/dist" -name \*.whl -prune -exec mv '{}' "${DIST}" \;
    else
        find "${1}/dist" -name \*.whl -prune -exec mv '{}' "${EE_DIST}" \;
    fi
}
