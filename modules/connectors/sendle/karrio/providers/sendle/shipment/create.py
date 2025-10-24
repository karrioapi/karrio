import karrio.schemas.sendle.order_request as sendle
import karrio.schemas.sendle.order_response as shipping
import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.sendle.error as provider_error
import karrio.providers.sendle.utils as provider_utils
import karrio.providers.sendle.units as provider_units


def parse_shipment_response(
    _responses: lib.Deserializable[typing.List[typing.Tuple[dict, dict]]],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.RateDetails], typing.List[models.Message]]:
    responses = _responses.deserialize()

    shipment = lib.to_multi_piece_shipment(
        [
            (
                f"{_}",
                (
                    _extract_details(response, settings)
                    if response[0].get("error") is None
                    else None
                ),
            )
            for _, response in enumerate(responses, start=1)
        ]
    )
    messages: typing.List[models.Message] = sum(
        [
            provider_error.parse_error_response(list(response), settings)
            for response in responses
        ],
        start=[],
    )

    return shipment, messages


def _extract_details(
    data: typing.Tuple[dict, dict],
    settings: provider_utils.Settings,
) -> models.ShipmentDetails:
    details, label = data
    order: shipping.OrderResponseType = lib.to_object(
        shipping.OrderResponseType, details
    )

    return models.ShipmentDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=order.sendle_reference,
        shipment_identifier=order.order_id,
        label_type="PDF",
        docs=models.Documents(label=label["label"]),
        meta=dict(
            carrier_tracking_link=order.tracking_url,
            customer_reference=order.customer_reference,
            order_url=order.order_url,
            order_id=order.order_id,
            metadata=order.metadata,
            shipment_identifiers=[order.order_id],
            tracking_numbers=[order.sendle_reference],
        ),
    )


def shipment_request(
    payload: models.ShipmentRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    service = provider_units.ShippingService.map(payload.service).value_or_key
    is_international = payload.recipient.country_code != payload.shipper.country_code
    options = lib.to_shipping_options(
        payload.options,
        option_type=provider_units.ShippingOption,
    )
    packages = lib.to_packages(
        payload.parcels,
        options=options,
        package_option_type=provider_units.ShippingOption,
        shipping_options_initializer=provider_units.shipping_options_initializer,
    )
    customs = lib.to_customs_info(
        payload.customs,
        shipper=shipper,
        recipient=recipient,
        weight_unit=units.WeightUnit.KG.name,
    )

    request = [
        sendle.OrderRequestType(
            sender=sendle.ReceiverType(
                address=sendle.AddressType(
                    country=shipper.country_code,
                    address_line1=shipper.address_line1,
                    address_line2=shipper.address_line2,
                    suburb=shipper.city,
                    postcode=shipper.postal_code,
                    state_name=shipper.state_code,
                ),
                contact=sendle.ContactType(
                    name=shipper.person_name,
                    email=shipper.email,
                    phone=shipper.phone,
                    company=shipper.company_name,
                ),
                instructions=package.options.instructions.state,
                tax_ids=(
                    sendle.TaxIDSType(ioss=shipper.tax_id) if shipper.tax_id else None
                ),
            ),
            receiver=sendle.ReceiverType(
                address=sendle.AddressType(
                    country=recipient.country_code,
                    address_line1=recipient.address_line1,
                    address_line2=recipient.address_line2,
                    suburb=recipient.city,
                    postcode=recipient.postal_code,
                    state_name=recipient.state_code,
                ),
                contact=sendle.ContactType(
                    name=recipient.person_name,
                    email=recipient.email,
                    phone=recipient.phone,
                    company=recipient.company_name,
                ),
                instructions=None,
                tax_ids=(
                    sendle.TaxIDSType(ioss=recipient.tax_id)
                    if recipient.tax_id
                    else None
                ),
            ),
            description=package.parcel.description,
            customer_reference=payload.reference,
            product_code=service,
            first_mile_option=package.options.sendle_first_mile_option.state,
            pickup_date=lib.fdate(package.options.shipment_date.state),
            weight=sendle.VolumeType(
                units=units.WeightUnit.KG.value,
                value=package.weight.KG,
            ),
            volume=sendle.VolumeType(
                units=units.VolumeUnit.m3.value,
                value=package.volume.m3,
            ),
            dimensions=sendle.DimensionsType(
                units=units.DimensionUnit.CM.value,
                width=package.width.CM,
                length=package.length.CM,
                height=package.height.CM,
            ),
            metadata=getattr(payload, "metadata", None),
            hide_pickup_address=package.options.sendle_hide_pickup_address.state,
            parcel_contents=(
                [
                    sendle.ParcelContentType(
                        description=(item.title or item.description),
                        value=str(item.value_amout),
                        currency=package.options.currency.state,
                        quantity=item.quantity,
                        country_of_origin=(item.origin_country or shipper.country_code),
                        hs_code=(item.hs_code or item.sku),
                    )
                    for item in (
                        package.items if any(package.items) else customs.commodities
                    )
                ]
                if is_international
                else []
            ),
        )
        for package in packages
    ]

    return lib.Serializable(request, lib.to_dict)
