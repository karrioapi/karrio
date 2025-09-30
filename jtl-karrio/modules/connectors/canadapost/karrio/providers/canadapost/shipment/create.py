import karrio.schemas.canadapost.shipment as canadapost
import uuid
import typing
import datetime
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.canadapost.error as provider_error
import karrio.providers.canadapost.units as provider_units
import karrio.providers.canadapost.utils as provider_utils


def parse_shipment_response(
    _responses: lib.Deserializable[typing.Tuple[lib.Element, str]],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.ShipmentDetails, typing.List[models.Message]]:
    responses = _responses.deserialize()

    shipment_details = [
        (
            f"{_}",
            (
                _extract_shipment(response, settings, _responses.ctx)
                if len(lib.find_element("shipment-id", response[0])) > 0
                else None
            ),
        )
        for _, response in enumerate(responses, start=1)
    ]

    shipment = lib.to_multi_piece_shipment(shipment_details)
    messages: typing.List[models.Message] = sum(
        [provider_error.parse_error_response(_, settings) for _, __ in responses],
        start=[],
    )

    return shipment, messages


def _extract_shipment(
    _response: typing.Tuple[lib.Element, str],
    settings: provider_utils.Settings,
    ctx: dict,
) -> models.ShipmentDetails:
    response, label = _response
    info = lib.to_object(canadapost.ShipmentInfoType, response)

    base_amount = lib.failsafe(lambda: info.shipment_price.base_amount)
    service_code = lib.failsafe(lambda: info.shipment_price.service_code)
    service = provider_units.ServiceType.map(service_code)
    adjustments = lib.failsafe(lambda: info.shipment_price.adjustments.adjustment) or []
    priced_options = lib.failsafe(lambda: info.shipment_price.priced_options.priced_option) or []
    charges = lib.failsafe(lambda: [
        ("Base charge", info.shipment_price.base_amount),
        ("GST", info.shipment_price.gst_amount),
        ("PST", info.shipment_price.pst_amount),
        ("HST", info.shipment_price.hst_amount),
        *((f"Option {o.option_code}", o.option_price) for o in priced_options),
        *((a.adjustment_code, a.adjustment_amount) for a in adjustments),
    ]) or []

    return models.ShipmentDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        tracking_number=info.tracking_pin,
        shipment_identifier=info.shipment_id,
        docs=models.Documents(label=label),
        label_type=ctx["label_type"],
        selected_rate=lib.identity(
            models.RateDetails(
                carrier_id=settings.carrier_id,
                carrier_name=settings.carrier_name,
                service=service.name_or_key,
                total_charge=lib.to_money(base_amount),
                currency="CAD",
                extra_charges=lib.identity([
                    models.ChargeDetails(name=name, amount=lib.to_money(amount), currency="CAD")
                    for name, amount in charges
                    if amount and lib.to_money(amount) != 0
                ]),
                meta=dict(
                    service_name=(service.name or service_code),
                ),
            )
            if base_amount is not None else None
        ),
        meta=lib.to_dict(
            dict(
                carrier_tracking_link=settings.tracking_url.format(info.tracking_pin),
                customer_request_ids=ctx["customer_request_ids"],
                manifest_required=ctx["manifest_required"],
                group_id=ctx["group_id"],
            )
        ),
    )


def shipment_request(
    payload: models.ShipmentRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    service = provider_units.ServiceType.map(payload.service).value_or_key
    options = lib.to_shipping_options(
        payload.options,
        is_international=(
            recipient.country_code is not None and recipient.country_code != "CA"
        ),
        initializer=provider_units.shipping_options_initializer,
    )
    packages = lib.to_packages(
        payload.parcels,
        provider_units.PackagePresets,
        required=["weight"],
        options=options,
        package_option_type=provider_units.ShippingOption,
        shipping_options_initializer=provider_units.shipping_options_initializer,
    )

    customs = lib.to_customs_info(payload.customs, weight_unit=units.WeightUnit.KG.name)
    label_encoding, label_format = provider_units.LabelType.map(
        payload.label_type or "PDF_4x6"
    ).value
    group_id = lib.fdate(datetime.datetime.now(), "%Y%m%d") + "-" + settings.carrier_id
    customer_request_ids = [f"{str(uuid.uuid4().hex)}" for _ in range(len(packages))]
    submit_shipment = lib.identity(
        #  set to true if canadapost_submit_shipment is true
        options.canadapost_submit_shipment.state
        #  default to true if transmit_shipment_by_default is true
        or (
            settings.connection_config.transmit_shipment_by_default.state
            and options.canadapost_submit_shipment.state is not False
        )
    )

    requests = [
        canadapost.ShipmentType(
            customer_request_id=customer_request_ids[index],
            groupIdOrTransmitShipment=canadapost.groupIdOrTransmitShipment(),
            quickship_label_requested=None,
            cpc_pickup_indicator=None,
            requested_shipping_point=provider_utils.format_ca_postal_code(
                shipper.postal_code
            ),
            shipping_point_id=None,
            expected_mailing_date=options.shipment_date.state,
            provide_pricing_info=True,
            provide_receipt_info=None,
            delivery_spec=canadapost.DeliverySpecType(
                service_code=service,
                sender=canadapost.SenderType(
                    name=shipper.person_name,
                    company=(shipper.company_name or "Not Applicable"),
                    contact_phone=(shipper.phone_number or "000 000 0000"),
                    address_details=canadapost.AddressDetailsType(
                        city=shipper.city,
                        prov_state=shipper.state_code,
                        country_code=shipper.country_code,
                        postal_zip_code=provider_utils.format_ca_postal_code(
                            shipper.postal_code
                        ),
                        address_line_1=shipper.street,
                        address_line_2=lib.text(shipper.address_line2),
                    ),
                ),
                destination=canadapost.DestinationType(
                    name=recipient.person_name,
                    company=recipient.company_name,
                    additional_address_info=None,
                    client_voice_number=recipient.phone_number or "000 000 0000",
                    address_details=canadapost.DestinationAddressDetailsType(
                        city=recipient.city,
                        prov_state=recipient.state_code,
                        country_code=recipient.country_code,
                        postal_zip_code=provider_utils.format_ca_postal_code(
                            recipient.postal_code
                        ),
                        address_line_1=recipient.street,
                        address_line_2=lib.text(recipient.address_line2),
                    ),
                ),
                parcel_characteristics=canadapost.ParcelCharacteristicsType(
                    weight=package.weight.map(provider_units.MeasurementOptions).KG,
                    dimensions=canadapost.dimensionsType(
                        length=package.length.map(provider_units.MeasurementOptions).CM,
                        width=package.width.map(provider_units.MeasurementOptions).CM,
                        height=package.height.map(provider_units.MeasurementOptions).CM,
                    ),
                    unpackaged=None,
                    mailing_tube=None,
                ),
                options=(
                    canadapost.optionsType(
                        option=[
                            canadapost.OptionType(
                                option_code=option.code,
                                option_amount=lib.to_money(option.state),
                                option_qualifier_1=None,
                                option_qualifier_2=None,
                            )
                            for _, option in package.options.items()
                            if option.state is not False
                        ]
                    )
                    if any(
                        [
                            option
                            for _, option in package.options.items()
                            if option.state is not False
                        ]
                    )
                    else None
                ),
                notification=(
                    canadapost.NotificationType(
                        email=(
                            package.options.email_notification_to.state
                            or recipient.email
                        ),
                        on_shipment=True,
                        on_exception=True,
                        on_delivery=True,
                    )
                    if package.options.email_notification.state
                    and any(
                        [package.options.email_notification_to.state, recipient.email]
                    )
                    else None
                ),
                print_preferences=canadapost.PrintPreferencesType(
                    output_format=label_format,
                    encoding=label_encoding,
                ),
                preferences=canadapost.PreferencesType(
                    service_code=None,
                    show_packing_instructions=False,
                    show_postage_rate=True,
                    show_insured_value=True,
                ),
                customs=(
                    canadapost.CustomsType(
                        currency=(options.currency.state or units.Currency.CAD.name),
                        conversion_from_cad=None,
                        reason_for_export="OTH",
                        other_reason=customs.content_type,
                        duties_and_taxes_prepaid=customs.duty.account_number,
                        certificate_number=customs.options.certificate_number.state,
                        licence_number=lib.text(
                            customs.options.license_number.state, max=10
                        ),
                        invoice_number=lib.text(customs.invoice, max=10),
                        sku_list=(
                            (
                                canadapost.sku_listType(
                                    item=[
                                        canadapost.SkuType(
                                            customs_number_of_units=item.quantity,
                                            customs_description=lib.text(
                                                item.title
                                                or item.description
                                                or item.sku
                                                or "N/B",
                                                max=35,
                                            ),
                                            sku=item.sku or "0000",
                                            hs_tariff_code=item.hs_code,
                                            unit_weight=(item.weight or 1),
                                            customs_value_per_unit=item.value_amount,
                                            customs_unit_of_measure=None,
                                            country_of_origin=(
                                                item.origin_country
                                                or shipper.country_code
                                            ),
                                            province_of_origin=shipper.state_code
                                            or "N/B",
                                        )
                                        for item in customs.commodities
                                    ]
                                )
                            )
                            if any(customs.commodities or [])
                            else None
                        ),
                    )
                    if payload.customs is not None
                    else None
                ),
                references=canadapost.ReferencesType(
                    cost_centre=(
                        options.canadapost_cost_center.state
                        or settings.connection_config.cost_center.state
                        or payload.reference
                    ),
                    customer_ref_1=payload.reference,
                    customer_ref_2=None,
                ),
                settlement_info=canadapost.SettlementInfoType(
                    paid_by_customer=getattr(
                        payload.payment, "account_number", settings.customer_number
                    ),
                    contract_id=settings.contract_id,
                    cif_shipment=None,
                    intended_method_of_payment=provider_units.PaymentType.map(
                        getattr(payload.payment, "paid_by", None)
                    ).value,
                    promo_code=None,
                ),
            ),
            return_spec=None,
            pre_authorized_payment=None,
            create_qr_code=None,
        )
        for index, package in enumerate(packages)
    ]

    return lib.Serializable(
        requests,
        lambda __: [
            lib.to_xml(
                request,
                name_="shipment",
                namespacedef_='xmlns="http://www.canadapost.ca/ws/shipment-v8"',
            ).replace(
                "<groupIdOrTransmitShipment/>",
                (
                    "<transmit-shipment/>"
                    if submit_shipment
                    else f"<group-id>{group_id}</group-id>"
                ),
            )
            for request in __
        ],
        dict(
            label_type=label_encoding,
            manifest_required=(not submit_shipment),
            customer_request_ids=customer_request_ids,
            group_id=(None if submit_shipment else group_id),
        ),
    )
