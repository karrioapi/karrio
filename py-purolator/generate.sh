SCHEMAS=./schemas
find ./pypurolator -name "*.py" -exec rm -r {} \;
touch ./pypurolator/__init__.py

generateDS --no-namespace-defs -o "./pypurolator/array_ofstring.py" $SCHEMAS/ArrayOfstring.xsd
generateDS --no-namespace-defs -o "./pypurolator/data_types.py" $SCHEMAS/DataTypes.xsd
generateDS --no-namespace-defs -o "./pypurolator/estimate_service_2_1_2.py" $SCHEMAS/EstimateService_2_1_2.xsd
generateDS --no-namespace-defs -o "./pypurolator/freight_data_types.py" $SCHEMAS/FreightDataTypes.xsd
generateDS --no-namespace-defs -o "./pypurolator/freight_estimate_service_1_1_0.py" $SCHEMAS/FreightEstimateService_1_1_0.xsd
generateDS --no-namespace-defs -o "./pypurolator/freight_pickup_service_1_1_0.py" $SCHEMAS/FreightPickupService_1_1_0.xsd
generateDS --no-namespace-defs -o "./pypurolator/freight_shipment_service_1_1_0.py" $SCHEMAS/FreightShipmentService_1_1_0.xsd
generateDS --no-namespace-defs -o "./pypurolator/freight_tracking_service_1_1_0.py" $SCHEMAS/FreightTrackingService_1_1_0.xsd
generateDS --no-namespace-defs -o "./pypurolator/freight_validation_detail.py" $SCHEMAS/FreightValidationDetail.xsd
generateDS --no-namespace-defs -o "./pypurolator/freight_validation_fault.py" $SCHEMAS/FreightValidationFault.xsd
generateDS --no-namespace-defs -o "./pypurolator/locator_service_1_0_2.py" $SCHEMAS/LocatorService_1_0_2.xsd
generateDS --no-namespace-defs -o "./pypurolator/pickup_service_1_2_1.py" $SCHEMAS/PickupService_1_2_1.xsd
generateDS --no-namespace-defs -o "./pypurolator/returns_management_service_2_0.py" $SCHEMAS/ReturnsManagementService_2_0.xsd
generateDS --no-namespace-defs -o "./pypurolator/service_availability_service_2_0_2.py" $SCHEMAS/ServiceAvailabilityService_2_0_2.xsd
generateDS --no-namespace-defs -o "./pypurolator/shipping_documents_service_1_3_0.py" $SCHEMAS/ShippingDocumentsService_1_3_0.xsd
generateDS --no-namespace-defs -o "./pypurolator/shipping_service_2_1_3.py" $SCHEMAS/ShippingService_2_1_3.xsd
generateDS --no-namespace-defs -o "./pypurolator/tracking_service_1_2_2.py" $SCHEMAS/TrackingService_1_2_2.xsd
generateDS --no-namespace-defs -o "./pypurolator/validation_detail.py" $SCHEMAS/ValidationDetail.xsd
generateDS --no-namespace-defs -o "./pypurolator/validation_fault.py" $SCHEMAS/ValidationFault.xsd