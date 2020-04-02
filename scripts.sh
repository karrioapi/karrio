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
    pip install -r requirements.dev.txt
}


alias env:new=create_env
alias env:on=activate_env
alias env:reset=init


# Project helpers

run_server() {
    (echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'password')" | python manage.py shell);
    python manage.py makemigrations && python manage.py migrate && python manage.py runserver
}

run_prod() {
    export APP_STAGE="production"
    run_server
}
alias run:prod=run_prod

run_dev() {
    export APP_STAGE="developement"
    run_server
}
alias run:dev=run_dev

run_container() {
    export APP_STAGE="containerized"
    docker-compose up "$@"
}
alias run:container=run_container

env:on || true
