#!/usr/bin/env bash

source "bin/activate-env.sh" > /dev/null 2>&1


# Run server commands
if [[ "$*" == *gen:graph* ]]; then
	cd "${ROOT:?}"
    apollo service:download --endpoint=http://0.0.0.0:5002/graphql/ "${ROOT:?}/server/schemas/graphql.json"
	cd -
elif [[ "$*" == *gen:openapi* ]]; then
	cd "${ROOT:?}"
    karrio spectacular --file "${ROOT:?}/server/schemas/openapi.yml"
	cd -
elif [[ "$*" == *gen:ts:cli* ]]; then
    cd "${ROOT:?}"
	mkdir -p "${ROOT:?}/.codegen"
	docker run --rm -v ${PWD}:/local openapitools/openapi-generator-cli generate \
		-i /local/server/schemas/openapi.yml \
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
        --additional-properties=invokerPackage=Karrio \
        --additional-properties=packageName=Karrio \
        --additional-properties=prependFormOrBodyParameters=true

	cd -
elif [[ "$*" == *gen:py:cli* ]]; then
	cd "${ROOT:?}"
	mkdir -p "${ROOT:?}/.codegen"
	docker run --rm -v ${PWD}:/local openapitools/openapi-generator-cli generate \
		-i /local/schemas/openapi.json \
		-g python \
		-o /local/.codegen/python \
        --additional-properties=projectName=karrio-python \
        --additional-properties=packageName=karrio

	cd -
elif [[ "$*" == *build:js* ]]; then
	cd "${ROOT:?}/.codegen/typescript"
	rm -rf node_modules;
    npm install;
    rm -f "${ROOT:?}/.codegen/typescript/api/generated/apis/index.ts"
	npx gulp build --output "${ROOT:?}/server/main/karrio/server/static/karrio/js/karrio.js"
	cd -
	karrio collectstatic --noinput
elif [[ "$*" == *build:pkgs* ]]; then
	cd "${ROOT:?}"
    rm -rf "${DIST}/*"

    # Generate ts client
    . ${ROOT}/bin/server.sh gen:ts:cli || exit 1

    # Build js client
    . ${ROOT}/bin/server.sh build:js || exit 1

    # Build server packages
    sm=$(find "${ROOT:?}/server" -type f -name "setup.py" ! -path "*$ENV_DIR/*" -prune -exec dirname '{}' \;  2>&1 | grep -v 'permission denied')

    for module in ${sm}; do
		./bin/build-package-wheel.sh "${module}" || exit 1
    done

	cd -
elif [[ "$*" == *build:ee* ]]; then
	cd "${ROOT:?}"
    rm -rf "${EE_DIST}/*"
    sm=$(find "${CLOUD_SERVER:?}" -type f -name "setup.py" ! -path "*$ENV_DIR/*" ! -path "*sdk/*" -prune -exec dirname '{}' \;  2>&1 | grep -v 'permission denied')

    for module in ${sm}; do
		./bin/build-package-wheel.sh "${module}" --ee || exit 1
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
