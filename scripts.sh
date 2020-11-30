#!/usr/bin/env bash

# Python virtual environment helpers

ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
BASE_DIR="${PWD##*/}"
ENV_DIR=".venv"

export SECRET_KEY="n*s-ex6@ex_r1i%bk=3jd)p+lsick5bi*90!mbk7rc3iy_op1r"
export wheels=~/Wheels
export PIP_FIND_LINKS="https://git.io/purplship"
[[ -d "$wheels" ]] && export PIP_FIND_LINKS=file://${wheels}

#export EMAIL_HOST="smtp.gmail.com"
#export EMAIL_PORT=587
#export EMAIL_USE_TLS=True
#export EMAIL_HOST_USER=""
#export EMAIL_HOST_PASSWORD=""

deactivate_env() {
  if command -v deactivate &> /dev/null
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
    create_env && pip install -r "${ROOT:?}/requirements.dev.txt"
}


alias env:new=create_env
alias env:on=activate_env
alias env:off=deactivate_env
alias env:reset=init


# Project helpers

install_released() {
  pip install purplship-server \
    purplship-server.core \
    purplship-server.proxy \
    purplship-server.extension \
    purplship.canadapost \
    purplship.dhl_express \
    purplship.fedex_express \
    purplship.purolator_courier \
    purplship.ups_package \
    freightcom.extension \
    eshipper.extension
}

migrate () {
  if [[ "$MULTI_TENANT_ENABLE" == "True" ]];
  then
    migrate="purplship migrate_schemas --shared"
  else
    migrate="purplship migrate"
  fi

  purplship makemigrations &&
  eval "$migrate" &&
  purplship collectstatic --noinput

  if [[ "$MULTI_TENANT_ENABLE" == "True" ]];
  then
    (echo "
from purpleserver.tenants.models import Client; Client.objects.create(name='public', schema_name='public', domain_url='localhost')
" | purplship shell) > /dev/null 2>&1;
    (echo "
from django.contrib.auth import get_user_model; get_user_model().objects.create_superuser('root@test.com', 'demo')
" | purplship shell) > /dev/null 2>&1;

    (echo "
from purpleserver.tenants.models import Client; Client.objects.create(name='purpleserver', schema_name='purpleserver', domain_url='127.0.0.1')
" | purplship shell) > /dev/null 2>&1;
    (echo "
from tenant_schemas.utils import tenant_context
from django.contrib.auth import get_user_model
from purpleserver.tenants.models import Client
with tenant_context(Client.objects.get(schema_name='purpleserver')):
  get_user_model().objects.create_superuser('admin@test.com', 'demo')
" | purplship shell) > /dev/null 2>&1;
  else
    (echo "from django.contrib.auth import get_user_model; get_user_model().objects.create_superuser('admin@test.com', 'demo')" | purplship shell) > /dev/null 2>&1;
    (echo "from django.contrib.auth import get_user_model; from rest_framework.authtoken.models import Token; Token.objects.create(user=get_user_model().objects.first(), key='19707922d97cef7a5d5e17c331ceeff66f226660')" | purplship shell) > /dev/null 2>&1;
    (echo "from django.contrib.auth import get_user_model; from purpleserver.providers.models import CanadaPostSettings;
CanadaPostSettings.objects.create(carrier_id='canadapost', test=True, username='6e93d53968881714', customer_number='2004381', contract_id='42708517', password='0bfa9fcb9853d1f51ee57a', user=get_user_model().objects.first())" | purplship shell) > /dev/null 2>&1;
  fi

}

runservices() {
  docker-compose down &&
  docker-compose up "$@"
}

# shellcheck disable=SC2120
rundb() {
  docker-compose down &&
  docker-compose up -d db

  if command -v docker-machine &> /dev/null
  then
    export DATABASE_HOST=$(docker-machine ip)
  else
    export DATABASE_HOST="0.0.0.0"
  fi

  export DATABASE_PORT=5432
  export DATABASE_NAME=db
  export DATABASE_ENGINE=postgresql_psycopg2
  export DATABASE_USERNAME=postgres
  export DATABASE_PASSWORD=postgres

  sleep 5
}

runserver() {
  if [[ "$*" = *--tenants* ]];
  then
    export MULTI_TENANT_ENABLE=True
  else
    export MULTI_TENANT_ENABLE=False
  fi

  if [[ "$*" == *--rdb* ]]; then
    rundb
  fi

  if [[ "$*" == *--rdata* ]]; then
    migrate "$@"
  fi

  purplship runserver
}

run_mail_server() {
  python -m smtpd -n -c DebuggingServer localhost:1025
}

test() {
  purplship test --failfast purpleserver.proxy.tests &&
  purplship test --failfast purpleserver.pricing.tests &&
  purplship test --failfast purpleserver.manager.tests
}

test_services() {
  TEST=True docker-compose up --build --exit-code-from=purpleserver purpleserver
}

clean_builds() {
    find . -type d -not -path "*$ENV_DIR/*" -name dist -exec rm -r {} \; 2>/dev/null || true
    find . -type d -not -path "*$ENV_DIR/*" -name build -exec rm -r {} \; 2>/dev/null || true
    find . -type d -not -path "*$ENV_DIR/*" -name "*.egg-info" -exec rm -r {} \; 2>/dev/null || true
}

backup_wheels() {
    # shellcheck disable=SC2154
    [[ -d "$wheels" ]] &&
    find . -not -path "*$ENV_DIR/*" -name \*.whl -exec mv {} "$wheels" \; 2>/dev/null &&
    clean_builds
}

_build() {
  pushd "$1" || false &&
  python setup.py bdist_wheel
  popd || true
}

build() {
  clean_builds
  sm=$(find "${ROOT:?}" -type f -name "setup.py" ! -path "*$ENV_DIR/*" -exec dirname {} \;  2>&1 | grep -v 'permission denied')

  while read -r module; do
    echo ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> building ${module} ..."
    _build "${module}" || break
  done <<< $sm
  backup_wheels
}

build_theme() {
  pushd "${ROOT:?}/src/theme" || false &&
  yarn && yarn build
  popd || true
}

build_client() {
  pushd "${ROOT:?}/src/frontend" || false &&
  yarn && yarn build "$@"
  popd
}

build_image() {
  docker build -t "purplship/purplship-server:$1" -f "${ROOT:?}/docker/Dockerfile" "${ROOT:?}"
}


alias run:db=rundb
alias run:server=runserver
alias run:micro=runservices
alias run:mail=run_mail_server

activate_env
