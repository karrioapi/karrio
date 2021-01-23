# References

## Standard Formats

| Type | Format
| --- | ---
| `time - str` | `HH:MM`
| `date - str` | `YYYY-MM-DD`
| `datetime - str` | `YYYY-MM-DD HH:MM`

## Gateway

#### USPS Settings

| Name | Type | Description 
| --- | --- | --- |
| `username` | `str` | **required**
| `password` | `str` | **required**
| `id` | `str` | 
| `test` | `bool` | 
| `carrier_id` | `str` | 


#### UPS Package Settings

| Name | Type | Description 
| --- | --- | --- |
| `username` | `str` | **required**
| `password` | `str` | **required**
| `access_license_number` | `str` | **required**
| `account_number` | `str` | 
| `id` | `str` | 
| `test` | `bool` | 
| `carrier_id` | `str` | 


#### Purolator Courier Settings

| Name | Type | Description 
| --- | --- | --- |
| `username` | `str` | **required**
| `password` | `str` | **required**
| `account_number` | `str` | **required**
| `user_token` | `str` | 
| `language` | `str` | 
| `id` | `str` | 
| `test` | `bool` | 
| `carrier_id` | `str` | 


#### FedEx Express Settings

| Name | Type | Description 
| --- | --- | --- |
| `user_key` | `str` | **required**
| `password` | `str` | **required**
| `meter_number` | `str` | **required**
| `account_number` | `str` | **required**
| `id` | `str` | 
| `test` | `bool` | 
| `carrier_id` | `str` | 


#### Dicom Settings

| Name | Type | Description 
| --- | --- | --- |
| `username` | `str` | **required**
| `password` | `str` | **required**
| `billing_account` | `str` | 
| `id` | `str` | 
| `test` | `bool` | 
| `carrier_id` | `str` | 


#### Canada Post Settings

| Name | Type | Description 
| --- | --- | --- |
| `username` | `str` | **required**
| `password` | `str` | **required**
| `customer_number` | `str` | **required**
| `contract_id` | `str` | 
| `language` | `str` | 
| `id` | `str` | 
| `test` | `bool` | 
| `carrier_id` | `str` | 


#### Canpar Settings

| Name | Type | Description 
| --- | --- | --- |
| `username` | `str` | **required**
| `password` | `str` | **required**
| `id` | `str` | 
| `test` | `bool` | 
| `carrier_id` | `str` | 


#### BoxKnight Settings

| Name | Type | Description 
| --- | --- | --- |
| `username` | `str` | **required**
| `password` | `str` | **required**
| `id` | `str` | 
| `test` | `bool` | 
| `carrier_id` | `str` | 


*Note that all carrier gateway defined bellow have these additional parameters*

| Name | Type | Description
| --- | --- | --- |
| `carrier_name` | `str` | default: carrier name (eg: canadapost, purolator...)
| `id` | `str` | 
| `test` | `boolean` |


## Models

### Carrier models

#### Address

| Name | Type | Description 
| --- | --- | --- |
| `id` | `str` | 
| `postal_code` | `str` | 
| `city` | `str` | 
| `person_name` | `str` | 
| `company_name` | `str` | 
| `country_code` | `str` | 
| `email` | `str` | 
| `phone_number` | `str` | 
| `state_code` | `str` | 
| `suburb` | `str` | 
| `residential` | `bool` | 
| `address_line1` | `str` | 
| `address_line2` | `str` | 
| `federal_tax_id` | `str` | 
| `state_tax_id` | `str` | 


#### AddressValidationDetails

| Name | Type | Description 
| --- | --- | --- |
| `carrier_name` | `str` | **required**
| `carrier_id` | `str` | **required**
| `success` | `bool` | **required**
| `complete_address` | [Address](#Address) | 


#### AddressValidationRequest

| Name | Type | Description 
| --- | --- | --- |
| `address` | [Address](#Address) | **required**


#### ChargeDetails

| Name | Type | Description 
| --- | --- | --- |
| `name` | `str` | 
| `amount` | `float` | 
| `currency` | `str` | 


#### Commodity

| Name | Type | Description 
| --- | --- | --- |
| `id` | `str` | 
| `weight` | `float` | 
| `weight_unit` | `str` | 
| `description` | `str` | 
| `quantity` | `int` | 
| `sku` | `str` | 
| `value_amount` | `float` | 
| `value_currency` | `str` | 
| `origin_country` | `str` | 


#### ConfirmationDetails

| Name | Type | Description 
| --- | --- | --- |
| `carrier_name` | `str` | **required**
| `carrier_id` | `str` | **required**
| `success` | `bool` | **required**
| `operation` | `str` | **required**


#### Customs

| Name | Type | Description 
| --- | --- | --- |
| `aes` | `str` | 
| `eel_pfc` | `str` | 
| `certify` | `bool` | 
| `signer` | `str` | 
| `content_type` | `str` | 
| `content_description` | `str` | 
| `incoterm` | `str` | 
| `invoice` | `str` | 
| `certificate_number` | `str` | 
| `commodities` | List[[Commodity](#Commodity)] | 
| `duty` | [Payment](#Payment) | 
| `commercial_invoice` | `bool` | 
| `options` | `dict` | 
| `id` | `str` | 


#### Message

| Name | Type | Description 
| --- | --- | --- |
| `carrier_name` | `str` | **required**
| `carrier_id` | `str` | **required**
| `message` | Union[str, Any] | 
| `code` | `str` | 
| `details` | `dict` | 


#### Parcel

| Name | Type | Description 
| --- | --- | --- |
| `id` | `str` | 
| `weight` | `float` | 
| `width` | `float` | 
| `height` | `float` | 
| `length` | `float` | 
| `packaging_type` | `str` | 
| `package_preset` | `str` | 
| `description` | `str` | 
| `content` | `str` | 
| `is_document` | `bool` | 
| `weight_unit` | `str` | 
| `dimension_unit` | `str` | 


#### Payment

| Name | Type | Description 
| --- | --- | --- |
| `paid_by` | `str` | 
| `amount` | `float` | 
| `currency` | `str` | 
| `account_number` | `str` | 
| `contact` | [Address](#Address) | 
| `id` | `str` | 


#### PickupCancelRequest

| Name | Type | Description 
| --- | --- | --- |
| `confirmation_number` | `str` | **required**
| `address` | [Address](#Address) | 
| `pickup_date` | `str` | 
| `reason` | `str` | 


#### PickupDetails

| Name | Type | Description 
| --- | --- | --- |
| `carrier_name` | `str` | **required**
| `carrier_id` | `str` | **required**
| `confirmation_number` | `str` | **required**
| `pickup_date` | `str` | 
| `pickup_charge` | [ChargeDetails](#ChargeDetails) | 
| `ready_time` | `str` | 
| `closing_time` | `str` | 
| `id` | `str` | 


#### PickupRequest

| Name | Type | Description 
| --- | --- | --- |
| `pickup_date` | `str` | **required**
| `ready_time` | `str` | **required**
| `closing_time` | `str` | **required**
| `address` | [Address](#Address) | **required**
| `parcels` | List[[Parcel](#Parcel)] | 
| `instruction` | `str` | 
| `package_location` | `str` | 
| `options` | `dict` | 


#### PickupUpdateRequest

| Name | Type | Description 
| --- | --- | --- |
| `confirmation_number` | `str` | **required**
| `pickup_date` | `str` | **required**
| `ready_time` | `str` | **required**
| `closing_time` | `str` | **required**
| `address` | [Address](#Address) | **required**
| `parcels` | List[[Parcel](#Parcel)] | 
| `instruction` | `str` | 
| `package_location` | `str` | 
| `options` | `dict` | 


#### RateDetails

| Name | Type | Description 
| --- | --- | --- |
| `carrier_name` | `str` | **required**
| `carrier_id` | `str` | **required**
| `currency` | `str` | **required**
| `transit_days` | `int` | 
| `service` | `str` | 
| `discount` | `float` | 
| `base_charge` | `float` | 
| `total_charge` | `float` | 
| `duties_and_taxes` | `float` | 
| `extra_charges` | List[[ChargeDetails](#ChargeDetails)] | 
| `meta` | `dict` | 
| `id` | `str` | 


#### RateRequest

| Name | Type | Description 
| --- | --- | --- |
| `shipper` | [Address](#Address) | **required**
| `recipient` | [Address](#Address) | **required**
| `parcels` | List[[Parcel](#Parcel)] | **required**
| `services` | List[str] | 
| `options` | `dict` | 
| `reference` | `str` | 


#### ShipmentCancelRequest

| Name | Type | Description 
| --- | --- | --- |
| `shipment_identifier` | `str` | **required**
| `service` | `str` | 
| `options` | `dict` | 


#### ShipmentDetails

| Name | Type | Description 
| --- | --- | --- |
| `carrier_name` | `str` | **required**
| `carrier_id` | `str` | **required**
| `label` | `str` | **required**
| `tracking_number` | `str` | **required**
| `shipment_identifier` | `str` | **required**
| `selected_rate` | [RateDetails](#RateDetails) | 
| `meta` | `dict` | 
| `id` | `str` | 


#### ShipmentRequest

| Name | Type | Description 
| --- | --- | --- |
| `service` | `str` | **required**
| `shipper` | [Address](#Address) | **required**
| `recipient` | [Address](#Address) | **required**
| `parcels` | List[[Parcel](#Parcel)] | **required**
| `payment` | [Payment](#Payment) | 
| `customs` | [Customs](#Customs) | 
| `options` | `dict` | 
| `reference` | `str` | 
| `label_type` | `str` | 


#### TrackingDetails

| Name | Type | Description 
| --- | --- | --- |
| `carrier_name` | `str` | **required**
| `carrier_id` | `str` | **required**
| `tracking_number` | `str` | **required**
| `events` | List[[TrackingEvent](#TrackingEvent)] | **required**
| `delivered` | `bool` | 


#### TrackingEvent

| Name | Type | Description 
| --- | --- | --- |
| `date` | `str` | **required**
| `description` | `str` | **required**
| `location` | `str` | 
| `code` | `str` | 
| `time` | `str` | 
| `signatory` | `str` | 


#### TrackingRequest

| Name | Type | Description 
| --- | --- | --- |
| `tracking_numbers` | List[str] | **required**
| `language_code` | `str` | 
| `level_of_details` | `str` | 




## Packaging Types


#### Multi-carrier (purplship)

| Code | Identifier
--- | ---
| `envelope` | Small Envelope
| `pak` | Pak
| `tube` | Tube
| `pallet` | Pallet
| `small_box` | Small Box
| `medium_box` | Medium Box
| `your_packaging` | Your Packaging


#### UPS Package

| Code | Identifier
--- | ---
| `ups_unknown` | 00
| `ups_letter` | 01
| `ups_package` | 02
| `ups_tube` | 03
| `ups_pak` | 04
| `ups_express_box` | 21
| `ups_box_25_kg` | 24
| `ups_box_10_kg` | 25
| `ups_pallet` | 30
| `ups_small_express_box` | 2a
| `ups_medium_express_box` | 2b
| `ups_large_express_box` | 2c


#### Purolator Courier

| Code | Identifier
--- | ---
| `purolator_express_envelope` | Envelope
| `purolator_express_pack` | Pack
| `purolator_express_box` | Box
| `purolator_customer_packaging` | Customer Packaging


#### FedEx Express

| Code | Identifier
--- | ---
| `fedex_envelope` | FEDEX_ENVELOPE
| `fedex_pak` | FEDEX_PAK
| `fedex_box` | FEDEX_BOX
| `fedex_10_kg_box` | FEDEX_10KG_BOX
| `fedex_25_kg_box` | FEDEX_25KG_BOX
| `fedex_tube` | FEDEX_TUBE
| `your_packaging` | YOUR_PACKAGING


#### DHL Express

| Code | Identifier
--- | ---
| `dhl_flyer_smalls` | FLY
| `dhl_parcels_conveyables` | COY
| `dhl_non_conveyables` | NCY
| `dhl_pallets` | PAL
| `dhl_double_pallets` | DBL
| `dhl_box` | BOX




## Package Presets


#### UPS Package

| Code | Dimensions | Note
--- | --- | ---
| `ups_small_express_box` | 11.0 x 2.0 x 30.0 x 13.0 | height x length x weight x width
| `ups_medium_express_box` | 11.0 x 3.0 x 30.0 x 16.0 | height x length x weight x width
| `ups_large_express_box` | 13.0 x 3.0 x 30.0 x 18.0 | height x length x weight x width
| `ups_express_tube` | 6.0 x 6.0 x 38.0 | height x length x width
| `ups_express_pak` | 11.75 x 1.5 x 16.0 | height x length x width
| `ups_world_document_box` | 12.5 x 3.0 x 17.5 | height x length x width


#### Purolator Courier

| Code | Dimensions | Note
--- | --- | ---
| `purolator_express_envelope` | 1.5 x 1.0 x 12.5 | length x weight x width
| `purolator_express_pack` | 1.0 x 3.0 x 12.5 | length x weight x width
| `purolator_express_box` | 3.5 x 7.0 | length x weight


#### FedEx Express
| Code | Dimensions | Note
--- | --- | ---
| `fedex_envelope_legal_size` | 15.5 x 1.0 x 9.5 | height x weight x width
| `fedex_padded_pak` | 14.75 x 2.2 x 11.75 | height x weight x width
| `fedex_polyethylene_pak` | 15.5 x 2.2 x 12.0 | height x weight x width
| `fedex_clinical_pak` | 18.0 x 2.2 x 13.5 | height x weight x width
| `fedex_small_box` | 10.9 x 1.5 x 20.0 x 12.25 | height x length x weight x width
| `fedex_medium_box` | 11.5 x 2.38 x 20.0 x 13.25 | height x length x weight x width
| `fedex_large_box` | 12.38 x 3.0 x 20.0 x 17.88 | height x length x weight x width
| `fedex_10_kg_box` | 12.94 x 10.19 x 10.0 x 15.81 | height x length x weight x width
| `fedex_25_kg_box` | 16.56 x 13.19 x 25.0 x 21.56 | height x length x weight x width
| `fedex_tube` | 6.0 x 6.0 x 20.0 x 38.0 | height x length x weight x width


#### DHL Express

| Code | Dimensions | Note
--- | --- | ---
| `dhl_express_envelope` | 27.5 x 1.0 x 0.5 x 35.0 | height x length x weight x width
| `dhl_express_standard_flyer` | 30.0 x 1.5 x 2.0 x 40.0 | height x length x weight x width
| `dhl_express_large_flyer` | 37.5 x 1.5 x 3.0 x 47.5 | height x length x weight x width
| `dhl_express_box_2` | 18.2 x 10.0 x 1.0 x 33.7 | height x length x weight x width
| `dhl_express_box_3` | 32.0 x 5.2 x 2.0 x 33.6 | height x length x weight x width
| `dhl_express_box_4` | 32.2 x 18.0 x 5.0 x 33.7 | height x length x weight x width
| `dhl_express_box_5` | 32.2 x 34.5 x 10.0 x 33.7 | height x length x weight x width
| `dhl_express_box_6` | 35.9 x 36.9 x 15.0 x 41.7 | height x length x weight x width
| `dhl_express_box_7` | 40.4 x 38.9 x 20.0 x 48.1 | height x length x weight x width
| `dhl_express_box_8` | 44.4 x 40.9 x 25.0 x 54.2 | height x length x weight x width
| `dhl_express_tube` | 15.0 x 15.0 x 5.0 x 96.0 | height x length x weight x width
| `dhl_didgeridoo_box` | 13.0 x 162.0 x 10.0 x 13.0 | height x length x weight x width
| `dhl_jumbo_box` | 42.7 x 33.0 x 30.0 x 45.0 | height x length x weight x width
| `dhl_jumbo_box_junior` | 34.0 x 24.1 x 20.0 x 39.9 | height x length x weight x width


#### Canada Post

| Code | Dimensions | Note
--- | --- | ---
| `canadapost_mailing_box` | 15.2 x 1.0 x 10.2 | height x length x width
| `canadapost_extra_small_mailing_box` | 14.0 x 14.0 x 14.0 | height x length x width
| `canadapost_small_mailing_box` | 22.9 x 6.4 x 28.6 | height x length x width
| `canadapost_medium_mailing_box` | 23.5 x 13.3 x 31.0 | height x length x width
| `canadapost_large_mailing_box` | 30.5 x 9.5 x 38.1 | height x length x width
| `canadapost_extra_large_mailing_box` | 30.5 x 21.6 x 40.0 | height x length x width
| `canadapost_corrugated_small_box` | 32.0 x 32.0 x 42.0 | height x length x width
| `canadapost_corrugated_medium_box` | 38.0 x 32.0 x 46.0 | height x length x width
| `canadapost_corrugated_large_box` | 46.0 x 40.6 x 46.0 | height x length x width
| `canadapost_xexpresspost_certified_envelope` | 15.9 x 1.5 x 0.5 x 26.0 | height x length x weight x width
| `canadapost_xexpresspost_national_large_envelope` | 29.2 x 1.5 x 1.36 x 40.0 | height x length x weight x width




## Shipping Services


#### UPS Package

| Code | Identifier
--- | ---
| `ups_standard` | 11
| `ups_worldwide_expedited` | 08
| `ups_worldwide_express` | 07
| `ups_worldwide_express_plus` | 54
| `ups_worldwide_saver` | 65
| `ups_2nd_day_air` | 02
| `ups_2nd_day_air_am` | 59
| `ups_3_day_select` | 12
| `ups_expedited_mail_innovations` | M4
| `ups_first_class_mail` | M2
| `ups_ground` | 03
| `ups_next_day_air` | 01
| `ups_next_day_air_early` | 14
| `ups_next_day_air_saver` | 13
| `ups_priority_mail` | M3
| `ups_access_point_economy` | 70
| `ups_today_dedicated_courier` | 83
| `ups_today_express` | 85
| `ups_today_express_saver` | 86
| `ups_today_standard` | 82
| `ups_worldwide_express_freight` | 96
| `ups_priority_mail_innovations` | M5
| `ups_economy_mail_innovations` | M6


#### Purolator Courier

| Code | Identifier
--- | ---
| `purolator_express_9_am` | PurolatorExpress9AM
| `purolator_express_us` | PurolatorExpressU.S.
| `purolator_express_10_30_am` | PurolatorExpress10:30AM
| `purolator_express_us_9_am` | PurolatorExpressU.S.9AM
| `purolator_express_12_pm` | PurolatorExpress12PM
| `purolator_express_us_10_30_am` | PurolatorExpressU.S.10:30AM
| `purolator_express` | PurolatorExpress
| `purolator_express_us_12_00` | PurolatorExpressU.S.12:00
| `purolator_express_evening` | PurolatorExpressEvening
| `purolator_express_envelope_us` | PurolatorExpressEnvelopeU.S.
| `purolator_express_envelope_9_am` | PurolatorExpressEnvelope9AM
| `purolator_express_us_envelope_9_am` | PurolatorExpressU.S.Envelope9AM
| `purolator_express_envelope_10_30_am` | PurolatorExpressEnvelope10:30AM
| `purolator_express_us_envelope_10_30_am` | PurolatorExpressU.S.Envelope10:30AM
| `purolator_express_envelope_12_pm` | PurolatorExpressEnvelope12PM
| `purolator_express_us_envelope_12_00` | PurolatorExpressU.S.Envelope12:00
| `purolator_express_envelope` | PurolatorExpressEnvelope
| `purolator_express_pack_us` | PurolatorExpressPackU.S.
| `purolator_express_envelope_evening` | PurolatorExpressEnvelopeEvening
| `purolator_express_us_pack_9_am` | PurolatorExpressU.S.Pack9AM
| `purolator_express_pack_9_am` | PurolatorExpressPack9AM
| `purolator_express_us_pack_10_30_am` | PurolatorExpressU.S.Pack10:30AM
| `purolator_express_pack10_30_am` | PurolatorExpressPack10:30AM
| `purolator_express_us_pack_12_00` | PurolatorExpressU.S.Pack12:00
| `purolator_express_pack_12_pm` | PurolatorExpressPack12PM
| `purolator_express_box_us` | PurolatorExpressBoxU.S.
| `purolator_express_pack` | PurolatorExpressPack
| `purolator_express_us_box_9_am` | PurolatorExpressU.S.Box9AM
| `purolator_express_pack_evening` | PurolatorExpressPackEvening
| `purolator_express_us_box_10_30_am` | PurolatorExpressU.S.Box10:30AM
| `purolator_express_box_9_am` | PurolatorExpressBox9AM
| `purolator_express_us_box_12_00` | PurolatorExpressU.S.Box12:00
| `purolator_express_box_10_30_am` | PurolatorExpressBox10:30AM
| `purolator_ground_us` | PurolatorGroundU.S.
| `purolator_express_box_12_pm` | PurolatorExpressBox12PM
| `purolator_express_international` | PurolatorExpressInternational
| `purolator_express_box` | PurolatorExpressBox
| `purolator_express_international_9_am` | PurolatorExpressInternational9AM
| `purolator_express_box_evening` | PurolatorExpressBoxEvening
| `purolator_express_international_10_30_am` | PurolatorExpressInternational10:30AM
| `purolator_ground` | PurolatorGround
| `purolator_express_international_12_00` | PurolatorExpressInternational12:00
| `purolator_ground9_am` | PurolatorGround9AM
| `purolator_express_envelope_international` | PurolatorExpressEnvelopeInternational
| `purolator_ground10_30_am` | PurolatorGround10:30AM
| `purolator_express_international_envelope_9_am` | PurolatorExpressInternationalEnvelope9AM
| `purolator_ground_evening` | PurolatorGroundEvening
| `purolator_express_international_envelope_10_30_am` | PurolatorExpressInternationalEnvelope10:30AM
| `purolator_quick_ship` | PurolatorQuickShip
| `purolator_express_international_envelope_12_00` | PurolatorExpressInternationalEnvelope12:00
| `purolator_quick_ship_envelope` | PurolatorQuickShipEnvelope
| `purolator_express_pack_international` | PurolatorExpressPackInternational
| `purolator_quick_ship_pack` | PurolatorQuickShipPack
| `purolator_express_international_pack_9_am` | PurolatorExpressInternationalPack9AM
| `purolator_quick_ship_box` | PurolatorQuickShipBox
| `purolator_express_international_pack_10_30_am` | PurolatorExpressInternationalPack10:30AM
| `purolator_express_international_pack_12_00` | PurolatorExpressInternationalPack12:00
| `purolator_express_box_international` | PurolatorExpressBoxInternational
| `purolator_express_international_box_9_am` | PurolatorExpressInternationalBox9AM
| `purolator_express_international_box_10_30_am` | PurolatorExpressInternationalBox10:30AM
| `purolator_express_international_box_12_00` | PurolatorExpressInternationalBox12:00


#### FedEx Express

| Code | Identifier
--- | ---
| `fedex_europe_first_international_priority` | EUROPE_FIRST_INTERNATIONAL_PRIORITY
| `fedex_1_day_freight` | FEDEX_1_DAY_FREIGHT
| `fedex_2_day` | FEDEX_2_DAY
| `fedex_2_day_am` | FEDEX_2_DAY_AM
| `fedex_2_day_freight` | FEDEX_2_DAY_FREIGHT
| `fedex_3_day_freight` | FEDEX_3_DAY_FREIGHT
| `fedex_cargo_airport_to_airport` | FEDEX_CARGO_AIRPORT_TO_AIRPORT
| `fedex_cargo_freight_forwarding` | FEDEX_CARGO_FREIGHT_FORWARDING
| `fedex_cargo_international_express_freight` | FEDEX_CARGO_INTERNATIONAL_EXPRESS_FREIGHT
| `fedex_cargo_international_premium` | FEDEX_CARGO_INTERNATIONAL_PREMIUM
| `fedex_cargo_mail` | FEDEX_CARGO_MAIL
| `fedex_cargo_registered_mail` | FEDEX_CARGO_REGISTERED_MAIL
| `fedex_cargo_surface_mail` | FEDEX_CARGO_SURFACE_MAIL
| `fedex_custom_critical_air_expedite` | FEDEX_CUSTOM_CRITICAL_AIR_EXPEDITE
| `fedex_custom_critical_air_expedite_exclusive_use` | FEDEX_CUSTOM_CRITICAL_AIR_EXPEDITE_EXCLUSIVE_USE
| `fedex_custom_critical_air_expedite_network` | FEDEX_CUSTOM_CRITICAL_AIR_EXPEDITE_NETWORK
| `fedex_custom_critical_charter_air` | FEDEX_CUSTOM_CRITICAL_CHARTER_AIR
| `fedex_custom_critical_point_to_point` | FEDEX_CUSTOM_CRITICAL_POINT_TO_POINT
| `fedex_custom_critical_surface_expedite` | FEDEX_CUSTOM_CRITICAL_SURFACE_EXPEDITE
| `fedex_custom_critical_surface_expedite_exclusive_use` | FEDEX_CUSTOM_CRITICAL_SURFACE_EXPEDITE_EXCLUSIVE_USE
| `fedex_custom_critical_temp_assure_air` | FEDEX_CUSTOM_CRITICAL_TEMP_ASSURE_AIR
| `fedex_custom_critical_temp_assure_validated_air` | FEDEX_CUSTOM_CRITICAL_TEMP_ASSURE_VALIDATED_AIR
| `fedex_custom_critical_white_glove_services` | FEDEX_CUSTOM_CRITICAL_WHITE_GLOVE_SERVICES
| `fedex_distance_deferred` | FEDEX_DISTANCE_DEFERRED
| `fedex_express_saver` | FEDEX_EXPRESS_SAVER
| `fedex_first_freight` | FEDEX_FIRST_FREIGHT
| `fedex_freight_economy` | FEDEX_FREIGHT_ECONOMY
| `fedex_freight_priority` | FEDEX_FREIGHT_PRIORITY
| `fedex_ground` | FEDEX_GROUND
| `fedex_international_priority_plus` | FEDEX_INTERNATIONAL_PRIORITY_PLUS
| `fedex_next_day_afternoon` | FEDEX_NEXT_DAY_AFTERNOON
| `fedex_next_day_early_morning` | FEDEX_NEXT_DAY_EARLY_MORNING
| `fedex_next_day_end_of_day` | FEDEX_NEXT_DAY_END_OF_DAY
| `fedex_next_day_freight` | FEDEX_NEXT_DAY_FREIGHT
| `fedex_next_day_mid_morning` | FEDEX_NEXT_DAY_MID_MORNING
| `fedex_first_overnight` | FIRST_OVERNIGHT
| `fedex_ground_home_delivery` | GROUND_HOME_DELIVERY
| `fedex_international_distribution_freight` | INTERNATIONAL_DISTRIBUTION_FREIGHT
| `fedex_international_economy` | INTERNATIONAL_ECONOMY
| `fedex_international_economy_distribution` | INTERNATIONAL_ECONOMY_DISTRIBUTION
| `fedex_international_economy_freight` | INTERNATIONAL_ECONOMY_FREIGHT
| `fedex_international_first` | INTERNATIONAL_FIRST
| `fedex_international_ground` | INTERNATIONAL_GROUND
| `fedex_international_priority` | INTERNATIONAL_PRIORITY
| `fedex_international_priority_distribution` | INTERNATIONAL_PRIORITY_DISTRIBUTION
| `fedex_international_priority_express` | INTERNATIONAL_PRIORITY_EXPRESS
| `fedex_international_priority_freight` | INTERNATIONAL_PRIORITY_FREIGHT
| `fedex_priority_overnight` | PRIORITY_OVERNIGHT
| `fedex_same_day` | SAME_DAY
| `fedex_same_day_city` | SAME_DAY_CITY
| `fedex_same_day_metro_afternoon` | SAME_DAY_METRO_AFTERNOON
| `fedex_same_day_metro_morning` | SAME_DAY_METRO_MORNING
| `fedex_same_day_metro_rush` | SAME_DAY_METRO_RUSH
| `fedex_smart_post` | SMART_POST
| `fedex_standard_overnight` | STANDARD_OVERNIGHT
| `fedex_transborder_distribution_consolidation` | TRANSBORDER_DISTRIBUTION_CONSOLIDATION


#### DHL Express

| Code | Identifier
--- | ---
| `dhl_logistics_services` | LOGISTICS SERVICES
| `dhl_domestic_express_12_00_doc` | DOMESTIC EXPRESS 12:00 DOC
| `dhl_b2_c_doc` | B2C DOC
| `dhl_b2_c_nondoc` | B2C NONDOC
| `dhl_jetline` | JETLINE
| `dhl_sprintline` | SPRINTLINE
| `dhl_express_easy_doc` | EXPRESS EASY DOC
| `dhl_express_easy_nondoc` | EXPRESS EASY NONDOC
| `dhl_europack_doc` | EUROPACK DOC
| `dhl_auto_reversals` | AUTO REVERSALS
| `dhl_breakbulk_express_doc` | BREAKBULK EXPRESS DOC
| `dhl_medical_express_doc` | MEDICAL EXPRESS DOC
| `dhl_express_worldwide_doc` | EXPRESS WORLDWIDE DOC
| `dhl_express_9_00_nondoc` | EXPRESS 9:00 NONDOC
| `dhl_freight_worldwide_nondoc` | FREIGHT WORLDWIDE NONDOC
| `dhl_domestic_economy_select_doc` | DOMESTIC ECONOMY SELECT DOC
| `dhl_economy_select_nondoc` | ECONOMY SELECT NONDOC
| `dhl_domestic_express_9_00_doc` | DOMESTIC EXPRESS 9:00 DOC
| `dhl_jumbo_box_nondoc` | JUMBO BOX NONDOC
| `dhl_express_9_00_doc` | EXPRESS 9:00 DOC
| `dhl_express_10_30_doc` | EXPRESS 10:30 DOC
| `dhl_express_10_30_nondoc` | EXPRESS 10:30 NONDOC
| `dhl_domestic_express_doc` | DOMESTIC EXPRESS DOC
| `dhl_domestic_express_10_30_doc` | DOMESTIC EXPRESS 10:30 DOC
| `dhl_express_worldwide_nondoc` | EXPRESS WORLDWIDE NONDOC
| `dhl_medical_express_nondoc` | MEDICAL EXPRESS NONDOC
| `dhl_globalmail_business_doc` | GLOBALMAIL BUSINESS DOC
| `dhl_same_day_doc` | SAME DAY DOC
| `dhl_express_12_00_doc` | EXPRESS 12:00 DOC
| `dhl_europack_nondoc` | EUROPACK NONDOC
| `dhl_economy_select_doc` | ECONOMY SELECT DOC
| `dhl_express_envelope_doc` | EXPRESS ENVELOPE DOC
| `dhl_express_12_00_nondoc` | EXPRESS 12:00 NONDOC
| `dhl_destination_charges` | Destination Charges


#### Canada Post

| Code | Identifier
--- | ---
| `canadapost_regular_parcel` | DOM.RP
| `canadapost_expedited_parcel` | DOM.EP
| `canadapost_xpresspost` | DOM.XP
| `canadapost_priority` | DOM.PC
| `canadapost_library_books` | DOM.LIB
| `canadapost_expedited_parcel_usa` | USA.EP
| `canadapost_priority_worldwide_envelope_usa` | USA.PW.ENV
| `canadapost_priority_worldwide_pak_usa` | USA.PW.PAK
| `canadapost_priority_worldwide_parcel_usa` | USA.PW.PARCEL
| `canadapost_small_packet_usa_air` | USA.SP.AIR
| `canadapost_tracked_packet_usa` | USA.TP
| `canadapost_tracked_packet_usa_lvm` | USA.TP.LVM
| `canadapost_xpresspost_usa` | USA.XP
| `canadapost_xpresspost_international` | INT.XP
| `canadapost_international_parcel_air` | INT.IP.AIR
| `canadapost_international_parcel_surface` | INT.IP.SURF
| `canadapost_priority_worldwide_envelope_intl` | INT.PW.ENV
| `canadapost_priority_worldwide_pak_intl` | INT.PW.PAK
| `canadapost_priority_worldwide_parcel_intl` | INT.PW.PARCEL
| `canadapost_small_packet_international_air` | INT.SP.AIR
| `canadapost_small_packet_international_surface` | INT.SP.SURF
| `canadapost_tracked_packet_international` | INT.TP




## Shipment Options


#### UPS Package

| Code | Identifier
--- | ---
| `ups_saturday_delivery_indicator` | SaturdayDeliveryIndicator
| `ups_access_point_cod` | AccessPointCOD
| `ups_deliver_to_addressee_only_indicator` | DeliverToAddresseeOnlyIndicator
| `ups_direct_delivery_only_indicator` | DirectDeliveryOnlyIndicator
| `ups_cod` | COD
| `ups_delivery_confirmation` | DeliveryConfirmation
| `ups_return_of_document_indicator` | ReturnOfDocumentIndicator
| `ups_up_scarbonneutral_indicator` | UPScarbonneutralIndicator
| `ups_certificate_of_origin_indicator` | CertificateOfOriginIndicator
| `ups_pickup_options` | PickupOptions
| `ups_delivery_options` | DeliveryOptions
| `ups_restricted_articles` | RestrictedArticles
| `ups_shipper_export_declaration_indicator` | ShipperExportDeclarationIndicator
| `ups_commercial_invoice_removal_indicator` | CommercialInvoiceRemovalIndicator
| `ups_import_control` | ImportControl
| `ups_return_service` | ReturnService
| `ups_sdl_shipment_indicator` | SDLShipmentIndicator
| `ups_epra_indicator` | EPRAIndicator


#### Purolator Courier

| Code | Identifier
--- | ---
| `purolator_dangerous_goods` | Dangerous Goods
| `purolator_chain_of_signature` | Chain of Signature
| `purolator_express_cheque` | ExpressCheque
| `purolator_hold_for_pickup` | Hold For Pickup
| `purolator_return_services` | Return Services
| `purolator_saturday_service` | Saturday Service
| `purolator_origin_signature_not_required` | Origin Signature Not Required (OSNR)
| `purolator_adult_signature_required` | Adult Signature Required (ASR)
| `purolator_special_handling` | Special Handling


#### FedEx Express

| Code | Identifier
--- | ---
| `fedex_blind_shipment` | BLIND_SHIPMENT
| `fedex_broker_select_option` | BROKER_SELECT_OPTION
| `fedex_call_before_delivery` | CALL_BEFORE_DELIVERY
| `fedex_cod` | COD
| `fedex_cod_remittance` | COD_REMITTANCE
| `fedex_custom_delivery_window` | CUSTOM_DELIVERY_WINDOW
| `fedex_cut_flowers` | CUT_FLOWERS
| `fedex_dangerous_goods` | DANGEROUS_GOODS
| `fedex_delivery_on_invoice_acceptance` | DELIVERY_ON_INVOICE_ACCEPTANCE
| `fedex_detention` | DETENTION
| `fedex_do_not_break_down_pallets` | DO_NOT_BREAK_DOWN_PALLETS
| `fedex_do_not_stack_pallets` | DO_NOT_STACK_PALLETS
| `fedex_dry_ice` | DRY_ICE
| `fedex_east_coast_special` | EAST_COAST_SPECIAL
| `fedex_electronic_trade_documents` | ELECTRONIC_TRADE_DOCUMENTS
| `fedex_event_notification` | EVENT_NOTIFICATION
| `fedex_exclude_from_consolidation` | EXCLUDE_FROM_CONSOLIDATION
| `fedex_exclusive_use` | EXCLUSIVE_USE
| `fedex_exhibition_delivery` | EXHIBITION_DELIVERY
| `fedex_exhibition_pickup` | EXHIBITION_PICKUP
| `fedex_expedited_alternate_delivery_route` | EXPEDITED_ALTERNATE_DELIVERY_ROUTE
| `fedex_expedited_one_day_earlier` | EXPEDITED_ONE_DAY_EARLIER
| `fedex_expedited_service_monitoring_and_delivery` | EXPEDITED_SERVICE_MONITORING_AND_DELIVERY
| `fedex_expedited_standard_day_early_delivery` | EXPEDITED_STANDARD_DAY_EARLY_DELIVERY
| `fedex_extra_labor` | EXTRA_LABOR
| `fedex_extreme_length` | EXTREME_LENGTH
| `fedex_one_rate` | FEDEX_ONE_RATE
| `fedex_flatbed_trailer` | FLATBED_TRAILER
| `fedex_food` | FOOD
| `fedex_freight_guarantee` | FREIGHT_GUARANTEE
| `fedex_freight_to_collect` | FREIGHT_TO_COLLECT
| `fedex_future_day_shipment` | FUTURE_DAY_SHIPMENT
| `fedex_hold_at_location` | HOLD_AT_LOCATION
| `fedex_holiday_delivery` | HOLIDAY_DELIVERY
| `fedex_holiday_guarantee` | HOLIDAY_GUARANTEE
| `fedex_home_delivery_premium` | HOME_DELIVERY_PREMIUM
| `fedex_inside_delivery` | INSIDE_DELIVERY
| `fedex_inside_pickup` | INSIDE_PICKUP
| `fedex_international_controlled_export_service` | INTERNATIONAL_CONTROLLED_EXPORT_SERVICE
| `fedex_international_mail_service` | INTERNATIONAL_MAIL_SERVICE
| `fedex_international_traffic_in_arms_regulations` | INTERNATIONAL_TRAFFIC_IN_ARMS_REGULATIONS
| `fedex_liftgate_delivery` | LIFTGATE_DELIVERY
| `fedex_liftgate_pickup` | LIFTGATE_PICKUP
| `fedex_limited_access_delivery` | LIMITED_ACCESS_DELIVERY
| `fedex_limited_access_pickup` | LIMITED_ACCESS_PICKUP
| `fedex_marking_or_tagging` | MARKING_OR_TAGGING
| `fedex_non_business_time` | NON_BUSINESS_TIME
| `fedex_pallet_shrinkwrap` | PALLET_SHRINKWRAP
| `fedex_pallet_weight_allowance` | PALLET_WEIGHT_ALLOWANCE
| `fedex_pallets_provided` | PALLETS_PROVIDED
| `fedex_pending_complete` | PENDING_COMPLETE
| `fedex_pending_shipment` | PENDING_SHIPMENT
| `fedex_permit` | PERMIT
| `fedex_pharmacy_delivery` | PHARMACY_DELIVERY
| `fedex_poison` | POISON
| `fedex_port_delivery` | PORT_DELIVERY
| `fedex_port_pickup` | PORT_PICKUP
| `fedex_pre_delivery_notification` | PRE_DELIVERY_NOTIFICATION
| `fedex_pre_eig_processing` | PRE_EIG_PROCESSING
| `fedex_pre_multiplier_processing` | PRE_MULTIPLIER_PROCESSING
| `fedex_protection_from_freezing` | PROTECTION_FROM_FREEZING
| `fedex_regional_mall_delivery` | REGIONAL_MALL_DELIVERY
| `fedex_regional_mall_pickup` | REGIONAL_MALL_PICKUP
| `fedex_return_shipment` | RETURN_SHIPMENT
| `fedex_returns_clearance` | RETURNS_CLEARANCE
| `fedex_returns_clearance_special_routing_required` | RETURNS_CLEARANCE_SPECIAL_ROUTING_REQUIRED
| `fedex_saturday_delivery` | SATURDAY_DELIVERY
| `fedex_saturday_pickup` | SATURDAY_PICKUP
| `fedex_shipment_assembly` | SHIPMENT_ASSEMBLY
| `fedex_sort_and_segregate` | SORT_AND_SEGREGATE
| `fedex_special_delivery` | SPECIAL_DELIVERY
| `fedex_special_equipment` | SPECIAL_EQUIPMENT
| `fedex_storage` | STORAGE
| `fedex_sunday_delivery` | SUNDAY_DELIVERY
| `fedex_third_party_consignee` | THIRD_PARTY_CONSIGNEE
| `fedex_top_load` | TOP_LOAD
| `fedex_usps_delivery` | USPS_DELIVERY
| `fedex_usps_pickup` | USPS_PICKUP
| `fedex_weighing` | WEIGHING


#### DHL Express

| Code | Identifier
--- | ---
| `dhl_logistics_services` | 0A
| `dhl_mailroom_management` | 0B
| `dhl_pallet_administration` | 0C
| `dhl_warehousing` | 0D
| `dhl_express_logistics_centre` | 0E
| `dhl_strategic_parts_centre` | 0F
| `dhl_local_distribution_centre` | 0G
| `dhl_terminal_handling` | 0H
| `dhl_cross_docking` | 0I
| `dhl_inventory_management` | 0J
| `dhl_loading_unloading` | 0K
| `dhl_product_kitting` | 0L
| `dhl_priority_account_desk` | 0M
| `dhl_document_archiving` | 0N
| `dhl_saturday_delivery` | AA
| `dhl_saturday_pickup` | AB
| `dhl_holiday_delivery` | AC
| `dhl_holiday_pickup` | AD
| `dhl_domestic_saturday_delivery` | AG
| `dhl_standard` | BA
| `dhl_globalmail_item` | BB
| `dhl_letter` | BC
| `dhl_packet` | BD
| `dhl_letter_plus` | BE
| `dhl_packet_plus` | BF
| `dhl_elevated_risk` | CA
| `dhl_restricted_destination` | CB
| `dhl_security_validation` | CC
| `dhl_secure_protection` | CD
| `dhl_proof_of_identity` | CE
| `dhl_secure_storage` | CF
| `dhl_diplomatic_material` | CG
| `dhl_smart_sensor` | CH
| `dhl_visa_program` | CI
| `dhl_onboard_courier` | CJ
| `dhl_secure_safebox` | CK
| `dhl_smart_sentry` | CL
| `dhl_split_duties_and_tax` | DC
| `dhl_duties_and_taxes_paid` | DD
| `dhl_receiver_paid` | DE
| `dhl_duties_and_taxes_unpaid` | DS
| `dhl_import_billing` | DT
| `dhl_importer_of_record` | DU
| `dhl_go_green_carbon_neutral` | EA
| `dhl_go_green_carbon_footprint` | EB
| `dhl_go_green_carbon_estimate` | EC
| `dhl_fuel_surcharge_b` | FB
| `dhl_fuel_surcharge_c` | FC
| `dhl_fuel_surcharge_f` | FF
| `dhl_smartphone_box` | GA
| `dhl_laptop_box` | GB
| `dhl_bottle_box` | GC
| `dhl_repacking` | GD
| `dhl_tablet_box` | GE
| `dhl_filler_material` | GF
| `dhl_packaging` | GG
| `dhl_diplomatic_bag` | GH
| `dhl_pallet_box` | GI
| `dhl_lock_box` | GJ
| `dhl_lithium_ion_pi965_section_ii` | HB
| `dhl_dry_ice_un1845` | HC
| `dhl_lithium_ion_pi965_966_section_ii` | HD
| `dhl_dangerous_goods` | HE
| `dhl_perishable_cargo` | HG
| `dhl_excepted_quantity` | HH
| `dhl_spill_cleaning` | HI
| `dhl_consumer_commodities` | HK
| `dhl_limited_quantities_adr` | HL
| `dhl_lithium_metal_pi969_section_ii` | HM
| `dhl_adr_load_exemption` | HN
| `dhl_lithium_ion_pi967_section_ii` | HV
| `dhl_lithium_metal_pi970_section_ii` | HW
| `dhl_biological_un3373` | HY
| `dhl_extended_liability` | IB
| `dhl_contract_insurance` | IC
| `dhl_shipment_insurance` | II
| `dhl_delivery_notification` | JA
| `dhl_pickup_notification` | JC
| `dhl_proactive_tracking` | JD
| `dhl_performance_reporting` | JE
| `dhl_prealert_notification` | JY
| `dhl_change_of_billing` | KA
| `dhl_cash_on_delivery` | KB
| `dhl_printed_invoice` | KD
| `dhl_waybill_copy` | KE
| `dhl_import_paperwork` | KF
| `dhl_payment_on_pickup` | KY
| `dhl_shipment_intercept` | LA
| `dhl_shipment_redirect` | LC
| `dhl_storage_at_facility` | LE
| `dhl_cold_storage` | LG
| `dhl_specific_routing` | LH
| `dhl_service_recovery` | LV
| `dhl_alternative_address` | LW
| `dhl_hold_for_collection` | LX
| `dhl_address_correction_a` | MA
| `dhl_address_correction_b` | MB
| `dhl_neutral_delivery` | NN
| `dhl_remote_area_pickup` | OB
| `dhl_remote_area_delivery_c` | OC
| `dhl_out_of_service_area` | OE
| `dhl_remote_area_delivery_o` | OO
| `dhl_shipment_preparation` | PA
| `dhl_shipment_labeling` | PB
| `dhl_shipment_consolidation` | PC
| `dhl_relabeling_data_entry` | PD
| `dhl_preprinted_waybill` | PE
| `dhl_piece_labelling` | PS
| `dhl_data_staging_03` | PT
| `dhl_data_staging_06` | PU
| `dhl_data_staging_12` | PV
| `dhl_data_staging_24` | PW
| `dhl_standard_pickup` | PX
| `dhl_scheduled_pickup` | PY
| `dhl_dedicated_pickup` | QA
| `dhl_early_pickup` | QB
| `dhl_late_pickup` | QD
| `dhl_residential_pickup` | QE
| `dhl_loading_waiting` | QF
| `dhl_bypass_injection` | QH
| `dhl_direct_injection` | QI
| `dhl_drop_off_at_facility` | QY
| `dhl_delivery_signature` | SA
| `dhl_content_signature` | SB
| `dhl_named_signature` | SC
| `dhl_adult_signature` | SD
| `dhl_contract_signature` | SE
| `dhl_alternative_signature` | SW
| `dhl_no_signature_required` | SX
| `dhl_dedicated_delivery` | TA
| `dhl_early_delivery` | TB
| `dhl_time_window_delivery` | TC
| `dhl_evening_delivery` | TD
| `dhl_delivery_on_appointment` | TE
| `dhl_return_undeliverable` | TG
| `dhl_swap_delivery` | TH
| `dhl_unloading_waiting` | TJ
| `dhl_residential_delivery` | TK
| `dhl_repeat_delivery` | TN
| `dhl_alternative_date` | TT
| `dhl_no_partial_delivery` | TU
| `dhl_service_point_24_7` | TV
| `dhl_pre_9_00` | TW
| `dhl_pre_10_30` | TX
| `dhl_pre_12_00` | TY
| `dhl_thermo_packaging` | UA
| `dhl_ambient_vialsafe` | UB
| `dhl_ambient_non_insulated` | UC
| `dhl_ambient_insulated` | UD
| `dhl_ambient_extreme` | UE
| `dhl_chilled_box_s` | UF
| `dhl_chilled_box_m` | UG
| `dhl_chilled_box_l` | UH
| `dhl_frozen_no_ice_s` | UI
| `dhl_frozen_no_ice_m` | UJ
| `dhl_frozen_no_ice_l` | UK
| `dhl_frozen_ice_sticks_s` | UL
| `dhl_frozen_ice_sticks_m` | UM
| `dhl_frozen_ice_sticks_l` | UN
| `dhl_frozen_ice_plates_s` | UO
| `dhl_frozen_ice_plates_m` | UP
| `dhl_frozen_ice_plates_l` | UQ
| `dhl_combination_no_ice` | UR
| `dhl_combination_dry_ice` | US
| `dhl_frozen_ice_sticks_e` | UT
| `dhl_frozen_ice_plates_e` | UV
| `dhl_customer_tcp_1` | UW
| `dhl_thermo_accessories` | VA
| `dhl_absorbent_sleeve` | VB
| `dhl_cooland_wrap` | VC
| `dhl_dry_ice_supplies` | VD
| `dhl_pressure_bag_s` | VE
| `dhl_pressure_bag_m` | VF
| `dhl_pressure_bag_l` | VG
| `dhl_informal_clearance` | WA
| `dhl_formal_clearance` | WB
| `dhl_payment_deferment` | WC
| `dhl_clearance_authorization` | WD
| `dhl_multiline_entry` | WE
| `dhl_post_clearance_modification` | WF
| `dhl_handover_to_broker` | WG
| `dhl_physical_intervention` | WH
| `dhl_bio_phyto_veterinary_controls` | WI
| `dhl_obtaining_permits_and_licences` | WJ
| `dhl_bonded_storage` | WK
| `dhl_bonded_transit_documents` | WL
| `dhl_temporary_import_export` | WM
| `dhl_under_bond_guarantee` | WN
| `dhl_export_declaration` | WO
| `dhl_exporter_validation` | WP
| `dhl_certificate_of_origin` | WQ
| `dhl_document_translation` | WR
| `dhl_personal_effects` | WS
| `dhl_paperless_trade` | WY
| `dhl_import_export_taxes` | XB
| `dhl_unrecoverable_origin_tax` | XC
| `dhl_quarantine_inspection` | XD
| `dhl_merchandise_process` | XE
| `dhl_domestic_postal_tax` | XF
| `dhl_tier_two_tax` | XG
| `dhl_tier_three_tax` | XH
| `dhl_import_penalty` | XI
| `dhl_cargo_zone_process` | XJ
| `dhl_import_export_duties` | XX
| `dhl_premium_09_00` | Y1
| `dhl_premium_10_30` | Y2
| `dhl_premium_12_00` | Y3
| `dhl_over_sized_piece_b` | YB
| `dhl_over_handled_piece_c` | YC
| `dhl_multipiece_shipment` | YE
| `dhl_over_weight_piece_f` | YF
| `dhl_over_sized_piece_g` | YG
| `dhl_over_handled_piece_h` | YH
| `dhl_premium_9_00_i` | YI
| `dhl_premium_10_30_j` | YJ
| `dhl_premium_12_00_k` | YK
| `dhl_paket_shipment` | YV
| `dhl_breakbulk_mother` | YW
| `dhl_breakbulk_baby` | YX
| `dhl_over_weight_piece_y` | YY
| `dhl_customer_claim` | ZA
| `dhl_damage_compensation` | ZB
| `dhl_loss_compensation` | ZC
| `dhl_customer_rebate` | ZD
| `dhl_e_com_discount` | ZE


#### Canada Post

| Code | Identifier
--- | ---
| `canadapost_signature` | SO
| `canadapost_coverage` | COV
| `canadapost_collect_on_delivery` | COD
| `canadapost_proof_of_age_required_18` | PA18
| `canadapost_proof_of_age_required_19` | PA19
| `canadapost_card_for_pickup` | HFP
| `canadapost_do_not_safe_drop` | DNS
| `canadapost_leave_at_door` | LAD
| `canadapost_deliver_to_post_office` | D2PO
| `canadapost_return_at_senders_expense` | RASE
| `canadapost_return_to_sender` | RTS
| `canadapost_abandon` | ABAN

