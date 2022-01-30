#!/usr/bin/env bash

source "scripts/activate-env.sh" > /dev/null 2>&1

# Run SDK commands
if [[ "$*" == *build:pkgs* ]]; then
	cd "${ROOT:?}"
    rm -rf "${DIST}/*"
    sm=$(find "${ROOT:?}/sdk" -type f -name "setup.py" ! -path "*$ENV_DIR/*" -prune -exec dirname '{}' \;  2>&1 | grep -v 'permission denied')

    for module in ${sm}; do
		./scripts/build-package-wheel.sh "${module}" || exit 1
    done

	cd -
elif [[ "$*" == *build:insiders* ]]; then
	cd "${ROOT:?}"
    rm -rf "${EE_DIST}/*"
    sm=$(find "${ROOT:?}/insiders/sdk" -type f -name "setup.py" ! -path "*$ENV_DIR/*" -prune -exec dirname '{}' \;  2>&1 | grep -v 'permission denied')

    for module in ${sm}; do
		./scripts/build-package-wheel.sh "${module}" --insiders || exit 1
    done

	cd -
else
    echo "Help: You can pass any the following commands to the sdk scripts"
    echo "-----"
    echo "build:pkgs - Build SDK packages"
fi
