SCHEMAS=./schemas
LIB_MODULES=./dhl_ecom_am_lib
mkdir -p $LIB_MODULES
find "${LIB_MODULES}" -name "*.py" -exec rm -r {} \;
touch "${LIB_MODULES}/__init__.py"

quicktype () {
    echo "Generating $1..."
    docker run -it -v $PWD:/app -e SCHEMAS=/app/schemas -e LIB_MODULES=/app/dhl_ecom_am_lib \
    karrio/tools /quicktype/script/quicktype --no-uuids --no-date-times --no-enums --src-lang json --lang jstruct \
    --no-nice-property-names --all-properties-optional $@
}

quicktype --src="${SCHEMAS}/create_label_request.json" --out="${LIB_MODULES}/create_label_request.py"
quicktype --src="${SCHEMAS}/create_label_response.json" --out="${LIB_MODULES}/create_label_response.py"
quicktype --src="${SCHEMAS}/create_pickup_request.json" --out="${LIB_MODULES}/create_pickup_request.py"
quicktype --src="${SCHEMAS}/create_pickup_response.json" --out="${LIB_MODULES}/create_pickup_response.py"
quicktype --src="${SCHEMAS}/create_return_request.json" --out="${LIB_MODULES}/create_return_request.py"
quicktype --src="${SCHEMAS}/create_return_response.json" --out="${LIB_MODULES}/create_return_response.py"
quicktype --src="${SCHEMAS}/error.json" --out="${LIB_MODULES}/error.py"
quicktype --src="${SCHEMAS}/product_finder_request.json" --out="${LIB_MODULES}/product_finder_request.py"
quicktype --src="${SCHEMAS}/product_finder_response.json" --out="${LIB_MODULES}/product_finder_response.py"
quicktype --src="${SCHEMAS}/tracking_request.json" --out="${LIB_MODULES}/tracking_response.py"
quicktype --src="${SCHEMAS}/tracking_response.json" --out="${LIB_MODULES}/tracking_response.py"
