import karrio.schemas.australiapost.shipment_request as australiapost
import karrio.schemas.australiapost.shipment_response as shipping
import karrio.schemas.australiapost.label_request as label_request
import karrio.schemas.australiapost.label_response as labels
import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.australiapost.error as error
import karrio.providers.australiapost.utils as provider_utils
import karrio.providers.australiapost.units as provider_units


def parse_shipment_response(
    _response: lib.Deserializable[
        typing.Tuple[dict, typing.Optional[dict], typing.Optional[str]]
    ],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.RateDetails], typing.List[models.Message]]:
    [response, label_response, label] = _response.deserialize()
    shipments = response.get("shipments") or []
    labels = label_response.get("labels") or []
    messages = [
        *error.parse_error_response(response, settings),
        *error.parse_error_response(label_response, settings),
    ]
    shipment = (
        _extract_details((shipments[0], labels[0], label), settings)
        if label is not None
        else None
    )

    return shipment, messages


def _extract_details(
    data: typing.Tuple[dict, dict, str],
    settings: provider_utils.Settings,
    ctx: dict = {},
) -> models.ShipmentDetails:
    [response, label_response, label] = data
    shipment = lib.to_object(shipping.ShipmentType, response)
    label_info = lib.to_object(labels.LabelType, label_response)
    tracking_numbers = [item.tracking_details.consignment_id for item in shipment.items]

    return models.ShipmentDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=tracking_numbers[0],
        shipment_identifier=shipment.shipment_id,
        label_type=ctx["label_type"],
        docs=models.Documents(label=label),
        meta=dict(
            carrier_tracking_link=settings.tracking_url.format(tracking_numbers[0]),
            label_request_id=label_info.request_id,
            tracking_numbers=tracking_numbers,
        ),
    )


def shipment_request(
    payload: models.ShipmentRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(recipient)
    service = provider_units.ShippingService.map(payload.service).value_or_key
    options = lib.to_shipping_options(
        payload.options,
        package_options=packages.options,
        option_type=provider_units.ShippingOption,
    )
    packages = lib.to_packages(
        payload.parcels,
        options=options,
        package_option_type=provider_units.PackagingType,
    )
    customs = lib.to_customs(payload.customs)
    label_type = provider_units.LabelType.map(payload.label_type or "PDF").value

    request = dict(
        shipment=australiapost.ShipmentRequestType(
            shipments=[
                australiapost.ShipmentType(
                    shipment_reference=payload.reference,
                    customer_reference_1=None,
                    customer_reference_2=None,
                    email_tracking_enabled=options.email_notification.state,
                    shipment_from=australiapost.FromType(
                        name=shipper.contact,
                        lines=shipper.address_lines,
                        suburb=shipper.city,
                        state=shipper.state,
                        postcode=shipper.postal_code,
                        country=shipper.country,
                        email=shipper.email,
                        phone=shipper.phone,
                    ),
                    to=australiapost.FromType(
                        name=recipient.contact,
                        lines=recipient.address_lines,
                        suburb=recipient.city,
                        state=recipient.state,
                        postcode=recipient.postal_code,
                        country=recipient.country,
                        email=recipient.email,
                        phone=recipient.phone,
                    ),
                    items=[
                        australiapost.ItemType(
                            item_reference=package.reference,
                            product_id=service,
                            length=package.length.CM,
                            width=package.width.CM,
                            height=package.height.CM,
                            weight=package.weight.KG,
                            cubic_volume=package.volume.m3,
                            authority_to_leave=package.options.authority_to_leave.state,
                            allow_partial_delivery=package.options.allow_partial_delivery.state,
                            contains_dangerous_goods=package.options.contains_dangerous_goods.state,
                            item_description=package.parcel.description,
                            features=(
                                {
                                    [option.code]: australiapost.FeatureType(
                                        attributes=australiapost.AttributesType(
                                            cover_amount=option.value,
                                        ),
                                    )
                                    for option in package.options
                                }
                                if any(package.options)
                                else None
                            ),
                            classification_type=(
                                # fmt: off
                                provider_units.ContentType.map(customs.content_type).value or "OTHER" 
                                if payload.customs 
                                else None
                                # fmt: on
                            ),
                            commercial_value=customs.commercial_invoice,
                            description_of_other=customs.content_description,
                            export_declaration_number=customs.options.export_declaration_number.value,
                            import_reference_number=customs.options.import_reference_number.value,
                            item_contents=[
                                australiapost.ItemContentType(
                                    country_of_origin=content.country,
                                    description=content.description,
                                    sku=content.sku,
                                    quantity=content.quantity,
                                    tariff_code=content.hs_code,
                                    value=content.value_amount,
                                    weight=content.weight.KG,
                                    item_contents_reference=None,
                                )
                                for content in (
                                    package.items
                                    if any(package.items)
                                    else customs.commodities
                                )
                            ],
                        )
                        for package in packages
                    ],
                    movement_type="DESPATCH",
                )
            ]
        ),
        label=label_request.LabelRequestType(
            wait_for_label_url=True,
            preferences=[
                label_request.PreferenceType(
                    type="PRINT",
                    format=label_type,
                    groups=[
                        label_request.GroupType(
                            group=service,
                            layout="A4-1pp",
                            branded=True,
                            left_offset=0,
                            top_offset=0,
                        )
                    ],
                )
            ],
            shipments=[label_request.ShipmentType(shipment_id="[SHIPMENT_ID]")],
        ),
    )

    return lib.Serializable(
        request,
        lambda _: dict(
            shipment=lib.to_dict(
                lib.to_json(_["shipment"]).replace("shipment_from", "from")
            ),
            label=lib.to_dict(_["label"]),
        ),
        dict(label_type=label_type),
    )
