SCHEMAS=./schemas
LIB_MODULES=./ups_freight_lib
find "${LIB_MODULES}" -name "*.py" -exec rm -r {} \;
touch "${LIB_MODULES}/__init__.py"

quicktype () {
    echo "Generating $1..."
    docker run -it -v $PWD:/app -e SCHEMAS=/app/schemas -e LIB_MODULES=/app/ups_freight_lib \
    karrio/tools /quicktype/script/quicktype --no-uuids --no-date-times --no-enums --src-lang json --lang jstruct \
    --no-nice-property-names --all-properties-optional --type-as-suffix $@
}

quicktype --src="${SCHEMAS}/error.json" --out="${LIB_MODULES}/error.py"
quicktype --src="${SCHEMAS}/document_upload_request.json" --out="${LIB_MODULES}/document_upload_request.py"
quicktype --src="${SCHEMAS}/document_upload_response.json" --out="${LIB_MODULES}/document_upload_response.py"
quicktype --src="${SCHEMAS}/freight_cancel_pickup_response.json" --out="${LIB_MODULES}/freight_cancel_pickup_response.py"
quicktype --src="${SCHEMAS}/freight_pickup_request.json" --out="${LIB_MODULES}/freight_pickup_request.py"
quicktype --src="${SCHEMAS}/freight_pickup_response.json" --out="${LIB_MODULES}/freight_pickup_response.py"
quicktype --src="${SCHEMAS}/freight_rate_request.json" --out="${LIB_MODULES}/freight_rate_request.py"
quicktype --src="${SCHEMAS}/freight_rate_response.json" --out="${LIB_MODULES}/freight_rate_response.py"
quicktype --src="${SCHEMAS}/freight_ship_request.json" --out="${LIB_MODULES}/freight_ship_request.py"
quicktype --src="${SCHEMAS}/freight_ship_response.json" --out="${LIB_MODULES}/freight_ship_response.py"
quicktype --src="${SCHEMAS}/tracking_response.json" --out="${LIB_MODULES}/tracking_response.py"
