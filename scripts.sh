#!/usr/bin/env bash

# Python virtual environment helpers

ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
BASE_DIR="${PWD##*/}"
ENV_DIR=".venv"

export PIP_FIND_LINKS="https://git.io/purplship"

deactivate_env() {
  if command -v COMMAND &> /dev/null
  then
    deactivate
  fi
}

activate_env() {
  if [[ -d "${ROOT:?}/$ENV_DIR/$BASE_DIR/bin" ]]; then
    echo "Activate $BASE_DIR"
    # shellcheck source=src/script.sh
    source "${ROOT:?}/$ENV_DIR/$BASE_DIR/bin/activate"
  fi
}

create_env() {
    echo "create $BASE_DIR Python3 env"
    deactivate_env
    rm -rf "${ROOT:?}/$ENV_DIR" || true
    mkdir -p "${ROOT:?}/$ENV_DIR"
    python3 -m venv "${ROOT:?}/$ENV_DIR/$BASE_DIR" &&
    activate_env &&
    pip install --upgrade pip wheel
}

init() {
    create_env &&
    install_all
}


alias env:new=create_env
alias env:on=activate_env
alias env:reset=init


# Project helpers

install_all() {
    pip install -e "${ROOT:?}/purpleserver[dev]" &&
    pip install -e "${ROOT:?}/purpleserver/core" &&
    pip install -e "${ROOT:?}/purpleserver/proxy" &&
    pip install -e "${ROOT:?}/purpleserver/manager" &&
    pip install -e "${ROOT:?}/purpleserver/tenants"
}

test_install() {
    pip install -r "${ROOT:?}/requirements.test.txt" &&
    install_all
}

install_released() {
  pip install purplship-server \
    purplship-server.core \
    purplship-server.proxy \
    purplship-server.extension \
    purplship.canadapost \
    purplship.dhl \
    purplship.fedex \
    purplship.purolator \
    purplship.ups \
    eshipper.extension \
    freightcom.extension
}

reset_db () {
  purplship makemigrations &&
  purplship migrate &&
  purplship collectstatic --noinput
  (echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'demo')" | purplship shell) > /dev/null 2>&1;
  (echo "from django.contrib.auth.models import User; from rest_framework.authtoken.models import Token; Token.objects.create(user=User.objects.first(), key='19707922d97cef7a5d5e17c331ceeff66f226660')" | purplship shell) > /dev/null 2>&1;
  (echo "from purpleserver.carriers.models import CanadaPostSettings; CanadaPostSettings.objects.create(carrier_id='canadapost', test=True, username='6e93d53968881714', customer_number='2004381', contract_id='42708517', password='0bfa9fcb9853d1f51ee57a')" | purplship shell) > /dev/null 2>&1;
}

run_server() {
  if [[ "$1" == "-i" ]]; then
    install_all
  fi
  reset_db
  purplship runserver
}

postgres_env() {
  export DATABASE_HOST=$(docker-machine ip)
  export DATABASE_PORT=5432
  export DATABASE_NAME=db
  export DATABASE_ENGINE=postgresql_psycopg2
  export DATABASE_USERNAME=postgres
  export DATABASE_PASSWORD=postgres
  export MULTI_TENANT_ENABLE=True
}

test() {
  purplship makemigrations &&
  purplship test --failfast purpleserver.proxy.tests &&
  purplship test --failfast purpleserver.manager.tests
}

test_with_postgres() {
  echo "clean env dir"
  deactivate_env
  [ -d "${ROOT:?}/$ENV_DIR/temp" ] && rm -rf "${ROOT:?}/$ENV_DIR/temp" && echo "env dir purged"
  docker-compose -f "${ROOT:?}/postgres.yml" up --force-recreate --exit-code-from purpleserver
}

clean_builds() {
    find . -type d -not -path "*$ENV_DIR/*" -name dist -exec rm -r {} \; || true
    find . -type d -not -path "*$ENV_DIR/*" -name build -exec rm -r {} \; || true
    find . -type d -not -path "*$ENV_DIR/*" -name "*.egg-info" -exec rm -r {} \; || true
}

backup_wheels() {
    # shellcheck disable=SC2154
    [ -d "$wheels" ] &&
    find . -not -path "*$ENV_DIR/*" -name \*.whl -exec mv {} "$wheels" \; &&
    clean_builds
}

build() {
  pushd "$1" || false &&
  python setup.py bdist_wheel
  popd || true
}

build_all() {
  clean_builds
  sm=(find "${ROOT:?}" -type f -name "setup.py" ! -path "*$ENV_DIR/*" -exec dirname {} \;)

  $sm | while read module; do
    echo "building ${module} ..."
    build "${module}" || break
  done
  backup_wheels
}

install_purplship_dev() {
  p="$(dirname "${ROOT:?}")"
  sm=(find "$p/purplship" -type f -name "setup.py" ! -path "*$ENV_DIR/*" -exec dirname {} \;)

  $sm | while read module; do
    echo "installing ${module} ..."
    pip install "${module}" --upgrade || break
  done
}

install_extension_dev() {
  p="$(dirname "${ROOT:?}")"
  sm=(find "$p/purplship-extension" -type f -name "setup.py" ! -path "*$ENV_DIR/*" -exec dirname {} \;)

  $sm | while read module; do
    echo "installing ${module} ..."
    pip install "${module}" --upgrade || break
  done
}


alias dev:purplship=install_purplship_dev
alias dev:extension=install_extension_dev
alias run=run_server

activate_env
