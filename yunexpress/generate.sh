#!/usr/bin/env bash

SCHEMAS=./schemas
LIB_MODULES=./yunexpress_lib
find "${LIB_MODULES}" -name "*.py" -exec rm -r {} \;
touch "${LIB_MODULES}/__init__.py"

generateDS --no-namespace-defs -o "${LIB_MODULES}/tracking.py" $SCHEMAS/tracking.xsd
