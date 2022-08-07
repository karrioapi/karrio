from canadapost_lib.ncshipment import (
    NonContractShipmentType,
    NonContractShipmentInfoType,
    DeliverySpecType,
    SenderType,
    DomesticAddressDetailsType,
    DestinationType,
    DestinationAddressDetailsType,
    ParcelCharacteristicsType,
    optionsType,
    ReferencesType,
    NotificationType,
    sku_listType,
    SkuType,
    dimensionsType,
    OptionType,
    CustomsType,
    PreferencesType,
)
import typing
import karrio.lib as lib
import karrio.core.units as units
import karrio.core.models as models
import karrio.providers.canadapost.error as provider_error
import karrio.providers.canadapost.units as provider_units
import karrio.providers.canadapost.utils as provider_utils


def parse_shipment_response(
    response: lib.Element, settings: provider_utils.Settings
) -> typing.Tuple[models.ShipmentDetails, typing.List[models.Message]]:
    shipment = (
        _extract_shipment(response, settings)
        if len(response.xpath(".//*[local-name() = $name]", name="shipment-id")) > 0
        else None
    )
    return shipment, provider_error.parse_error_response(response, settings)


def _extract_shipment(
    response: lib.Element, settings: provider_utils.Settings
) -> models.ShipmentDetails:
    info_node = next(
        iter(response.xpath(".//*[local-name() = $name]", name="shipment-info"))
    )
    label_node = next(iter(response.xpath(".//*[local-name() = $name]", name="label")))
    errors = provider_error.parse_error_response(label_node, settings)
    label = str(label_node.text) if len(errors) == 0 else None
    info: NonContractShipmentInfoType = NonContractShipmentInfoType()
    info.build(info_node)

    return models.ShipmentDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        tracking_number=info.tracking_pin,
        shipment_identifier=info.tracking_pin,
        docs=models.Documents(label=label),
    )


def shipment_request(
    payload: models.ShipmentRequest, _
) -> lib.Serializable[NonContractShipmentType]:
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
            payload.recipient.country_code is not None
            and payload.recipient.country_code != "CA"
        ),
        initializer=provider_units.shipping_options_initializer,
    )

    request = NonContractShipmentType(
        requested_shipping_point=None,
        delivery_spec=DeliverySpecType(
            service_code=service,
            sender=SenderType(
                name=payload.shipper.person_name,
                company=payload.shipper.company_name,
                contact_phone=payload.shipper.phone_number,
                address_details=DomesticAddressDetailsType(
                    address_line_1=lib.join(payload.shipper.address_line1, join=True),
                    address_line_2=lib.join(payload.shipper.address_line2, join=True),
                    city=payload.shipper.city,
                    prov_state=payload.shipper.state_code,
                    postal_zip_code=provider_utils.format_ca_postal_code(
                        payload.shipper.postal_code
                    ),
                ),
            ),
            destination=DestinationType(
                name=payload.recipient.person_name,
                company=payload.recipient.company_name,
                additional_address_info=None,
                client_voice_number=payload.recipient.phone_number,
                address_details=DestinationAddressDetailsType(
                    address_line_1=lib.join(payload.recipient.address_line1, join=True),
                    address_line_2=lib.join(payload.recipient.address_line2, join=True),
                    city=payload.recipient.city,
                    prov_state=payload.recipient.state_code,
                    country_code=payload.recipient.country_code,
                    postal_zip_code=provider_utils.format_ca_postal_code(
                        payload.recipient.postal_code
                    ),
                ),
            ),
            options=(
                optionsType(
                    option=[
                        OptionType(
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
            parcel_characteristics=ParcelCharacteristicsType(
                weight=lib.to_decimal(package.weight.KG, 0.1),
                dimensions=dimensionsType(
                    length=lib.to_decimal(package.length.CM, 0.1),
                    width=lib.to_decimal(package.width.CM, 0.1),
                    height=lib.to_decimal(package.height.CM, 0.1),
                ),
                unpackaged=None,
                mailing_tube=None,
            ),
            notification=(
                NotificationType(
                    email=options.notification_email.state or payload.recipient.email,
                    on_shipment=True,
                    on_exception=True,
                    on_delivery=True,
                )
                if any([options.notification_email.state, payload.recipient.email])
                else None
            ),
            preferences=PreferencesType(
                show_packing_instructions=False,
                show_postage_rate=True,
                show_insured_value=True,
            ),
            references=ReferencesType(
                cost_centre=options.canadapost_cost_center.state or payload.reference,
                customer_ref_1=payload.reference,
                customer_ref_2=None,
            ),
            customs=(
                CustomsType(
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
                    sku_list=sku_listType(
                        item=[
                            SkuType(
                                customs_number_of_units=item.quantity,
                                customs_description=item.description,
                                sku=item.sku,
                                hs_tariff_code=item.hs_code,
                                unit_weight=units.WeightUnit.KG.value,
                                customs_value_per_unit=item.value_amount,
                                customs_unit_of_measure=None,
                                country_of_origin=payload.shipper.country_code,
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


def _request_serializer(request: NonContractShipmentType) -> str:
    return lib.to_xml(
        request,
        name_="non-contract-shipment",
        namespacedef_='xmlns="http://www.canadapost.ca/ws/ncshipment-v4"',
    )
