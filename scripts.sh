#!/usr/bin/env bash

# Python virtual environment helpers

ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
BASE_DIR="${PWD##*/}"
ENV_DIR=".venv"

export DEBUG_MODE=True

export DATABASE_PORT=5432
export DATABASE_NAME=db
export DATABASE_ENGINE=postgresql_psycopg2
export DATABASE_USERNAME=postgres
export DATABASE_PASSWORD=postgres

export SECRET_KEY="n*s-ex6@ex_r1i%bk=3jd)p+lsick5bi*90!mbk7rc3iy_op1r"
export wheels=~/Wheels
export PIP_FIND_LINKS="https://git.io/purplship"
[[ -d "$wheels" ]] && export PIP_FIND_LINKS="${PIP_FIND_LINKS} file://${wheels}"

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
    create_env &&
    pip install -r "${ROOT:?}/requirements.dev.txt" &&

    if [[ "$*" != *--no-insider* ]];
	then
    	pip install -r "${ROOT:?}/requirements.insider.dev.txt"
	fi
}


# Project helpers
add_data () {
  echo "> setup superuser and initial data"
  if [[ "$MULTI_TENANT_ENABLE" == "True" ]];
  then

    (echo "
from purpleserver.tenants.models import Client, Domain
if not any(Client.objects.all()):
  Domain.objects.create(domain='localhost', tenant=Client.objects.create(name='public', schema_name='public'))
  Domain.objects.create(domain='127.0.0.1', tenant=Client.objects.create(name='purplship', schema_name='purplship'))
" | purplship shell) > /dev/null 2>&1;

    (echo "
from django_tenants.utils import tenant_context
from django.contrib.auth import get_user_model
from purpleserver.tenants.models import Client
with tenant_context(Client.objects.get(schema_name='public')):
  if not any(get_user_model().objects.all()):
     get_user_model().objects.create_superuser('root@domain.com', 'demo')
with tenant_context(Client.objects.get(schema_name='purplship')):
  if not any(get_user_model().objects.all()):
     get_user_model().objects.create_superuser('admin@domain.com', 'demo')
" | purplship shell) > /dev/null 2>&1;

  else

    (echo "
from django.contrib.auth import get_user_model
if not any(get_user_model().objects.all()):
   get_user_model().objects.create_superuser('admin@domain.com', 'demo')
" | purplship shell) > /dev/null 2>&1;

    (echo "from django.contrib.auth import get_user_model; from purpleserver.user.models import Token; Token.objects.create(user=get_user_model().objects.first(), key='key_3d601f1394b2ee95f412567c29d599a6')" | purplship shell) > /dev/null 2>&1;

    (echo "from purpleserver.providers.extension.models.canadapost import SETTINGS;
SETTINGS.objects.create(carrier_id='canadapost', test=True, username='6e93d53968881714', customer_number='2004381', contract_id='42708517', password='0bfa9fcb9853d1f51ee57a')" | purplship shell) > /dev/null 2>&1;
  fi
}

migrate () {
  echo "> update database migrations"
  purplship makemigrations &> /dev/null

  echo "> migrate database schemas"
  if [[ "$MULTI_TENANT_ENABLE" == "True" ]];
  then
    purplship migrate_schemas --shared &> /dev/null
  else
    purplship migrate &> /dev/null
  fi

  add_data

  echo "> collect static files"
  purplship collectstatic --noinput
}

runservices() {
  cd "${ROOT:?}"
  docker-compose down &&
  docker-compose up "$@"
  cd -
}

# shellcheck disable=SC2120
rundb() {
  cd "${ROOT:?}"
  docker-compose down &&
  docker-compose up -d db adminer

  if command -v docker-machine &> /dev/null
  then
    export DATABASE_HOST=$(docker-machine ip)
  else
    export DATABASE_HOST="0.0.0.0"
  fi

  sleep 5
  cd -
}

stopdb() {
	cd "${ROOT:?}"
	docker-compose down
	cd -
}

kill_server() {
	lsof -i tcp:8000 | tail -n +2 | awk '{print $2}' | xargs kill -9
	pkill purplship
	pkill Python
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
		migrate
	fi

	gunicorn --config "${ROOT:?}/gunicorn-cfg.py" purpleserver.asgi -k uvicorn.workers.UvicornWorker &
	sleep 1
	purplship run_huey -w 2

	kill_server
	sleep 1
}

run_mail_server() {
  python -m smtpd -n -c DebuggingServer localhost:1025
}

test() {
	if [[ "$*" == *--rdb* ]]; then
		rundb
	fi

	purplship test --failfast purpleserver.proxy.tests &&
	purplship test --failfast purpleserver.pricing.tests &&
	purplship test --failfast purpleserver.manager.tests &&
	purplship test --failfast purpleserver.events.tests &&
	purplship test --failfast purpleserver.graph.tests
}

test_services() {
  TEST=True docker-compose up --build --exit-code-from=pship pship
}

clean_builds() {
    find . -type d -not -path "*$ENV_DIR/*" -name dist -prune -exec rm -r '{}' \; 2>/dev/null || true
    find . -type d -not -path "*$ENV_DIR/*" -name build -prune -exec rm -r '{}' \; 2>/dev/null || true
}

backup_wheels() {
    # shellcheck disable=SC2154
    [[ -d "$wheels" ]] &&
    find . -not -path "*$ENV_DIR/*" -name \*.whl -prune -exec mv '{}' "$wheels" \; 2>/dev/null &&
    clean_builds
}

_build() {
  pushd "$1" || false &&
  python setup.py bdist_wheel
  popd || true
}

build() {
  build_theme -i &&
  build_dashboard &&
  build_js -i &&
  clean_builds
  sm=$(find "${ROOT:?}" -type f -name "setup.py" ! -path "*$ENV_DIR/*" -prune -exec dirname '{}' \;  2>&1 | grep -v 'permission denied')

  while read -r module; do
    echo ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> building ${module} ..."
    _build "${module}" || break
  done <<< $sm
  backup_wheels
}

build_theme() {
  	cd "${ROOT:?}/webapp" || false &&
	if [[ "$*" == *-i* ]]; then
		rm -rf node_modules; yarn
	fi
	yarn build:theme "${ROOT:?}/purpleserver/purpleserver/static/purpleserver/css/purplship.theme.min.css"
	cd - || true
	purplship collectstatic --noinput
}

build_dashboard() {
  	cd "${ROOT:?}/webapp" || false &&
	if [[ "$*" == *-i* ]]; then
		rm -rf node_modules; yarn
	fi
	yarn build --output-path "${ROOT:?}/apps/client/purpleserver/client/static/client/"
	cd -
	purplship collectstatic --noinput
}

build_js() {
	cd "${ROOT:?}/webapp/api" || false &&
	if [[ "$*" == *-i* ]]; then
		rm -rf node_modules; yarn
	fi
	npx gulp build --output "${ROOT:?}/purpleserver/purpleserver/static/purpleserver/js/purplship.js"
	cd -
	purplship collectstatic --noinput
}

dev_webapp() {
  cd "${ROOT:?}/webapp" || false &&
  rm -rf node_modules;
  yarn && yarn build -w \
    --env postbuild="purplship collectstatic --noinput" \
    --output-path "${ROOT:?}/apps/client/purpleserver/client/static/client/"
  cd -
}

build_image() {
  docker build -t "purplship/purplship-server:$1" -f "${ROOT:?}/.docker/Dockerfile" "${ROOT:?}" --no-cache
}

generate_node_client() {
	cd "${ROOT:?}"
	mkdir -p "${ROOT:?}/codegen"
	docker run --rm -v ${PWD}:/local openapitools/openapi-generator-cli generate \
		-i /local/schemas/openapi.json \
		-g javascript \
		-o /local/codegen/node \
		-c /local/artifacts/config.json

	cd -
}

generate_typescript_client() {
	cd "${ROOT:?}"
	docker run --rm -v ${PWD}:/local openapitools/openapi-generator-cli generate \
		-i /local/schemas/openapi.json \
		-g typescript-fetch \
		-o /local/webapp/api \
		-c /local/artifacts/config.json \
		--additional-properties=typescriptThreePlus=true

	cd -
  
	rm -f "${ROOT:?}/webapp/api/apis/index.ts"
	rm -f "${ROOT:?}/webapp/api/.openapi-generator-ignore"
	rm -rf "${ROOT:?}/webapp/api/.openapi-generator/"

	cd "${ROOT:?}/webapp" && git checkout "./api/index.ts"; cd -
}

generate_php_client() {
	cd "${ROOT:?}"
	mkdir -p "${ROOT:?}/codegen"
	docker run --rm -v ${PWD}:/local openapitools/openapi-generator-cli generate \
		-i /local/schemas/openapi.json \
		-g php \
		-o /local/codegen/php

	cd -
}

generate_python_client() {
	cd "${ROOT:?}"
	mkdir -p "${ROOT:?}/codegen"
	docker run --rm -v ${PWD}:/local openapitools/openapi-generator-cli generate \
		-i /local/schemas/openapi.json \
		-g python \
		-o /local/codegen/python

	cd -
}

generate_graphql_schema() {
	cd "${ROOT:?}"
	purplship graphql_schema --out "${ROOT:?}/schemas/graphql.json"
	apollo-codegen generate "${ROOT:?}/webapp/graphql/queries.ts" \
		--schema "${ROOT:?}/schemas/graphql.json" \
		--target typescript \
		--output "${ROOT:?}/webapp/graphql/types.ts"
	cd -
}

generate_api_schema() {
	cd "${ROOT:?}"
	purplship generate_swagger -f json -o -u https://app.purplship.com "${ROOT:?}/schemas/swagger.json"
	docker run -d -p 8085:8080 --rm --name swagger swaggerapi/swagger-converter:v1.0.2
	sleep 4 &&
	curl -X POST -H "Content-Type: application/json" \
		-d @./schemas/swagger.json http://localhost:8085/api/convert \
		| python -m json.tool >| ./schemas/openapi.json
	docker rm -f swagger
	cd -
}

stub_server() {
echo "
from http.server import HTTPServer, BaseHTTPRequestHandler
class S(BaseHTTPRequestHandler):
    def do_POST(self):
    	try:
    		print(self.rfile.read1())
    	except:
    		pass
    	self.send_response(200)
    	self.send_header('Content-type', 'application/json')
    	self.end_headers()
    	self.wfile.write('good'.encode('utf8'))
addr = 'localhost'
port = 8080
server_address = (addr, port)
httpd = HTTPServer(server_address, S)
print(f'Starting httpd server on {addr}:{port}')
httpd.serve_forever()
" | python
}

docs() {
	cd "${ROOT:?}" && mkdocs serve -a localhost:4002; cd -
}


alias env:new=create_env
alias env:on=activate_env
alias env:off=deactivate_env
alias env:reset=init


alias run:db=rundb
alias run:server=runserver
alias run:micro=runservices
alias run:mail=run_mail_server
alias ks=kill_server


alias gen:js=generate_node_client
alias gen:ts=generate_typescript_client
alias gen:php=generate_php_client
alias gen:python=generate_python_client
alias gen:graph=generate_graphql_schema
alias gen:api=generate_api_schema


alias dev:webapp=dev_webapp


activate_env
