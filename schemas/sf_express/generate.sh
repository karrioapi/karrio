#!/usr/bin/env bash

SCHEMAS=./schemas
LIB_MODULES=./sf_express_lib
find "${LIB_MODULES}" -name "*.py" -exec rm -r {} \;
touch "${LIB_MODULES}/__init__.py"

generateDS --no-namespace-defs -o "${LIB_MODULES}/route_request.py" $SCHEMAS/route_request.xsd
generateDS --no-namespace-defs -o "${LIB_MODULES}/route_response.py" $SCHEMAS/route_response.xsd
