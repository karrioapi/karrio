#!/usr/bin/env bash

source "scripts/activate-env.sh"

echo "running sdk typecheck with mypy"
packages=$(find "sdk" -type f -name "pyproject.toml" ! -path "sdk/pyproject.toml" -exec dirname '{}' \;)
for module in ${packages}; do
    for submodule in $(find ${module} -type f -name "__init__.py" ! -path "*tests*"  ! -path "*_lib*" -exec dirname '{}' \;); do
        mypy ${submodule} || exit $?;
    done;
done
