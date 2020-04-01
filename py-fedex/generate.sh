SCHEMAS=$1
find ./pyfedex -name "*.py" -exec rm -r {} \;
touch ./pyfedex/__init__.py

generateDS --no-namespace-defs -o "./pyfedex/async_service_v4.py" $SCHEMAS/ASYNCService_v4.xsd
generateDS --no-namespace-defs -o "./pyfedex/address_validation_service_v4.py" $SCHEMAS/AddressValidationService_v4.xsd
generateDS --no-namespace-defs -o "./pyfedex/close_service_v5.py" $SCHEMAS/CloseService_v5.xsd
generateDS --no-namespace-defs -o "./pyfedex/country_service_v8.py" $SCHEMAS/CountryService_v8.xsd
generateDS --no-namespace-defs -o "./pyfedex/dgds_service_v5.py" $SCHEMAS/DGDSService_v5.xsd
generateDS --no-namespace-defs -o "./pyfedex/dgld_service_v1.py" $SCHEMAS/DGLDService_v1.xsd
generateDS --no-namespace-defs -o "./pyfedex/in_flight_shipment_service_v1.py" $SCHEMAS/InFlightShipmentService_v1.xsd
generateDS --no-namespace-defs -o "./pyfedex/location_service_v11.py" $SCHEMAS/LocationService_v11.xsd
generateDS --no-namespace-defs -o "./pyfedex/openship_service_v17.py" $SCHEMAS/OpenshipService_v17.xsd
generateDS --no-namespace-defs -o "./pyfedex/pickup_service_v20.py" $SCHEMAS/PickupService_v20.xsd
generateDS --no-namespace-defs -o "./pyfedex/rate_service_v26.py" $SCHEMAS/RateService_v26.xsd
generateDS --no-namespace-defs -o "./pyfedex/ship_service_v25.py" $SCHEMAS/ShipService_v25.xsd
generateDS --no-namespace-defs -o "./pyfedex/track_service_v18.py" $SCHEMAS/TrackService_v18.xsd
generateDS --no-namespace-defs -o "./pyfedex/upload_document_service_v11.py" $SCHEMAS/UploadDocumentService_v11.xsd
generateDS --no-namespace-defs -o "./pyfedex/validation_availability_and_commitment_service_v13.py" $SCHEMAS/ValidationAvailabilityAndCommitmentService_v13.xsd