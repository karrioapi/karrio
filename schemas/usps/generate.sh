SCHEMAS=./schemas
DATA_TYPES=./usps_lib
mkdir -p $DATA_TYPES
find $DATA_TYPES -name "*.py" -exec rm -r {} \;
touch $DATA_TYPES/__init__.py

generateDS --no-namespace-defs -o "$DATA_TYPES/address_validate_request.py" $SCHEMAS/AddressValidateRequest.xsd
generateDS --no-namespace-defs -o "$DATA_TYPES/address_validate_response.py" $SCHEMAS/AddressValidateResponse.xsd
generateDS --no-namespace-defs -o "$DATA_TYPES/carrier_pickup_availability_request.py" $SCHEMAS/CarrierPickupAvailabilityRequest.xsd
generateDS --no-namespace-defs -o "$DATA_TYPES/carrier_pickup_availability_response.py" $SCHEMAS/CarrierPickupAvailabilityResponse.xsd
generateDS --no-namespace-defs -o "$DATA_TYPES/carrier_pickup_cancel_request.py" $SCHEMAS/CarrierPickupCancelRequest.xsd
generateDS --no-namespace-defs -o "$DATA_TYPES/carrier_pickup_cancel_response.py" $SCHEMAS/CarrierPickupCancelResponse.xsd
generateDS --no-namespace-defs -o "$DATA_TYPES/carrier_pickup_change_request.py" $SCHEMAS/CarrierPickupChangeRequest.xsd
generateDS --no-namespace-defs -o "$DATA_TYPES/carrier_pickup_change_response.py" $SCHEMAS/CarrierPickupChangeResponse.xsd
generateDS --no-namespace-defs -o "$DATA_TYPES/carrier_pickup_inquiry_request.py" $SCHEMAS/CarrierPickupInquiryRequest.xsd
generateDS --no-namespace-defs -o "$DATA_TYPES/carrier_pickup_inquiry_response.py" $SCHEMAS/CarrierPickupInquiryResponse.xsd
generateDS --no-namespace-defs -o "$DATA_TYPES/carrier_pickup_schedule_request.py" $SCHEMAS/CarrierPickupScheduleRequest.xsd
generateDS --no-namespace-defs -o "$DATA_TYPES/carrier_pickup_schedule_response.py" $SCHEMAS/CarrierPickupScheduleResponse.xsd
generateDS --no-namespace-defs -o "$DATA_TYPES/city_state_lookup_request.py" $SCHEMAS/CityStateLookupRequest.xsd
generateDS --no-namespace-defs -o "$DATA_TYPES/city_state_lookup_response.py" $SCHEMAS/CityStateLookupResponse.xsd
generateDS --no-namespace-defs -o "$DATA_TYPES/emrsv4_0_bulk_request.py" $SCHEMAS/EMRSV4.0BulkRequest.xsd
generateDS --no-namespace-defs -o "$DATA_TYPES/error.py" $SCHEMAS/Error.xsd
generateDS --no-namespace-defs -o "$DATA_TYPES/express_mail_commitment_request.py" $SCHEMAS/ExpressMailCommitmentRequest.xsd
generateDS --no-namespace-defs -o "$DATA_TYPES/express_mail_commitment_response.py" $SCHEMAS/ExpressMailCommitmentResponse.xsd
generateDS --no-namespace-defs -o "$DATA_TYPES/first_class_mail_request.py" $SCHEMAS/FirstClassMailRequest.xsd
generateDS --no-namespace-defs -o "$DATA_TYPES/first_class_mail_response.py" $SCHEMAS/FirstClassMailResponse.xsd
generateDS --no-namespace-defs -o "$DATA_TYPES/hfp_facility_info_request.py" $SCHEMAS/HFPFacilityInfoRequest.xsd
generateDS --no-namespace-defs -o "$DATA_TYPES/hfp_facility_info_response.py" $SCHEMAS/HFPFacilityInfoResponse.xsd
generateDS --no-namespace-defs -o "$DATA_TYPES/intl_rate_v2_request.py" $SCHEMAS/IntlRateV2Request.xsd
generateDS --no-namespace-defs -o "$DATA_TYPES/intl_rate_v2_response.py" $SCHEMAS/IntlRateV2Response.xsd
generateDS --no-namespace-defs -o "$DATA_TYPES/mrsv4_0_request.py" $SCHEMAS/MRSV4.0Request.xsd
generateDS --no-namespace-defs -o "$DATA_TYPES/pts_emailresult.py" $SCHEMAS/PTSEmailResult.xsd
generateDS --no-namespace-defs -o "$DATA_TYPES/pts_email_request.py" $SCHEMAS/PTSEmailRequest.xsd
generateDS --no-namespace-defs -o "$DATA_TYPES/ptspod_result.py" $SCHEMAS/PTSPODResult.xsd
generateDS --no-namespace-defs -o "$DATA_TYPES/ptspod_request.py" $SCHEMAS/PTSPodRequest.xsd
generateDS --no-namespace-defs -o "$DATA_TYPES/ptsrre_result.py" $SCHEMAS/PTSRREResult.xsd
generateDS --no-namespace-defs -o "$DATA_TYPES/ptsrre_request.py" $SCHEMAS/PTSRreRequest.xsd
generateDS --no-namespace-defs -o "$DATA_TYPES/ptstpod_result.py" $SCHEMAS/PTSTPODResult.xsd
generateDS --no-namespace-defs -o "$DATA_TYPES/ptstpod_request.py" $SCHEMAS/PTSTPodRequest.xsd
generateDS --no-namespace-defs -o "$DATA_TYPES/priority_mail_request.py" $SCHEMAS/PriorityMailRequest.xsd
generateDS --no-namespace-defs -o "$DATA_TYPES/priority_mail_response.py" $SCHEMAS/PriorityMailResponse.xsd
generateDS --no-namespace-defs -o "$DATA_TYPES/rate_v4_request.py" $SCHEMAS/RateV4Request.xsd
generateDS --no-namespace-defs -o "$DATA_TYPES/rate_v4_response.py" $SCHEMAS/RateV4Response.xsd
generateDS --no-namespace-defs -o "$DATA_TYPES/scan_request.py" $SCHEMAS/SCANRequest.xsd
generateDS --no-namespace-defs -o "$DATA_TYPES/scan_response.py" $SCHEMAS/SCANResponse.xsd
generateDS --no-namespace-defs -o "$DATA_TYPES/sdc_get_locations_request.py" $SCHEMAS/SDCGetLocationsRequest.xsd
generateDS --no-namespace-defs -o "$DATA_TYPES/sdc_get_locations_response.py" $SCHEMAS/SDCGetLocationsResponse.xsd
generateDS --no-namespace-defs -o "$DATA_TYPES/standard_b_request.py" $SCHEMAS/StandardBRequest.xsd
generateDS --no-namespace-defs -o "$DATA_TYPES/standard_b_response.py" $SCHEMAS/StandardBResponse.xsd
generateDS --no-namespace-defs -o "$DATA_TYPES/track_field_request.py" $SCHEMAS/TrackFieldRequest.xsd
generateDS --no-namespace-defs -o "$DATA_TYPES/track_request.py" $SCHEMAS/TrackRequest.xsd
generateDS --no-namespace-defs -o "$DATA_TYPES/track_response.py" $SCHEMAS/TrackResponse.xsd
generateDS --no-namespace-defs -o "$DATA_TYPES/zip_code_lookup_request.py" $SCHEMAS/ZipCodeLookupRequest.xsd
generateDS --no-namespace-defs -o "$DATA_TYPES/zip_code_lookup_response.py" $SCHEMAS/ZipCodeLookupResponse.xsd
generateDS --no-namespace-defs -o "$DATA_TYPES/evs_cancel_request.py" $SCHEMAS/eVSCancelRequest.xsd
generateDS --no-namespace-defs -o "$DATA_TYPES/evs_cancel_response.py" $SCHEMAS/eVSCancelResponse.xsd
generateDS --no-namespace-defs -o "$DATA_TYPES/evs_request.py" $SCHEMAS/eVSRequest.xsd
generateDS --no-namespace-defs -o "$DATA_TYPES/evs_response.py" $SCHEMAS/eVSResponse.xsd
generateDS --no-namespace-defs -o "$DATA_TYPES/evs_express_mail_intl_request.py" $SCHEMAS/eVSExpressMailIntlRequest.xsd
generateDS --no-namespace-defs -o "$DATA_TYPES/evs_express_mail_intl_response.py" $SCHEMAS/eVSExpressMailIntlResponse.xsd
generateDS --no-namespace-defs -o "$DATA_TYPES/evs_first_class_mail_intl_request.py" $SCHEMAS/eVSFirstClassMailIntlRequest.xsd
generateDS --no-namespace-defs -o "$DATA_TYPES/evs_first_class_mail_intl_response.py" $SCHEMAS/eVSFirstClassMailIntlResponse.xsd
generateDS --no-namespace-defs -o "$DATA_TYPES/evs_gxg_get_label_request.py" $SCHEMAS/eVSGXGGetLabelRequest.xsd
generateDS --no-namespace-defs -o "$DATA_TYPES/evs_gxg_get_label_response.py" $SCHEMAS/eVSGXGGetLabelResponse.xsd
generateDS --no-namespace-defs -o "$DATA_TYPES/evsi_cancel_request.py" $SCHEMAS/eVSICancelRequest.xsd
generateDS --no-namespace-defs -o "$DATA_TYPES/evsi_cancel_response.py" $SCHEMAS/eVSICancelResponse.xsd
generateDS --no-namespace-defs -o "$DATA_TYPES/evs_priority_mail_intl_request.py" $SCHEMAS/eVSPriorityMailIntlRequest.xsd
generateDS --no-namespace-defs -o "$DATA_TYPES/evs_priority_mail_intl_response.py" $SCHEMAS/eVSPriorityMailIntlResponse.xsd
