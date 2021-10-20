SCHEMAS=$1
find ./pyups -name "*.py" -exec rm -r {} \;
touch ./pyups/__init__.py

generateDS --no-namespace-defs -o "./pyups/av_request.py" $SCHEMAS/AVRequest.xsd
generateDS --no-namespace-defs -o "./pyups/av_response.py" $SCHEMAS/AVResponse.xsd
generateDS --no-namespace-defs -o "./pyups/access_request.py" $SCHEMAS/AccessRequest.xsd
generateDS --no-namespace-defs -o "./pyups/access_request_xpci.py" $SCHEMAS/AccessRequestXPCI.xsd
generateDS --no-namespace-defs -o "./pyups/dangerous_goods_utility.py" $SCHEMAS/DangerousGoodsUtility.xsd
generateDS --no-namespace-defs -o "./pyups/denied_party_web_service_schema.py" $SCHEMAS/DeniedPartyWebServiceSchema.xsd
generateDS --no-namespace-defs -o "./pyups/error_1_1.py" $SCHEMAS/Error1.1.xsd
generateDS --no-namespace-defs -o "./pyups/error_xpci.py" $SCHEMAS/ErrorXPCI.xsd
generateDS --no-namespace-defs -o "./pyups/freight_pickup_web_service_schema.py" $SCHEMAS/FreightPickupWebServiceSchema.xsd
generateDS --no-namespace-defs -o "./pyups/freight_rate_web_service_schema.py" $SCHEMAS/FreightRateWebServiceSchema.xsd
generateDS --no-namespace-defs -o "./pyups/freight_ship_web_service_schema.py" $SCHEMAS/FreightShipWebServiceSchema.xsd
generateDS --no-namespace-defs -o "./pyups/ifws.py" $SCHEMAS/IFWS.xsd
generateDS --no-namespace-defs -o "./pyups/lb_recovery.py" $SCHEMAS/LBRecovery.xsd
generateDS --no-namespace-defs -o "./pyups/landed_cost_web_service_schema.py" $SCHEMAS/LandedCostWebServiceSchema.xsd
generateDS --no-namespace-defs -o "./pyups/locator_request.py" $SCHEMAS/LocatorRequest.xsd
generateDS --no-namespace-defs -o "./pyups/locator_response.py" $SCHEMAS/LocatorResponse.xsd
generateDS --no-namespace-defs -o "./pyups/paperless_document_api.py" $SCHEMAS/PaperlessDocumentAPI.xsd
generateDS --no-namespace-defs -o "./pyups/pickup_web_service_schema.py" $SCHEMAS/PickupWebServiceSchema.xsd
generateDS --no-namespace-defs -o "./pyups/pre_notification_web_service_schema.py" $SCHEMAS/PreNotificationWebServiceSchema.xsd
generateDS --no-namespace-defs -o "./pyups/quantum_view_request.py" $SCHEMAS/QuantumViewRequest.xsd
generateDS --no-namespace-defs -o "./pyups/quantum_view_response.py" $SCHEMAS/QuantumViewResponse.xsd
generateDS --no-namespace-defs -o "./pyups/rate_web_service_schema.py" $SCHEMAS/RateWebServiceSchema.xsd
generateDS --no-namespace-defs -o "./pyups/ship_web_service_schema.py" $SCHEMAS/ShipWebServiceSchema.xsd
generateDS --no-namespace-defs -o "./pyups/time_in_transit_web_service_schema.py" $SCHEMAS/TimeInTransitWebServiceSchema.xsd
generateDS --no-namespace-defs -o "./pyups/track_web_service_schema.py" $SCHEMAS/TrackWebServiceSchema.xsd
generateDS --no-namespace-defs -o "./pyups/ups_security.py" $SCHEMAS/UPSSecurity.xsd
generateDS --no-namespace-defs -o "./pyups/void_web_service_schema.py" $SCHEMAS/VoidWebServiceSchema.xsd
generateDS --no-namespace-defs -o "./pyups/common.py" $SCHEMAS/common.xsd
