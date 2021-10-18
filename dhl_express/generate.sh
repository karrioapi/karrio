SCHEMAS=./schemas
LIB_MODULES=./dhl_express
mkdir -p $LIB_MODULES
find "${LIB_MODULES}" -name "*.py" -exec rm -r {} \;
touch "${LIB_MODULES}/__init__.py"

quicktype () {
    echo "Generating $1..."
    docker run -it -v $PWD:/app -e SCHEMAS=/app/schemas -e LIB_MODULES=/app/dhl_express \
    purplship/tools /quicktype/script/quicktype --no-uuids --no-date-times --no-enums --src-lang json --lang jstruct \
    --no-nice-property-names --all-properties-optional $@
}

quicktype --src="${SCHEMAS}/create_pickup_request.json" --out="${LIB_MODULES}/create_pickup_request.py"
quicktype --src="${SCHEMAS}/create_shipment_request.json" --out="${LIB_MODULES}/create_shipment_request.py"
quicktype --src="${SCHEMAS}/create_shipment_response.json" --out="${LIB_MODULES}/create_shipment_response.py"
quicktype --src="${SCHEMAS}/error.json" --out="${LIB_MODULES}/error.py"
quicktype --src="${SCHEMAS}/pickup_response.json" --out="${LIB_MODULES}/pickup_response.py"
quicktype --src="${SCHEMAS}/rating_request.json" --out="${LIB_MODULES}/rating_request.py"
quicktype --src="${SCHEMAS}/rating_response.json" --out="${LIB_MODULES}/rating_response.py"
quicktype --src="${SCHEMAS}/tracking_request.json" --out="${LIB_MODULES}/tracking_request.py"
quicktype --src="${SCHEMAS}/tracking_response.json" --out="${LIB_MODULES}/tracking_response.py"
quicktype --src="${SCHEMAS}/update_pickup_request.json" --out="${LIB_MODULES}/update_pickup_request.py"
quicktype --src="${SCHEMAS}/validate_address_request.json" --out="${LIB_MODULES}/validate_address_request.py"
quicktype --src="${SCHEMAS}/validate_address_response.json" --out="${LIB_MODULES}/validate_address_response.py"
