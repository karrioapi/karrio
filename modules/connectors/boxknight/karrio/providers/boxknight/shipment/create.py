import karrio.schemas.boxknight.order_request as boxknight
import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.core.errors as errors
import karrio.providers.boxknight.error as error
import karrio.providers.boxknight.utils as provider_utils
import karrio.providers.boxknight.units as provider_units


def parse_shipment_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.RateDetails], typing.List[models.Message]]:
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)
    shipment = (
        _extract_details(response, settings) if response.get("error") is None else None
    )

    return shipment, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.ShipmentDetails:
    return models.ShipmentDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=data["order_id"],
        shipment_identifier=data["order_id"],
        label_type=data["label_type"],
        docs=models.Documents(label=data["label"]),
        meta=dict(service_name=data.get("service")),
    )


def shipment_request(
    payload: models.ShipmentRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    if (
        payload.shipper.country_code is not None
        and payload.shipper.country_code != units.Country.CA.name
    ):
        raise errors.OriginNotServicedError(payload.shipper.country_code)

    if (
        payload.recipient.country_code is not None
        and payload.recipient.country_code != units.Country.CA.name
    ):
        raise errors.DestinationNotServicedError(payload.recipient.country_code)

    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    packages = lib.to_packages(payload.parcels)
    service = provider_units.ShippingService.map(payload.service).value_or_key
    options = lib.to_shipping_options(
        payload.options,
        package_options=packages.options,
        initializer=provider_units.shipping_options_initializer,
    )

    request = dict(
        order=boxknight.OrderRequest(
            recipient=(
                boxknight.Recipient(
                    name=recipient.contact,
                    phone=recipient.phone_number,
                    notes=None,
                    email=recipient.email,
                )
                if any([recipient.contact, recipient.phone_number, recipient.email])
                else None
            ),
            recipientAddress=boxknight.Address(
                street=recipient.address_line1,
                unit=recipient.address_line2,
                city=recipient.city,
                province=units.CountryState.CA.value[recipient.state_code].value,
                country=units.Country.CA.value,
                postalCode=recipient.postal_code,
                isBusinessAddress=recipient.residential is False,
            ),
            originAddress=boxknight.Address(
                street=shipper.address_line1,
                unit=shipper.address_line2,
                city=shipper.city,
                province=units.CountryState.CA.value[shipper.state_code].value,
                country=units.Country.CA.value,
                postalCode=shipper.postal_code,
                isBusinessAddress=shipper.residential is False,
            ),
            packageCount=len(packages),
            service=service,
            notes=options.boxknight_notes.state,
            refNumber=payload.reference,
            merchantDisplayName=(
                shipper.company_name or options.boxknight_merchant_display_name.state
            ),
            signatureRequired=options.boxknight_signature_required.state,
            packages=[
                boxknight.Package(
                    refNumber=package.parcel.reference_number or str(idx),
                    weightOptions=boxknight.WeightOptions(
                        weight=package.weight.value,
                        unit=package.weight_unit.value.lower(),
                    ),
                    sizeOptions=boxknight.SizeOptions(
                        length=package.length.value,
                        width=package.width.value,
                        height=package.height.value,
                        unit=provider_units.DimensionUnit.map(
                            package.dimension_unit.value
                        ).value,
                    ),
                )
                for idx, package in enumerate(packages, start=1)
            ],
        ),
        label_type=units.LabelType.map(
            payload.label_type or "PDF"
        ).value_or_key.lower(),
    )

    return lib.Serializable(
        request,
        lambda _: {
            "order": lib.to_dict(_["order"]),
            "label_type": _["label_type"],
        },
    )
