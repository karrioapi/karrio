SCHEMAS=./schemas
LIB_MODULES=./easypost_lib
find "${LIB_MODULES}" -name "*.py" -exec rm -r {} \;
touch "${LIB_MODULES}/__init__.py"

quicktype () {
    echo "Generating $1..."
    docker run -it -v $PWD:/app -e SCHEMAS=/app/schemas -e LIB_MODULES=/app/easypost_lib \
    karrio/tools /quicktype/script/quicktype --no-uuids --no-date-times --no-enums --src-lang json --lang jstruct \
    --all-properties-optional $@
}

quicktype --src="${SCHEMAS}/error.json" --out="${LIB_MODULES}/error.py"
quicktype --src="${SCHEMAS}/buy_shipment.json" --out="${LIB_MODULES}/buy_shipment.py"
quicktype --src="${SCHEMAS}/create_shipment.json" --out="${LIB_MODULES}/create_shipment.py"
quicktype --src="${SCHEMAS}/trackers_response.json" --out="${LIB_MODULES}/trackers_response.py"
quicktype --src="${SCHEMAS}/shipments_response.json" --out="${LIB_MODULES}/shipments_response.py"
