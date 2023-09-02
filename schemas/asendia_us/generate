SCHEMAS=./schemas
LIB_MODULES=./asendia_us_lib
find "${LIB_MODULES}" -name "*.py" -exec rm -r {} \;
touch "${LIB_MODULES}/__init__.py"

quicktype () {
    echo "Generating $1..."
    docker run -it -v $PWD:/app -e SCHEMAS=/app/schemas -e LIB_MODULES=/app/asendia_us_lib \
    karrio/tools /quicktype/script/quicktype --no-uuids --no-date-times --no-enums --src-lang json --lang jstruct \
    --no-nice-property-names --all-properties-optional $@
}

quicktype --src="${SCHEMAS}/shipping_close_dispatch_request.json" --out="${LIB_MODULES}/shipping_close_dispatch_request.py"
quicktype --src="${SCHEMAS}/shipping_close_dispatch_response.json" --out="${LIB_MODULES}/shipping_close_dispatch_response.py"
quicktype --src="${SCHEMAS}/shipping_rate_request.json" --out="${LIB_MODULES}/shipping_rate_request.py"
quicktype --src="${SCHEMAS}/shipping_rate_response.json" --out="${LIB_MODULES}/shipping_rate_response.py"
quicktype --src="${SCHEMAS}/shipping_request.json" --out="${LIB_MODULES}/shipping_request.py"
quicktype --src="${SCHEMAS}/shipping_response.json" --out="${LIB_MODULES}/shipping_response.py"
quicktype --src="${SCHEMAS}/tracking_details_response.json" --out="${LIB_MODULES}/tracking_details_response.py"
quicktype --src="${SCHEMAS}/tracking_milestone_response.json" --out="${LIB_MODULES}/tracking_milestone_response.py"
