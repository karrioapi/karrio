SCHEMAS=./schemas
LIB_MODULES=./tnt_lib
find "${LIB_MODULES}" -name "*.py" -exec rm -r {} \;
touch "${LIB_MODULES}/__init__.py"

generateDS --no-namespace-defs -o "${LIB_MODULES}/label_common_definitions.py" $SCHEMAS/label_common_definitions.xsd
generateDS --no-namespace-defs -o "${LIB_MODULES}/label_request.py" $SCHEMAS/label_request.xsd
generateDS --no-namespace-defs -o "${LIB_MODULES}/label_response.py" $SCHEMAS/label_response.xsd
generateDS --no-namespace-defs -o "${LIB_MODULES}/pricing_common_definitions.py" $SCHEMAS/pricing_common_definitions.xsd
generateDS --no-namespace-defs -o "${LIB_MODULES}/pricing_request.py" $SCHEMAS/pricing_request.xsd
generateDS --no-namespace-defs -o "${LIB_MODULES}/pricing_response.py" $SCHEMAS/pricing_response.xsd
generateDS --no-namespace-defs -o "${LIB_MODULES}/shipment_common_definitions.py" $SCHEMAS/shipment_common_definitions.xsd
generateDS --no-namespace-defs -o "${LIB_MODULES}/shipment_request.py" $SCHEMAS/shipment_request.xsd
generateDS --no-namespace-defs -o "${LIB_MODULES}/shipment_response.py" $SCHEMAS/shipment_response.xsd
generateDS --no-namespace-defs -o "${LIB_MODULES}/track_request_v3_1.py" $SCHEMAS/track_request_v3_1.xsd
generateDS --no-namespace-defs -o "${LIB_MODULES}/track_response_v3_1.py" $SCHEMAS/track_response_v3_1.xsd