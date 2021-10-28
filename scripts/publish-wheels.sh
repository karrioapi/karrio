#!/usr/bin/env bash

source "scripts/activate-env.sh" > /dev/null 2>&1

echo 'uploading wheels...'
pip install twine &&
twine upload "${DIST}/*"
