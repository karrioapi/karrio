SCHEMAS=./schemas
LIB_MODULES=./easypost_lib
find "${LIB_MODULES}" -name "*.py" -exec rm -r {} \;
touch "${LIB_MODULES}/__init__.py"

quicktype () {
    echo "Generating $1..."
    docker run -it -v $PWD:/app -e SCHEMAS=/app/schemas -e LIB_MODULES=/app/easypost_lib \
    karrio/tools /quicktype/script/quicktype --no-uuids --no-date-times --no-enums \
    --src-lang json --lang jstruct --all-properties-optional $@
}

quicktype --src="${SCHEMAS}/errors_response.json" --out="${LIB_MODULES}/errors_response.py"
quicktype --src="${SCHEMAS}/shipment_request.json" --out="${LIB_MODULES}/shipment_request.py"
quicktype --src="${SCHEMAS}/shipment_purchase.json" --out="${LIB_MODULES}/shipment_purchase.py"
quicktype --src="${SCHEMAS}/trackers_response.json" --out="${LIB_MODULES}/trackers_response.py"
quicktype --src="${SCHEMAS}/shipments_response.json" --out="${LIB_MODULES}/shipments_response.py"
