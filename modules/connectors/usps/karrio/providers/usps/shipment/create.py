"""Karrio USPS create label implementation."""

import karrio.schemas.usps.label_request as usps
import karrio.schemas.usps.label_response as shipping

import time
import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.core.errors as errors
import karrio.providers.usps.error as error
import karrio.providers.usps.utils as provider_utils
import karrio.providers.usps.units as provider_units


def parse_shipment_response(
    _response: lib.Deserializable[typing.List[dict]],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.RateDetails], typing.List[models.Message]]:
    responses = _response.deserialize()

    shipment = lib.to_multi_piece_shipment(
        [
            (
                f"{_}",
                (
                    _extract_details(response, settings)
                    if response.get("error") is None
                    else None
                ),
            )
            for _, response in enumerate(responses, start=1)
        ]
    )
    messages: typing.List[models.Message] = sum(
        [error.parse_error_response(response, settings) for response in responses],
        start=[],
    )

    return shipment, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.ShipmentDetails:
    shipment = lib.to_object(shipping.ShipmentResponseType, data)
    label = shipment.labelImage
    invoice = shipment.receiptImage

    return models.ShipmentDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=shipment.labelMetadata.trackingNumber,
        shipment_identifier=shipment.labelMetadata.trackingNumber,
        label_type="PDF",
        docs=models.Documents(label=label, invoice=invoice),
        meta=dict(
            SKU=shipment.labelMetadata.SKU,
            postage=shipment.labelMetadata.postage,
            routingInformation=shipment.labelMetadata.routingInformation,
            labelBrokerID=shipment.labelMetadata.labelBrokerID,
        ),
    )


def shipment_request(
    payload: models.ShipmentRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:

    if (
        shipper.country_code is not None
        and shipper.country_code != units.Country.US.name
    ):
        raise errors.OriginNotServicedError(shipper.country_code)

    if (
        recipient.country_code is not None
        and recipient.country_code != units.Country.US.name
    ):
        raise errors.DestinationNotServicedError(recipient.country_code)

    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    return_address = lib.to_address(payload.return_address)
    pickup_location = lib.to_address(options.hold_for_pickup_address.state)
    service = provider_units.ShippingService.map(payload.service).value_or_key
    options = lib.to_shipping_options(
        payload.options,
        package_options=packages.options,
    )
    packages = lib.to_packages(
        payload.parcels,
        options=options,
        package_option_type=provider_units.ShippingOption,
        shipping_options_initializer=provider_units.shipping_options_initializer,
    )

    # map data to convert karrio model to usps specific type
    request = [
        usps.LabelRequestType(
            imageInfo=usps.ImageInfoType(
                imageType=lib.identity(
                    provider_units.LabelType.map(payload.label_type).value or "PDF"
                ),
                labelType="4X6LABEL",
                # shipInfo=None,
                receiptOption="SEPARATE_PAGE",
                suppressPostage=None,
                suppressMailDate=None,
                returnLabel=None,
            ),
            toAddress=usps.AddressType(
                streetAddress=recipient.street_name,
                secondaryAddress=recipient.street_number,
                city=recipient.city,
                state=recipient.state,
                ZIPCode=lib.to_zip5(recipient.postal_code) or "",
                ZIPPlus4=lib.to_zip4(recipient.postal_code) or "",
                urbanization=None,
                firstName=recipient.person_name,
                lastName=None,
                firm=recipient.company_name,
                phone=recipient.phone_number,
                email=recipient.email,
                ignoreBadAddress=True,
                platformUserId=None,
                parcelLockerDelivery=None,
                holdForPickup=package.options.usps_hold_for_pickup.state,
                facilityId=package.options.usps_facility_id.state,
            ),
            fromAddress=usps.AddressType(
                streetAddress=shipper.street_name,
                secondaryAddress=shipper.street_number,
                city=shipper.city,
                state=shipper.state,
                ZIPCode=lib.to_zip4(shipper.postal_code) or "",
                ZIPPlus4=lib.to_zip5(shipper.postal_code) or "",
                urbanization=None,
                firstName=shipper.person_name,
                lastName=None,
                firm=shipper.company_name,
                phone=shipper.phone_number,
                email=shipper.email,
                ignoreBadAddress=True,
                platformUserId=None,
                parcelLockerDelivery=None,
                holdForPickup=None,
                facilityId=None,
            ),
            senderAddress=usps.AddressType(
                streetAddress=shipper.street_name,
                secondaryAddress=shipper.street_number,
                city=shipper.city,
                state=shipper.state,
                ZIPCode=lib.to_zip4(shipper.postal_code) or "",
                ZIPPlus4=lib.to_zip5(shipper.postal_code) or "",
                urbanization=None,
                firstName=shipper.person_name,
                lastName=None,
                firm=shipper.company_name,
                phone=shipper.phone_number,
                email=shipper.email,
                ignoreBadAddress=True,
                platformUserId=None,
                parcelLockerDelivery=None,
                holdForPickup=None,
                facilityId=None,
            ),
            returnAddress=usps.AddressType(
                streetAddress=return_address.street_name,
                secondaryAddress=return_address.street_number,
                city=return_address.city,
                state=return_address.state,
                ZIPCode=lib.to_zip4(return_address.postal_code) or "",
                ZIPPlus4=lib.to_zip5(return_address.postal_code) or "",
                urbanization=None,
                firstName=return_address.person_name,
                lastName=None,
                firm=return_address.company_name,
                phone=return_address.phone_number,
                email=return_address.email,
                ignoreBadAddress=True,
                platformUserId=None,
                parcelLockerDelivery=None,
                holdForPickup=None,
                facilityId=None,
            ),
            packageDescription=usps.PackageDescriptionType(
                weightUOM="lb",
                weight=package.weight.LB,
                dimensionsUOM="in",
                length=package.length.IN,
                height=package.height.IN,
                width=package.width.IN,
                girth=package.girth,
                mailClass=service.value_or_key,
                rateIndicator=package.options.usps_rate_indicator.state or "SP",
                processingCategory=lib.identity(
                    package.options.usps_processing_category.state or "NON_MACHINABLE"
                ),
                destinationEntryFacilityType=lib.identity(
                    package.options.usps_destination_facility_type.state or "NONE"
                ),
                destinationEntryFacilityAddress=lib.identity(
                    usps.DestinationEntryFacilityAddressType(
                        streetAddress=pickup_location.street_name,
                        secondaryAddress=pickup_location.street_number,
                        city=pickup_location.city,
                        state=pickup_location.state,
                        ZIPCode=lib.to_zip4(pickup_location.postal_code) or "",
                        ZIPPlus4=lib.to_zip5(pickup_location.postal_code) or "",
                        urbanization=None,
                    )
                    if package.options.hold_for_pickup_address.state is not None
                    else None
                ),
                packageOptions=lib.identity(
                    usps.PackageOptionsType(
                        packageValue=package.total_value,
                        nonDeliveryOption=None,
                        redirectAddress=None,
                        contentType=None,
                        generateGXEvent=None,
                        containers=[],
                        ancillaryServiceEndorsements=None,
                        originalPackage=None,
                    )
                    if (package.total_value or 0.0) > 0.0
                    else None
                ),
                customerReference=[
                    usps.CustomerReferenceType(
                        referenceNumber=reference,
                        printReferenceNumber=True,
                    )
                    for reference in [payload.reference]
                    if reference is not None
                ],
                extraServices=[
                    _.code
                    for __, _ in package.options.items
                    if _.name not in provider_units.CUSTOM_OPTIONS
                ],
                mailingDate=lib.fdate(
                    package.options.shipment_date.state or time.strftime("%Y-%m-%d")
                ),
                carrierRelease=package.options.usps_carrier_release.state,
                physicalSignatureRequired=package.options.usps_physical_signature_required.state,
                inductionZIPCode=lib.identity(
                    return_address.postal_code or shipper.postal_code
                ),
            ),
            customsForm=None,
        )
        for package in packages
    ]

    return lib.Serializable(request, lib.to_dict)
