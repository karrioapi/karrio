SCHEMAS=./schemas
LIB_MODULES=./easypost_lib
find "${LIB_MODULES}" -name "*.py" -exec rm -r {} \;
touch "${LIB_MODULES}/__init__.py"

quicktype () {
    echo "Generating $1..."
    docker run -it -v $PWD:/app -e SCHEMAS=/app/schemas -e LIB_MODULES=/app/easypost_lib \
    karrio/tools /quicktype/script/quicktype --no-uuids --no-date-times --no-enums --src-lang json --lang jstruct \
    --no-nice-property-names --all-properties-optional $@
}

quicktype --src="${SCHEMAS}/error.json" --out="${LIB_MODULES}/error.py"
quicktype --src="${SCHEMAS}/shipment.json" --out="${LIB_MODULES}/shipment.py"
quicktype --src="${SCHEMAS}/shipment_request.json" --out="${LIB_MODULES}/shipment_request.py"
quicktype --src="${SCHEMAS}/tracker.json" --out="${LIB_MODULES}/tracker.py"
