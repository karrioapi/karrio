import canadapost_lib.ncshipment as canadapost
import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.canadapost.error as provider_error
import karrio.providers.canadapost.units as provider_units
import karrio.providers.canadapost.utils as provider_utils


def parse_shipment_response(
    _response: lib.Deserializable[lib.Element],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.ShipmentDetails, typing.List[models.Message]]:
    response = _response.deserialize()
    shipment = (
        _extract_shipment(response, settings)
        if len(lib.find_element("shipment-id", response)) > 0
        else None
    )
    return shipment, provider_error.parse_error_response(response, settings)


def _extract_shipment(
    response: lib.Element, settings: provider_utils.Settings
) -> models.ShipmentDetails:
    info_node = lib.find_element(response, "shipment-info", first=True)
    label_node = lib.find_element(response, "label", first=True)

    errors = provider_error.parse_error_response(label_node, settings)
    label = str(label_node.text) if len(errors) == 0 else None
    info = lib.to_object(canadapost.NonContractShipmentInfoType, info_node)

    return models.ShipmentDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        tracking_number=info.tracking_pin,
        shipment_identifier=info.tracking_pin,
        docs=models.Documents(label=label),
        meta=dict(
            carrier_tracking_link=settings.tracking_url.format(info.tracking_pin),
        ),
    )


def shipment_request(payload: models.ShipmentRequest, _) -> lib.Serializable:
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    service = provider_units.ServiceType.map(payload.service).value_or_key
    customs = lib.to_customs_info(payload.customs)
    package = lib.to_packages(
        payload.parcels,
        provider_units.PackagePresets,
        required=["weight"],
        package_option_type=provider_units.ShippingOption,
    ).single
    options = lib.to_shipping_options(
        options=payload.options,
        package_options=package.options,
        is_international=(
            recipient.country_code is not None and recipient.country_code != "CA"
        ),
        initializer=provider_units.shipping_options_initializer,
    )

    request = canadapost.NonContractShipmentType(
        requested_shipping_point=None,
        delivery_spec=canadapost.DeliverySpecType(
            service_code=service,
            sender=canadapost.SenderType(
                name=shipper.person_name,
                company=shipper.company_name,
                contact_phone=shipper.phone_number,
                address_details=canadapost.DomesticAddressDetailsType(
                    address_line_1=shipper.street,
                    address_line_2=lib.text(shipper.address_line2),
                    city=shipper.city,
                    prov_state=shipper.state_code,
                    postal_zip_code=provider_utils.format_ca_postal_code(
                        shipper.postal_code
                    ),
                ),
            ),
            destination=canadapost.DestinationType(
                name=recipient.person_name,
                company=recipient.company_name,
                additional_address_info=None,
                client_voice_number=recipient.phone_number,
                address_details=canadapost.DestinationAddressDetailsType(
                    address_line_1=recipient.street,
                    address_line_2=lib.text(recipient.address_line2),
                    city=recipient.city,
                    prov_state=recipient.state_code,
                    country_code=recipient.country_code,
                    postal_zip_code=provider_utils.format_ca_postal_code(
                        recipient.postal_code
                    ),
                ),
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
                        for _, option in options.items()
                    ]
                )
                if any(options.items())
                else None
            ),
            parcel_characteristics=canadapost.ParcelCharacteristicsType(
                weight=lib.to_decimal(package.weight.KG, 0.1),
                dimensions=canadapost.dimensionsType(
                    length=lib.to_decimal(package.length.CM, 0.1),
                    width=lib.to_decimal(package.width.CM, 0.1),
                    height=lib.to_decimal(package.height.CM, 0.1),
                ),
                unpackaged=None,
                mailing_tube=None,
            ),
            notification=(
                canadapost.NotificationType(
                    email=options.notification_email.state or recipient.email,
                    on_shipment=True,
                    on_exception=True,
                    on_delivery=True,
                )
                if any([options.notification_email.state, recipient.email])
                else None
            ),
            preferences=canadapost.PreferencesType(
                show_packing_instructions=False,
                show_postage_rate=True,
                show_insured_value=True,
            ),
            references=canadapost.ReferencesType(
                cost_centre=options.canadapost_cost_center.state or payload.reference,
                customer_ref_1=payload.reference,
                customer_ref_2=None,
            ),
            customs=(
                canadapost.CustomsType(
                    currency=units.Currency.AUD.value,
                    conversion_from_cad=None,
                    reason_for_export=customs.incoterm,
                    other_reason=customs.content_description,
                    duties_and_taxes_prepaid=getattr(
                        customs.duty, "account_number", None
                    ),
                    certificate_number=customs.options.certificate_number.state,
                    licence_number=customs.options.licence_number.state,
                    invoice_number=customs.invoice,
                    sku_list=canadapost.sku_listType(
                        item=[
                            canadapost.SkuType(
                                customs_number_of_units=item.quantity,
                                customs_description=lib.text(
                                    item.title or item.description, max=35
                                ),
                                sku=item.sku,
                                hs_tariff_code=item.hs_code,
                                unit_weight=units.WeightUnit.KG.value,
                                customs_value_per_unit=item.value_amount,
                                customs_unit_of_measure=None,
                                country_of_origin=shipper.country_code,
                                province_of_origin=None,
                            )
                            for item in customs.commodities or []
                        ]
                    ),
                )
                if customs.is_defined
                else None
            ),
            settlement_info=None,
        ),
    )
    return lib.Serializable(request, _request_serializer)


def _request_serializer(request: canadapost.NonContractShipmentType) -> str:
    return lib.to_xml(
        request,
        name_="non-contract-shipment",
        namespacedef_='xmlns="http://www.canadapost.ca/ws/ncshipment-v4"',
    )
