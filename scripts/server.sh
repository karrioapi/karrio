#!/usr/bin/env bash

source "scripts/activate-env.sh" > /dev/null 2>&1

# Export environment variables
export DEBUG_MODE=True
export DATABASE_PORT=5432
export DATABASE_NAME=db
export DATABASE_ENGINE=postgresql_psycopg2
export DATABASE_USERNAME=postgres
export DATABASE_PASSWORD=postgres
export LOG_DIR="${ROOT:?}/.pship"
export WORKER_DB_DIR="${ROOT:?}/.pship"
export SECRET_KEY="n*s-ex6@ex_r1i%bk=3jd)p+lsick5bi*90!mbk7rc3iy_op1r"

if command -v docker-machine &> /dev/null
then
    export DATABASE_HOST=$(docker-machine ip)
else
    export DATABASE_HOST="0.0.0.0"
fi


# Run server commands
if [[ "$*" == *gen:graph* ]]; then
	cd "${ROOT:?}"
	purplship graphql_schema --out "${ROOT:?}/server/schemas/graphql.json"
	cd -
elif [[ "$*" == *gen:openapi* ]]; then
	cd "${ROOT:?}"
    docker rm -f swagger 2> /dev/null
	purplship generate_swagger -f json -o -u https://app.purplship.com "${ROOT:?}/server/schemas/swagger.json"
	docker run -d -p 8085:8080 --rm --name swagger swaggerapi/swagger-converter:v1.0.2
	sleep 5 &&
	curl -X POST -H "Content-Type: application/json" \
		-d @./server/schemas/swagger.json http://localhost:8085/api/convert \
		| python -m json.tool >| ./server/schemas/openapi.json
	docker rm -f swagger
	cd -
elif [[ "$*" == *gen:ts:cli* ]]; then
    cd "${ROOT:?}"
	mkdir -p "${ROOT:?}/.codegen"
	docker run --rm -v ${PWD}:/local openapitools/openapi-generator-cli generate \
		-i /local/server/schemas/openapi.json \
        -g typescript-fetch \
		-o /local/.codegen/typescript/api/generated \
        --additional-properties=typescriptThreePlus=true \
        --additional-properties=modelPropertyNaming=snake_case \
        --additional-properties=useSingleRequestParameter=True

	cd -
elif [[ "$*" == *gen:php:cli* ]]; then
    cd "${ROOT:?}"
	mkdir -p "${ROOT:?}/.codegen"
	docker run --rm -v ${PWD}:/local openapitools/openapi-generator-cli generate \
		-i /local/server/schemas/openapi.json \
		-g php \
		-o /local/.codegen/php \
        --additional-properties=invokerPackage=Purplship \
        --additional-properties=packageName=Purplship \
        --additional-properties=prependFormOrBodyParameters=true

	cd -
elif [[ "$*" == *gen:py:cli* ]]; then
	cd "${ROOT:?}"
	mkdir -p "${ROOT:?}/.codegen"
	docker run --rm -v ${PWD}:/local openapitools/openapi-generator-cli generate \
		-i /local/schemas/openapi.json \
		-g python \
		-o /local/.codegen/python \
        --additional-properties=projectName=purplship-python \
        --additional-properties=packageName=purplship

	cd -
elif [[ "$*" == *build:js* ]]; then
	cd "${ROOT:?}/.codegen/typescript"
	rm -rf node_modules;
    yarn;
    rm -f "${ROOT:?}/.codegen/typescript/api/generated/apis/index.ts"
	npx gulp build --output "${ROOT:?}/server/main/purplship/server/static/purplship/js/purplship.js"
	cd -
	purplship collectstatic --noinput
elif [[ "$*" == *build:pkgs* ]]; then
	cd "${ROOT:?}"
    rm -rf "${DIST}/*"

    # Generate ts client
    . ${ROOT}/scripts/server.sh gen:ts:cli || exit 1

    # Build js client
    . ${ROOT}/scripts/server.sh build:js || exit 1

    # Build server packages
    sm=$(find "${ROOT:?}/server" -type f -name "setup.py" ! -path "*$ENV_DIR/*" -prune -exec dirname '{}' \;  2>&1 | grep -v 'permission denied')

    for module in ${sm}; do
		./scripts/build-package-wheel.sh "${module}" || exit 1
    done

	cd -
elif [[ "$*" == *build:insiders* ]]; then
	cd "${ROOT:?}"
    rm -rf "${EE_DIST}/*"
    sm=$(find "${ROOT:?}/insiders" -type f -name "setup.py" ! -path "*$ENV_DIR/*" -prune -exec dirname '{}' \;  2>&1 | grep -v 'permission denied')

    for module in ${sm}; do
		./scripts/build-package-wheel.sh "${module}" --insiders || exit 1
    done

	cd -
else
    echo "Help: You can pass any the following commands to the server"
    echo "-----"
    echo "gen:graph - Generate GraphQL schema"
    echo "gen:openapi - Generate OpenAPI schema"
    echo "gen:ts:cli - Generate TypeScript client"
    echo "gen:php:cli - Generate PHP client"
    echo "gen:py:cli - Generate Python client"
    echo "build:pkgs - Build server packages"
    echo "build:ee - Build enterprise packages"
fi
