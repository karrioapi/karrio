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
    [shipment_response, label_response, label] = _response.deserialize()
    shipments = shipment_response.get("shipments") or []
    labels = label_response.get("labels") or []
    messages = [
        *error.parse_error_response(label_response, settings),
        *error.parse_error_response(shipment_response, settings),
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
    [shipment_response, label_response, label] = data
    label_format = ctx.get("label_format") or "PDF"
    label_info = lib.to_object(labels.LabelType, label_response)
    shipment = lib.to_object(shipping.ShipmentType, shipment_response)
    article_ids = [item.tracking_details.article_id for item in shipment.items]
    tracking_numbers = [item.tracking_details.consignment_id for item in shipment.items]

    return models.ShipmentDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=tracking_numbers[0],
        shipment_identifier=shipment.shipment_id,
        label_type=label_format,
        docs=models.Documents(label=label),
        meta=dict(
            carrier_tracking_link=settings.tracking_url.format(tracking_numbers[0]),
            label_request_id=label_info.request_id,
            tracking_numbers=tracking_numbers,
            article_ids=article_ids,
            manifest_required=True,
        ),
    )


def shipment_request(
    payload: models.ShipmentRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    service = provider_units.ShippingService.map(payload.service)
    is_intl = shipper.country_code != recipient.country_code
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
    customs = lib.to_customs_info(payload.customs, weight_unit=units.WeightUnit.KG.name)
    label_format, label_layout = provider_units.LabelType.map(
        payload.label_type or "PDF"
    ).value
    label_group = (
        provider_units.ServiceLabelGroup.map(service.name).value
        or provider_units.ServiceLabelGroup.australiapost_parcel_post.value
    )

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
                        state=shipper.state_code,
                        postcode=shipper.postal_code,
                        country=shipper.country_code,
                        email=shipper.email,
                        phone=shipper.phone_number,
                    ),
                    to=australiapost.FromType(
                        name=recipient.contact,
                        lines=recipient.address_lines,
                        suburb=recipient.city,
                        state=recipient.state_code,
                        postcode=recipient.postal_code,
                        country=recipient.country_code,
                        email=recipient.email,
                        phone=recipient.phone_number,
                    ),
                    items=[
                        australiapost.ItemType(
                            item_reference=getattr(package, "id", None) or str(idx),
                            product_id=service.value_or_key,
                            length=package.length.CM,
                            width=package.width.CM,
                            height=package.height.CM,
                            weight=package.weight.KG,
                            cubic_volume=None,
                            transportable_by_air=package.options.transportable_by_air.state,
                            authority_to_leave=package.options.australiapost_authority_to_leave.state,
                            allow_partial_delivery=package.options.australiapost_allow_partial_delivery.state,
                            contains_dangerous_goods=package.options.australiapost_contains_dangerous_goods.state,
                            item_description=package.parcel.description,
                            features=(
                                australiapost.FeaturesType(
                                    DELIVERY_DATE=(
                                        australiapost.DELIVERYDATEAttributesType(
                                            date=package.options.australiapost_delivery_date.state,
                                        )
                                        if package.options.australiapost_delivery_date.state
                                        else None
                                    ),
                                    DELIVERY_TIMES=(
                                        australiapost.DELIVERYTIMESAttributesType(
                                            windows=australiapost.WindowType(
                                                start=package.options.australiapost_delivery_time_start.state,
                                                end=package.options.australiapost_delivery_time_end.state,
                                            )
                                        )
                                        if any(
                                            [
                                                package.options.australiapost_delivery_time_start.state,
                                                package.options.australiapost_delivery_time_end.state,
                                            ]
                                        )
                                        else None
                                    ),
                                    PICKUP_DATE=(
                                        australiapost.DateType(
                                            attributes=australiapost.DELIVERYDATEAttributesType(
                                                date=package.options.australiapost_pickup_date.state,
                                            )
                                        )
                                        if package.options.australiapost_pickup_date.state
                                        else None
                                    ),
                                    PICKUP_TIME=(
                                        australiapost.PickupTimeType(
                                            attributes=australiapost.PICKUPTIMEAttributesType(
                                                time=package.options.australiapost_pickup_time.state,
                                            )
                                        )
                                        if package.options.australiapost_pickup_time.state
                                        else None
                                    ),
                                    IDENTITY_ON_DELIVERY=(
                                        australiapost.IdentityOnDeliveryType(
                                            attributes=australiapost.IDENTITYONDELIVERYAttributesType(
                                                id_capture_type=package.options.australiapost_identity_on_delivery.state,
                                                redirection_enabled=None,
                                            )
                                        )
                                        if package.options.australiapost_identity_on_delivery.state
                                        else None
                                    ),
                                    PRINT_AT_DEPOT=(
                                        australiapost.PrintAtDepotType(
                                            attributes=australiapost.PRINTATDEPOTAttributesType(
                                                enabled=package.options.australiapost_print_at_depot.state,
                                            )
                                        )
                                        if package.options.australiapost_print_at_depot.state
                                        else None
                                    ),
                                    SAMEDAY_IDENTITY_ON_DELIVERY=(
                                        australiapost.SamedayIdentityOnDeliveryType(
                                            attributes=australiapost.SAMEDAYIDENTITYONDELIVERYAttributesType(
                                                id_option=package.options.australiapost_sameday_identity_on_delivery.state,
                                            )
                                        )
                                        if package.options.australiapost_sameday_identity_on_delivery.state
                                        else None
                                    ),
                                    COMMERCIAL_CLEARANCE=(
                                        australiapost.CommercialClearanceType()
                                        if payload.customs
                                        else None
                                    ),
                                )
                                if any(
                                    [
                                        package.options.australiapost_delivery_date.state,
                                        package.options.australiapost_delivery_time_start.state,
                                        package.options.australiapost_delivery_time_end.state,
                                        package.options.australiapost_pickup_date.state,
                                        package.options.australiapost_pickup_time.state,
                                        package.options.australiapost_identity_on_delivery.state,
                                        package.options.australiapost_print_at_depot.state,
                                        package.options.australiapost_sameday_identity_on_delivery.state,
                                        payload.customs,
                                    ]
                                )
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
                            export_declaration_number=customs.options.export_declaration_number.state,
                            import_reference_number=customs.options.import_reference_number.state,
                            item_contents=(
                                [
                                    australiapost.ItemContentType(
                                        country_of_origin=content.country,
                                        description=content.description,
                                        sku=content.sku,
                                        quantity=content.quantity,
                                        tariff_code=content.hs_code,
                                        value=content.value_amount,
                                        weight=content.weight,
                                        item_contents_reference=None,
                                    )
                                    for content in (
                                        package.items
                                        if any(package.items)
                                        else customs.commodities
                                    )
                                ]
                                if is_intl
                                else []
                            ),
                        )
                        for idx, package in enumerate(packages, start=1)
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
                    format=label_format,
                    groups=[
                        label_request.GroupType(
                            group=label_group,
                            layout=label_layout,
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
        dict(label_format=label_format),
    )
