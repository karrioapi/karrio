SCHEMAS=./schemas
LIB_MODULES=./ups_lib
mkdir -p $LIB_MODULES
find "${LIB_MODULES}" -name "*.py" -exec rm -r {} \;
touch "${LIB_MODULES}/__init__.py"

quicktype () {
    echo "Generating $1..."
    docker run -it -v $PWD:/app -e SCHEMAS=/app/schemas -e LIB_MODULES=/app/ups_lib \
    karrio/tools /quicktype/script/quicktype --no-uuids --no-date-times --no-enums --src-lang json --lang jstruct \
    --no-nice-property-names --all-properties-optional --type-as-suffix $@
}

generateDS --no-namespace-defs -o "${LIB_MODULES}/av_request.py" "${SCHEMAS}/AVRequest.xsd"
generateDS --no-namespace-defs -o "${LIB_MODULES}/av_response.py" "${SCHEMAS}/AVResponse.xsd"
generateDS --no-namespace-defs -o "${LIB_MODULES}/access_request.py" "${SCHEMAS}/AccessRequest.xsd"
generateDS --no-namespace-defs -o "${LIB_MODULES}/error_1_1.py" "${SCHEMAS}/Error1.1.xsd"
generateDS --no-namespace-defs -o "${LIB_MODULES}/freight_pickup_web_service_schema.py" "${SCHEMAS}/FreightPickupWebServiceSchema.xsd"
generateDS --no-namespace-defs -o "${LIB_MODULES}/freight_rate_web_service_schema.py" "${SCHEMAS}/FreightRateWebServiceSchema.xsd"
generateDS --no-namespace-defs -o "${LIB_MODULES}/freight_ship_web_service_schema.py" "${SCHEMAS}/FreightShipWebServiceSchema.xsd"
generateDS --no-namespace-defs -o "${LIB_MODULES}/paperless_document_api.py" "${SCHEMAS}/PaperlessDocumentAPI.xsd"
generateDS --no-namespace-defs -o "${LIB_MODULES}/pickup_web_service_schema.py" "${SCHEMAS}/PickupWebServiceSchema.xsd"
generateDS --no-namespace-defs -o "${LIB_MODULES}/rate_web_service_schema.py" "${SCHEMAS}/RateWebServiceSchema.xsd"
generateDS --no-namespace-defs -o "${LIB_MODULES}/ship_web_service_schema.py" "${SCHEMAS}/ShipWebServiceSchema.xsd"
generateDS --no-namespace-defs -o "${LIB_MODULES}/ups_security.py" "${SCHEMAS}/UPSSecurity.xsd"
generateDS --no-namespace-defs -o "${LIB_MODULES}/void_web_service_schema.py" "${SCHEMAS}/VoidWebServiceSchema.xsd"
generateDS --no-namespace-defs -o "${LIB_MODULES}/common.py" "${SCHEMAS}/common.xsd"


quicktype --src="${SCHEMAS}/rest_error.json" --out="${LIB_MODULES}/rest_error.py"
quicktype --src="${SCHEMAS}/rest_tracking_response.json" --out="${LIB_MODULES}/rest_tracking_response.py"
quicktype --src="${SCHEMAS}/document_upload_request.json" --out="${LIB_MODULES}/document_upload_request.py"
quicktype --src="${SCHEMAS}/document_upload_response.json" --out="${LIB_MODULES}/document_upload_response.py"
