SCHEMAS=./schemas
LIB_MODULES=./sendle_lib
find "${LIB_MODULES}" -name "*.py" -exec rm -r {} \;
touch "${LIB_MODULES}/__init__.py"

quicktype () {
    echo "Generating $1..."
    docker run -it -v $PWD:/app -e SCHEMAS=/app/schemas -e LIB_MODULES=/app/sendle_lib \
    purplship/tools /quicktype/script/quicktype --no-uuids --no-date-times --no-enums --src-lang json --lang jstruct \
    --all-properties-optional $@
}

quicktype --src="${SCHEMAS}/order_cancel_response.json" --out="${LIB_MODULES}/order_cancel_response.py"
quicktype --src="${SCHEMAS}/order_request.json" --out="${LIB_MODULES}/order_request.py"
quicktype --src="${SCHEMAS}/order_response.json" --out="${LIB_MODULES}/order_response.py"
quicktype --src="${SCHEMAS}/rating.json" --out="${LIB_MODULES}/rating.py"
quicktype --src="${SCHEMAS}/tracking_response.json" --out="${LIB_MODULES}/tracking_response.py"
quicktype --src="${SCHEMAS}/validation_error.json" --out="${LIB_MODULES}/validation_error.py"
