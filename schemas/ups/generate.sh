SCHEMAS=./schemas
LIB_MODULES=./ups_lib
mkdir -p $LIB_MODULES
find "${LIB_MODULES}" -name "*.py" -exec rm -r {} \;
touch "${LIB_MODULES}/__init__.py"

quicktype () {
    echo "Generating $1..."
    docker run -it -v $PWD:/app -e SCHEMAS=/app/schemas -e LIB_MODULES=/app/ups_lib \
    purplship/tools /quicktype/script/quicktype --no-uuids --no-date-times --no-enums --src-lang json --lang jstruct \
    --no-nice-property-names --all-properties-optional $@
}

generateDS --no-namespace-defs -o "${LIB_MODULES}/av_request.py" "${SCHEMAS}/AVRequest.xsd"
generateDS --no-namespace-defs -o "${LIB_MODULES}/av_response.py" "${SCHEMAS}/AVResponse.xsd"
generateDS --no-namespace-defs -o "${LIB_MODULES}/access_request.py" "${SCHEMAS}/AccessRequest.xsd"
generateDS --no-namespace-defs -o "${LIB_MODULES}/access_request_xpci.py" "${SCHEMAS}/AccessRequestXPCI.xsd"
generateDS --no-namespace-defs -o "${LIB_MODULES}/dangerous_goods_utility.py" "${SCHEMAS}/DangerousGoodsUtility.xsd"
generateDS --no-namespace-defs -o "${LIB_MODULES}/denied_party_web_service_schema.py" "${SCHEMAS}/DeniedPartyWebServiceSchema.xsd"
generateDS --no-namespace-defs -o "${LIB_MODULES}/error_1_1.py" "${SCHEMAS}/Error1.1".xsd
generateDS --no-namespace-defs -o "${LIB_MODULES}/error_xpci.py" "${SCHEMAS}/ErrorXPCI.xsd"
generateDS --no-namespace-defs -o "${LIB_MODULES}/freight_pickup_web_service_schema.py" "${SCHEMAS}/FreightPickupWebServiceSchema.xsd"
generateDS --no-namespace-defs -o "${LIB_MODULES}/freight_rate_web_service_schema.py" "${SCHEMAS}/FreightRateWebServiceSchema.xsd"
generateDS --no-namespace-defs -o "${LIB_MODULES}/freight_ship_web_service_schema.py" "${SCHEMAS}/FreightShipWebServiceSchema.xsd"
generateDS --no-namespace-defs -o "${LIB_MODULES}/ifws.py" "${SCHEMAS}/IFWS.xsd"
generateDS --no-namespace-defs -o "${LIB_MODULES}/lb_recovery.py" "${SCHEMAS}/LBRecovery.xsd"
generateDS --no-namespace-defs -o "${LIB_MODULES}/landed_cost_web_service_schema.py" "${SCHEMAS}/LandedCostWebServiceSchema.xsd"
generateDS --no-namespace-defs -o "${LIB_MODULES}/locator_request.py" "${SCHEMAS}/LocatorRequest.xsd"
generateDS --no-namespace-defs -o "${LIB_MODULES}/locator_response.py" "${SCHEMAS}/LocatorResponse.xsd"
generateDS --no-namespace-defs -o "${LIB_MODULES}/paperless_document_api.py" "${SCHEMAS}/PaperlessDocumentAPI.xsd"
generateDS --no-namespace-defs -o "${LIB_MODULES}/pickup_web_service_schema.py" "${SCHEMAS}/PickupWebServiceSchema.xsd"
generateDS --no-namespace-defs -o "${LIB_MODULES}/pre_notification_web_service_schema.py" "${SCHEMAS}/PreNotificationWebServiceSchema.xsd"
generateDS --no-namespace-defs -o "${LIB_MODULES}/quantum_view_request.py" "${SCHEMAS}/QuantumViewRequest.xsd"
generateDS --no-namespace-defs -o "${LIB_MODULES}/quantum_view_response.py" "${SCHEMAS}/QuantumViewResponse.xsd"
generateDS --no-namespace-defs -o "${LIB_MODULES}/rate_web_service_schema.py" "${SCHEMAS}/RateWebServiceSchema.xsd"
generateDS --no-namespace-defs -o "${LIB_MODULES}/ship_web_service_schema.py" "${SCHEMAS}/ShipWebServiceSchema.xsd"
generateDS --no-namespace-defs -o "${LIB_MODULES}/time_in_transit_web_service_schema.py" "${SCHEMAS}/TimeInTransitWebServiceSchema.xsd"
generateDS --no-namespace-defs -o "${LIB_MODULES}/track_web_service_schema.py" "${SCHEMAS}/TrackWebServiceSchema.xsd"
generateDS --no-namespace-defs -o "${LIB_MODULES}/ups_security.py" "${SCHEMAS}/UPSSecurity.xsd"
generateDS --no-namespace-defs -o "${LIB_MODULES}/void_web_service_schema.py" "${SCHEMAS}/VoidWebServiceSchema.xsd"
generateDS --no-namespace-defs -o "${LIB_MODULES}/common.py" "${SCHEMAS}/common.xsd"


quicktype --src="${SCHEMAS}/rest_tracking_response.json" --out="${LIB_MODULES}/rest_tracking_response.py"
quicktype --src="${SCHEMAS}/rest_error.json" --out="${LIB_MODULES}/rest_error.py"
