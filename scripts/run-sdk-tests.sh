#!/usr/bin/env bash

source "scripts/activate-env.sh"

echo "running sdk tests with python unittest"
packages=$(find sdk insiders/sdk -type d -name "tests" -exec dirname '{}' \;)
for module in ${packages}; do
    python -m unittest discover -v -f ${module}/tests || exit $?;
done
