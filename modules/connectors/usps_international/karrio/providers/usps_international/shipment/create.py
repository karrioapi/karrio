"""Karrio USPS create label implementation."""

import karrio.schemas.usps_international.label_request as usps
import karrio.schemas.usps_international.label_response as shipping

import time
import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.core.errors as errors
import karrio.providers.usps_international.error as error
import karrio.providers.usps_international.utils as provider_utils
import karrio.providers.usps_international.units as provider_units


def parse_shipment_response(
    _response: lib.Deserializable[typing.List[dict]],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.RateDetails], typing.List[models.Message]]:
    responses = _response.deserialize()

    shipment = lib.to_multi_piece_shipment(
        [
            (
                f"{_}",
                _extract_details(response, settings, _response.ctx),
            )
            for _, response in enumerate(responses, start=1)
            if response.get("error") is None
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
    label_type = ctx.get("label_type", "PDF")

    return models.ShipmentDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=details.labelMetadata.internationalTrackingNumber,
        shipment_identifier=details.labelMetadata.internationalTrackingNumber,
        label_type=label_type,
        docs=models.Documents(label=label),
        meta=dict(
            SKU=details.labelMetadata.SKU,
            postage=details.labelMetadata.postage,
        ),
    )


def shipment_request(
    payload: models.ShipmentRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)

    if shipper.country_code != units.Country.US.name:
        raise errors.OriginNotServicedError(shipper.country_code)

    if recipient.country_code == units.Country.US.name:
        raise errors.DestinationNotServicedError(recipient.country_code)

    service = provider_units.ShippingService.map(payload.service).value_or_key
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
    customs = lib.to_customs_info(
        payload.customs,
        shipper=payload.shipper,
        recipient=payload.recipient,
        weight_unit=units.WeightUnit.LB.name,
    )
    pickup_location = lib.to_address(options.hold_for_pickup_address.state)
    label_type = provider_units.LabelType.map(payload.label_type).value or "PDF"

    # map data to convert karrio model to usps specific type
    request = [
        usps.LabelRequestType(
            imageInfo=usps.ImageInfoType(
                imageType=label_type,
                labelType="4X6LABEL",
            ),
            toAddress=usps.AddressType(
                streetAddress=recipient.address_line1,
                secondaryAddress=recipient.address_line2,
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
            ),
            fromAddress=usps.AddressType(
                streetAddress=shipper.address_line1,
                secondaryAddress=shipper.address_line2,
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
            ),
            senderAddress=usps.AddressType(
                streetAddress=shipper.address_line1,
                secondaryAddress=shipper.address_line2,
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
            ),
            packageDescription=usps.PackageDescriptionType(
                weightUOM="lb",
                weight=package.weight.LB,
                dimensionsUOM="in",
                length=package.length.IN,
                height=package.height.IN,
                width=package.width.IN,
                girth=package.girth,
                mailClass=service,
                rateIndicator=package.options.usps_rate_indicator.state or "SP",
                processingCategory=lib.identity(
                    package.options.usps_processing_category.state or "NON_MACHINABLE"
                ),
                destinationEntryFacilityType=lib.identity(
                    package.options.usps_destination_facility_type.state or "NONE"
                ),
                destinationEntryFacilityAddress=lib.identity(
                    usps.DestinationEntryFacilityAddressType(
                        streetAddress=pickup_location.address_line1,
                        secondaryAddress=pickup_location.address_line2,
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
                        generateGXEvent=None,
                        originalPackage=None,
                    )
                    if (package.total_value or 0.0) > 0.0
                    else None
                ),
                customerReference=[
                    usps.CustomerReferenceType(
                        referenceNumber=reference,
                    )
                    for reference in [payload.reference]
                    if reference is not None
                ],
                extraServices=[
                    lib.to_int(_.code)
                    for __, _ in package.options.items()
                    if __ not in provider_units.CUSTOM_OPTIONS
                ],
                mailingDate=lib.fdate(
                    package.options.shipment_date.state or time.strftime("%Y-%m-%d")
                ),
            ),
            customsForm=usps.CustomsFormType(
                contentComments=customs.content_description,
                restrictionType=package.options.usps_restriction_type.state,
                restrictionComments=package.options.restrictionComments.state,
                AESITN=customs.options.aes.state,
                invoiceNumber=customs.invoice,
                licenseNumber=customs.options.license_number.state,
                certificateNumber=customs.options.certificate_number.state,
                customsContentType=lib.identity(
                    provider_units.CustomsContentType.map(customs.content_type).value
                    or "OTHER"
                ),
                importersReference=None,
                exportersReference=None,
                contents=[
                    usps.ContentType(
                        itemDescription=item.description,
                        itemQuantity=item.quantity,
                        itemValue=item.value_amount,
                        itemTotalValue=item.value_amount * item.quantity,
                        weightUOM="lb",
                        itemWeight=item.weight,
                        itemTotalWeight=item.weight * item.quantity,
                        HSTariffNumber=item.hs_code,
                        countryofOrigin=item.origin_country,
                        itemCategory=None,
                        itemSubcategory=None,
                    )
                    for item in customs.commodities
                ],
            ),
        )
        for package in packages
    ]

    return lib.Serializable(request, lib.to_dict, dict(label_type=label_type))
