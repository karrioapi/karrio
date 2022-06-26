from typing import Tuple, List
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
from karrio.core.units import Currency, WeightUnit, Options, Packages
from karrio.core.utils import Serializable, Element, XP, SF
from karrio.core.models import (
    Documents,
    Duty,
    Message,
    ShipmentDetails,
    ShipmentRequest,
)
from karrio.providers.canadapost.error import parse_error_response
from karrio.providers.canadapost.units import (
    ShippingOption,
    ServiceType,
    PackagePresets,
    PaymentType,
    LabelType,
    CUSTOM_OPTIONS,
    MeasurementOptions,
)
from karrio.providers.canadapost.utils import Settings, format_ca_postal_code


def parse_shipment_response(
    response: Element, settings: Settings
) -> Tuple[ShipmentDetails, List[Message]]:
    shipment = (
        _extract_shipment(response, settings)
        if len(XP.find("shipment-id", response)) > 0
        else None
    )
    return shipment, parse_error_response(response, settings)


def _extract_shipment(response: Element, settings: Settings) -> ShipmentDetails:
    info = XP.find("shipment-info", response, ShipmentInfoType, first=True)
    label = XP.find("label", response, first=True)

    return ShipmentDetails(
        carrier_name=settings.carrier_name,
        carrier_id=settings.carrier_id,
        tracking_number=info.tracking_pin,
        shipment_identifier=info.tracking_pin,
        docs=Documents(label=getattr(label, "text", None)),
    )


def shipment_request(
    payload: ShipmentRequest, settings: Settings
) -> Serializable[ShipmentType]:
    service = ServiceType.map(payload.service).value_or_key
    package = Packages(
        payload.parcels,
        PackagePresets,
        required=["weight"],
        package_option_type=ShippingOption,
    ).single
    options = ShippingOption.to_options(
        options=payload.options,
        package_options=package.options,
        is_international=(
            payload.recipient.country_code is not None
            and payload.recipient.country_code != "CA"
        ),
    )

    customs = payload.customs
    duty = getattr(customs, "duty", Duty())
    label_encoding, label_format = LabelType[payload.label_type or "PDF_4x6"].value

    request = ShipmentType(
        customer_request_id=None,
        groupIdOrTransmitShipment=groupIdOrTransmitShipment(),
        quickship_label_requested=None,
        cpc_pickup_indicator=None,
        requested_shipping_point=format_ca_postal_code(payload.shipper.postal_code),
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
                    postal_zip_code=format_ca_postal_code(payload.shipper.postal_code),
                    address_line_1=SF.concat_str(
                        payload.shipper.address_line1, join=True
                    ),
                    address_line_2=SF.concat_str(
                        payload.shipper.address_line2, join=True
                    ),
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
                    postal_zip_code=format_ca_postal_code(
                        payload.recipient.postal_code
                    ),
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
                            option_code=code,
                            option_amount=value,
                            option_qualifier_1=None,
                            option_qualifier_2=None,
                        )
                        for _, code, value in options.as_list()
                    ]
                )
                if any(options.as_list())
                else None
            ),
            notification=(
                NotificationType(
                    email=options.email_notification_to or payload.recipient.email,
                    on_shipment=True,
                    on_exception=True,
                    on_delivery=True,
                )
                if options.email_notification
                and any([options.email_notification_to, payload.recipient.email])
                else None
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
                    currency=options.currency or Currency.CAD.name,
                    conversion_from_cad=None,
                    reason_for_export="OTH",
                    other_reason=customs.content_type,
                    duties_and_taxes_prepaid=duty.account_number,
                    certificate_number=customs.certificate_number,
                    licence_number=customs.license_number,
                    invoice_number=customs.invoice,
                    sku_list=(
                        sku_listType(
                            item=[
                                SkuType(
                                    customs_number_of_units=item.quantity,
                                    customs_description=item.description,
                                    sku=item.sku,
                                    hs_tariff_code=item.hs_code,
                                    unit_weight=WeightUnit.KG.value.lower(),
                                    customs_value_per_unit=item.value_amount,
                                    customs_unit_of_measure=None,
                                    country_of_origin=item.origin_country,
                                    province_of_origin=None,
                                )
                                for item in customs.commodities
                            ]
                        )
                    )
                    if any(customs.commodities or [])
                    else None,
                )
                if customs is not None
                else None
            ),
            references=ReferencesType(
                cost_centre=(
                    options.canadapost_cost_center
                    or settings.metadata.get("cost-center")
                    or payload.reference
                ),
                customer_ref_1=payload.reference,
                customer_ref_2=None,
            ),
            settlement_info=SettlementInfoType(
                paid_by_customer=getattr(
                    payload.payment, "account_number", settings.customer_number
                ),
                contract_id=settings.contract_id,
                cif_shipment=None,
                intended_method_of_payment=PaymentType.map(
                    getattr(payload.payment, "paid_by", None)
                ).value,
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
