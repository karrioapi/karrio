from typing import Tuple, List, Any
from canadapost_lib.shipment import (
    ShipmentType,
    ShipmentInfoType,
    DeliverySpecType,
    SenderType,
    AddressDetailsType,
    DestinationType,
    DestinationAddressDetailsType,
    ParcelCharacteristicsType,
    optionsType,
    ReferencesType,
    NotificationType,
    PrintPreferencesType,
    sku_listType,
    SkuType,
    dimensionsType,
    OptionType,
    CustomsType,
    PreferencesType,
    SettlementInfoType,
    groupIdOrTransmitShipment,
)
from purplship.core.units import Currency, WeightUnit, Options, Packages
from purplship.core.utils import Serializable, Element, XP, SF, NF
from purplship.core.models import (
    Message,
    ShipmentDetails,
    ShipmentRequest,
)
from purplship.providers.canadapost.error import parse_error_response
from purplship.providers.canadapost.units import (
    OptionCode,
    ServiceType,
    PackagePresets,
    PaymentType,
    LabelType,
    INTERNATIONAL_NON_DELIVERY_OPTION,
    MeasurementOptions,
)
from purplship.providers.canadapost.utils import Settings


def parse_shipment_response(
    response: Element, settings: Settings
) -> Tuple[ShipmentDetails, List[Message]]:
    shipment = (
        _extract_shipment(response, settings)
        if len(response.xpath(".//*[local-name() = $name]", name="shipment-id")) > 0
        else None
    )
    return shipment, parse_error_response(response, settings)


def _extract_shipment(response: Element, settings: Settings) -> ShipmentDetails:
    info_node = next(
        iter(response.xpath(".//*[local-name() = $name]", name="shipment-info"))
    )
    label = next(iter(response.xpath(".//*[local-name() = $name]", name="label")))
    errors = parse_error_response(label, settings)
    info: ShipmentInfoType = ShipmentInfoType()
    info.build(info_node)

    return ShipmentDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        tracking_number=info.tracking_pin,
        shipment_identifier=info.tracking_pin,
        label=str(label.text) if len(errors) == 0 else None
    )


def shipment_request(
    payload: ShipmentRequest, settings: Settings
) -> Serializable[ShipmentType]:
    package = Packages(payload.parcels, PackagePresets, required=['weight']).single
    service = ServiceType[payload.service].value
    options = Options(payload.options, OptionCode)

    is_intl = (
        payload.recipient.country_code is not None and
        payload.recipient.country_code != 'CA'
    )
    payment_type = (
        PaymentType[payload.payment.paid_by].value
        if payload.payment is not None else None
    )
    all_options = (
        [*options, (OptionCode.canadapost_return_to_sender.name, OptionCode.canadapost_return_to_sender.value.apply(True))]
        if is_intl and not any(key in options for key in INTERNATIONAL_NON_DELIVERY_OPTION)
        else [*options]
    )

    label_encoding, label_format = LabelType[payload.label_type or 'PDF_4x6'].value

    request = ShipmentType(
        customer_request_id=None,
        groupIdOrTransmitShipment=groupIdOrTransmitShipment(),
        quickship_label_requested=None,
        cpc_pickup_indicator=None,
        requested_shipping_point=payload.shipper.postal_code,
        shipping_point_id=None,
        expected_mailing_date=options.shipment_date,
        provide_pricing_info=True,
        provide_receipt_info=None,
        delivery_spec=DeliverySpecType(
            service_code=service,
            sender=SenderType(
                name=payload.shipper.person_name,
                company=payload.shipper.company_name or "Not Applicable",
                contact_phone=payload.shipper.phone_number,
                address_details=AddressDetailsType(
                    city=payload.shipper.city,
                    prov_state=payload.shipper.state_code,
                    country_code=payload.shipper.country_code,
                    postal_zip_code=payload.shipper.postal_code,
                    address_line_1=SF.concat_str(payload.shipper.address_line1, join=True),
                    address_line_2=SF.concat_str(payload.shipper.address_line2, join=True),
                ),
            ),
            destination=DestinationType(
                name=payload.recipient.person_name,
                company=payload.recipient.company_name,
                additional_address_info=None,
                client_voice_number=payload.recipient.phone_number,
                address_details=DestinationAddressDetailsType(
                    city=payload.recipient.city,
                    prov_state=payload.recipient.state_code,
                    country_code=payload.recipient.country_code,
                    postal_zip_code=payload.recipient.postal_code,
                    address_line_1=SF.concat_str(
                        payload.recipient.address_line1, join=True
                    ),
                    address_line_2=SF.concat_str(
                        payload.recipient.address_line2, join=True
                    ),
                ),
            ),
            parcel_characteristics=ParcelCharacteristicsType(
                weight=package.weight.map(MeasurementOptions).KG,
                dimensions=dimensionsType(
                    length=package.length.map(MeasurementOptions).CM,
                    width=package.width.map(MeasurementOptions).CM,
                    height=package.height.map(MeasurementOptions).CM,
                ),
                unpackaged=None,
                mailing_tube=None,
            ),
            options=(
                optionsType(
                    option=[
                        OptionType(
                            option_code=getattr(option, 'key', option),
                            option_amount=getattr(option, 'value', None),
                            option_qualifier_1=None,
                            option_qualifier_2=None,
                        )
                        for code, option in all_options if code in OptionCode
                    ]
                )
                if any(all_options) else None
            ),
            notification=(
                NotificationType(
                    email=options.notification_email or payload.recipient.email,
                    on_shipment=True,
                    on_exception=True,
                    on_delivery=True,
                )
                if options.notification_email else None
            ),
            print_preferences=PrintPreferencesType(
                output_format=label_format,
                encoding=label_encoding,
            ),
            preferences=PreferencesType(
                service_code=None,
                show_packing_instructions=False,
                show_postage_rate=True,
                show_insured_value=True,
            ),
            customs=(
                CustomsType(
                    currency=options.currency or Currency.CAD.value,
                    conversion_from_cad=None,
                    reason_for_export=payload.customs.content_type,
                    other_reason=payload.customs.content_description,
                    duties_and_taxes_prepaid=payload.customs.duty.account_number,
                    certificate_number=payload.customs.certificate_number,
                    licence_number=None,
                    invoice_number=payload.customs.invoice,
                    sku_list=(
                        sku_listType(
                            item=[
                                SkuType(
                                    customs_number_of_units=item.quantity,
                                    customs_description=item.description,
                                    sku=item.sku,
                                    hs_tariff_code=None,
                                    unit_weight=WeightUnit.KG.value,
                                    customs_value_per_unit=item.value_amount,
                                    customs_unit_of_measure=None,
                                    country_of_origin=payload.shipper.country_code,
                                    province_of_origin=None,
                                )
                                for item in payload.customs.commodities
                            ]
                        ),
                    )
                )
                if payload.customs is not None else None
            ),
            references=ReferencesType(
                cost_centre=None,
                customer_ref_1=payload.reference,
                customer_ref_2=None,
            ),
            settlement_info=SettlementInfoType(
                paid_by_customer=(
                    payload.payment.account_number
                    if payload.payment is not None
                    else settings.customer_number
                ),
                contract_id=settings.contract_id,
                cif_shipment=None,
                intended_method_of_payment=payment_type,
                promo_code=None,
            ),
        ),
        return_spec=None,
        pre_authorized_payment=None,
    )
    request.groupIdOrTransmitShipment.original_tagname_ = "transmit-shipment"

    return Serializable(request, _request_serializer)


def _request_serializer(request: ShipmentType) -> str:
    return XP.export(
        request,
        name_="shipment",
        namespacedef_='xmlns="http://www.canadapost.ca/ws/shipment-v8"',
    )
