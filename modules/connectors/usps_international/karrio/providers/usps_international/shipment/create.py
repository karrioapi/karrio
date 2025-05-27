"""Karrio USPS International create label implementation."""

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
    label_type = ctx.get("label_type", "PDF")

    return models.ShipmentDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=details.labelMetadata.trackingNumber,
        shipment_identifier=details.labelMetadata.trackingNumber,
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
    customs = lib.to_customs_info(
        payload.customs,
        shipper=payload.shipper,
        recipient=payload.recipient,
        weight_unit=units.WeightUnit.LB.name,
    )
    pickup_location = lib.to_address(options.hold_for_pickup_address.state)
    label_type = provider_units.LabelType.map(payload.label_type).value or "PDF"

    package_options = lambda package: lib.identity(
        package.options
        if mail_class not in []
        else {}
    )

    # map data to convert karrio model to usps specific type
    request = [
        usps.LabelRequestType(
            imageInfo=usps.ImageInfoType(
                imageType=label_type,
                labelType="4X6LABEL",
            ),
            toAddress=usps.ToAddressType(
                streetAddress=recipient.address_line1,
                secondaryAddress=recipient.address_line2,
                city=recipient.city,
                postalCode=recipient.postal_code,
                province=recipient.state_code,
                country=recipient.country_code,
                countryISOAlpha2Code=recipient.country_code,
                firstName=recipient.first_name or recipient.person_name,
                lastName=recipient.last_name or " ",
                firm=recipient.company_name,
                phone=recipient.phone_number,
            ),
            fromAddress=usps.AddressType(
                streetAddress=shipper.address_line1,
                secondaryAddress=shipper.address_line2,
                city=shipper.city,
                state=shipper.state_code,
                ZIPCode=lib.to_zip5(shipper.postal_code),
                ZIPPlus4=lib.to_zip4(shipper.postal_code),
                urbanization=None,
                firstName=shipper.first_name or shipper.person_name,
                lastName=shipper.last_name or " ",
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
                state=shipper.state_code,  # only US states are supported
                ZIPCode=lib.identity(
                    lib.to_zip4(shipper.postal_code) or shipper.postal_code
                ),
                ZIPPlus4=lib.to_zip4(shipper.postal_code),
                urbanization=None,
                firstName=shipper.first_name or shipper.person_name,
                lastName=shipper.last_name or " ",
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
                        secondaryAddress=pickup_location.address_line2,
                        city=pickup_location.city,
                        state=pickup_location.state_code,
                        ZIPCode=lib.to_zip4(pickup_location.postal_code) or "",
                        ZIPPlus4=lib.to_zip5(pickup_location.postal_code) or "",
                        urbanization=None,
                    )
                    if package.options.hold_for_pickup_address.state is not None
                    else None
                ),
                packageOptions=usps.PackageOptionsType(
                    packageValue=lib.identity(
                        package.total_value
                        or package.options.declared_value.state
                        or customs.commodities.value_amount
                        or 1.0
                    ),
                    nonDeliveryOption=None,
                    redirectAddress=None,
                    generateGXEvent=None,
                    originalPackage=None,
                ),
                customerReference=[
                    usps.CustomerReferenceType(
                        referenceNumber=reference,
                    )
                    for reference in [payload.reference]
                    if reference is not None
                ],
                extraServices=lib.identity(
                    package.options.usps_extra_services.state
                    or [
                        lib.to_int(_.code)
                        for __, _ in package_options(package).items()
                        if __ not in provider_units.CUSTOM_OPTIONS
                    ]
                ),
                mailingDate=lib.fdate(
                    package.options.shipment_date.state or time.strftime("%Y-%m-%d")
                ),
            ),
            customsForm=usps.CustomsFormType(
                contentComments=customs.content_description,
                restrictionType=package.options.usps_restriction_type.state,
                restrictionComments=package.options.usps_restriction_comments.state,
                AESITN=customs.options.aes.state,
                invoiceNumber=customs.invoice,
                licenseNumber=customs.options.license_number.state,
                certificateNumber=lib.text(
                    customs.options.certificate_number.state,
                    max=12,
                ),
                customsContentType=lib.identity(
                    provider_units.CustomsContentType.map(customs.content_type).value
                    or "OTHER"
                ),
                importersReference=None,
                exportersReference=None,
                contents=[
                    usps.ContentType(
                        itemDescription=lib.text(
                            item.description or item.title or "Item",
                            max=12,
                        ),
                        itemQuantity=item.quantity,
                        itemValue=item.value_amount,
                        itemTotalValue=item.value_amount * item.quantity,
                        weightUOM="lb",
                        itemWeight=item.weight,
                        itemTotalWeight=item.weight * item.quantity,
                        HSTariffNumber=item.hs_code,
                        countryofOrigin=item.origin_country,
                        itemCategory=item.category,
                        itemSubcategory=None,
                    )
                    for item in customs.commodities
                ],
            ),
        )
        for package in packages
    ]

    return lib.Serializable(request, lib.to_dict, dict(label_type=label_type))
