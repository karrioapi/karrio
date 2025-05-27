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
) -> typing.Tuple[models.ShipmentDetails, typing.List[models.Message]]:
    responses = _response.deserialize()
    shipment = lib.to_multi_piece_shipment(
        [
            (
                f"{_}",
                _extract_details(response, settings, _response.ctx),
            )
            for _, response in enumerate(responses, start=1)
            if response.get("error") is None
            and response.get("labelMetadata") is not None
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
    ctx: dict = None,
) -> models.ShipmentDetails:
    details = lib.to_object(shipping.LabelResponseType, data)
    label = details.labelImage
    invoice = details.receiptImage
    label_type = ctx.get("label_type", "PDF")

    return models.ShipmentDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=details.labelMetadata.trackingNumber,
        shipment_identifier=details.labelMetadata.trackingNumber,
        label_type=label_type,
        docs=models.Documents(label=label, invoice=invoice),
        meta=dict(
            SKU=details.labelMetadata.SKU,
            postage=details.labelMetadata.postage,
            routingInformation=details.labelMetadata.routingInformation,
            labelBrokerID=details.labelMetadata.labelBrokerID,
        ),
    )


def shipment_request(
    payload: models.ShipmentRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)

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

    return_address = lib.to_address(payload.return_address)
    mail_class = lib.identity(
        provider_units.ShippingService.to_mail_class(payload.service).value
        or payload.service
    )
    options = lib.to_shipping_options(
        payload.options,
        initializer=provider_units.shipping_options_initializer,
    )
    packages = lib.to_packages(
        payload.parcels,
        options=options,
        package_option_type=provider_units.ShippingOption,
        shipping_options_initializer=provider_units.shipping_options_initializer,
    )
    pickup_location = lib.to_address(options.hold_for_pickup_address.state)
    label_type = provider_units.LabelType.map(payload.label_type).value or "PDF"

    package_options = lambda package: lib.identity(
        package.options
        if mail_class not in provider_units.INCOMPATIBLE_SERVICES
        else {}
    )

    # map data to convert karrio model to usps specific type
    request = [
        usps.LabelRequestType(
            imageInfo=usps.ImageInfoType(
                imageType=label_type,
                labelType="4X6LABEL",
                # shipInfo=None,
                receiptOption="NONE",
                suppressPostage=None,
                suppressMailDate=None,
                returnLabel=None,
            ),
            toAddress=usps.AddressType(
                streetAddress=recipient.address_line1,
                secondaryAddress=recipient.address_line2,
                city=recipient.city,
                state=recipient.state_code,
                ZIPCode=lib.to_zip5(recipient.postal_code) or "",
                ZIPPlus4=lib.to_zip4(recipient.postal_code) or "",
                urbanization=None,
                firstName=recipient.first_name,
                lastName=recipient.last_name,
                firm=recipient.company_name,
                phone=provider_utils.parse_phone_number(recipient.phone_number),
                email=recipient.email,
                ignoreBadAddress=True,
                platformUserId=None,
                parcelLockerDelivery=None,
                holdForPickup=package.options.usps_hold_for_pickup.state,
                facilityId=package.options.usps_facility_id.state,
            ),
            fromAddress=usps.AddressType(
                streetAddress=shipper.address_line1,
                secondaryAddress=shipper.address_line2,
                city=shipper.city,
                state=shipper.state_code,
                ZIPCode=lib.to_zip5(shipper.postal_code) or "",
                ZIPPlus4=lib.to_zip4(shipper.postal_code) or "",
                urbanization=None,
                firstName=shipper.first_name,
                lastName=shipper.last_name,
                firm=shipper.company_name,
                phone=provider_utils.parse_phone_number(shipper.phone_number),
                email=shipper.email,
                ignoreBadAddress=True,
                platformUserId=None,
                parcelLockerDelivery=None,
                holdForPickup=None,
                facilityId=None,
            ),
            senderAddress=usps.AddressType(
                streetAddress=shipper.address_line1,
                secondaryAddress=shipper.address_line2r,
                city=shipper.city,
                state=shipper.state_code,
                ZIPCode=lib.to_zip5(shipper.postal_code) or "",
                ZIPPlus4=lib.to_zip4(shipper.postal_code) or "",
                urbanization=None,
                firstName=shipper.first_name,
                lastName=shipper.last_name,
                firm=shipper.company_name,
                phone=provider_utils.parse_phone_number(shipper.phone_number),
                email=shipper.email,
                ignoreBadAddress=True,
                platformUserId=None,
                parcelLockerDelivery=None,
                holdForPickup=None,
                facilityId=None,
            ),
            returnAddress=lib.identity(
                usps.AddressType(
                    streetAddress=return_address.address_line1,
                    secondaryAddress=return_address.address_line2r,
                    city=return_address.city,
                    state=return_address.state_code,
                    ZIPCode=lib.to_zip5(return_address.postal_code) or "",
                    ZIPPlus4=lib.to_zip4(return_address.postal_code) or "",
                    urbanization=None,
                    firstName=return_address.first_name,
                    lastName=return_address.last_name,
                    firm=return_address.company_name,
                    phone=provider_utils.parse_phone_number(return_address.phone_number),
                    email=return_address.email,
                    ignoreBadAddress=True,
                    platformUserId=None,
                    parcelLockerDelivery=None,
                    holdForPickup=None,
                    facilityId=None,
                )
                if payload.return_address is not None
                else None
            ),
            packageDescription=usps.PackageDescriptionType(
                weightUOM="lb",
                weight=package.weight.LB,
                dimensionsUOM="in",
                length=package.length.IN,
                height=package.height.IN,
                width=package.width.IN,
                girth=package.girth.value,
                mailClass=mail_class,
                rateIndicator=package.options.usps_rate_indicator.state or "DR",
                processingCategory=lib.identity(
                    package.options.usps_processing_category.state or "NON_MACHINABLE"
                ),
                destinationEntryFacilityType=lib.identity(
                    package.options.usps_destination_facility_type.state or "NONE"
                ),
                destinationEntryFacilityAddress=lib.identity(
                    usps.DestinationEntryFacilityAddressType(
                        streetAddress=pickup_location.address_line1,
                        secondaryAddress=pickup_location.address_line2r,
                        city=pickup_location.city,
                        state=pickup_location.state_code,
                        ZIPCode=lib.to_zip5(pickup_location.postal_code) or "",
                        ZIPPlus4=lib.to_zip4(pickup_location.postal_code) or "",
                        urbanization=None,
                    )
                    if package.options.hold_for_pickup_address.state is not None
                    else None
                ),
                packageOptions=lib.identity(
                    usps.PackageOptionsType(
                        packageValue=lib.identity(
                            package.total_value
                            or package.options.declared_value.state
                            or 1.0
                        ),
                        nonDeliveryOption=None,
                        redirectAddress=None,
                        contentType=None,
                        generateGXEvent=None,
                        containers=[],
                        ancillaryServiceEndorsements=None,
                        originalPackage=None,
                    )
                    if (package.total_value or package.options.declared_value.state)
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
                extraServices=lib.identity(
                    package.options.usps_extra_services.state
                    or [
                        lib.to_int(_.code)
                        for __, _ in package_options(package).items()
                        if _.name not in provider_units.CUSTOM_OPTIONS
                    ]
                ),
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

    return lib.Serializable(request, lib.to_dict, dict(label_type=label_type))
