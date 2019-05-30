#!/usr/bin/env bash

ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
BASE_DIR="${PWD##*/}"

init() {
    deactivate || true
    rm -r $ROOT/venv || true
    mkdir -p $ROOT/venv
    python3 -m venv $ROOT/venv/$BASE_DIR &&
    source $ROOT/venv/$BASE_DIR/bin/activate &&
    pip install -r requirements.txt &&
    pip install -r requirements-dev.txt
}

run_server() {
    (echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'password')" | python manage.py shell) > /dev/null 2>&1;
    python manage.py makemigrations && python manage.py migrate && python manage.py runserver
}

run_prod() {
    APP_STAGE="production"
    run_server
}
alias run:prod=run_prod

run_dev() {
    APP_STAGE="developement"
    run_server
}
alias run:dev=run_dev

run_container() {
    APP_STAGE="containerized"
    docker-compose up "$@"
}
alias run:container=run_container
