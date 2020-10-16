from typing import Tuple, List, Any
from purplship.providers.canadapost.error import parse_error_response
from purplship.providers.canadapost.units import (
    OptionCode,
    ServiceType,
    PackagePresets,
    PrinterType,
    PaymentType,
)
from purplship.providers.canadapost.utils import Settings
from purplship.core.models import (
    Message,
    ShipmentDetails,
    ShipmentRequest,
)
from purplship.core.units import Currency, WeightUnit, Options, Packages
from purplship.core.utils import export, concat_str, Serializable, Element
from purplship.core.errors import FieldError, FieldErrorCode
from pycanadapost.shipment import (
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


def parse_contract_shipment_response(
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
        label=label.text if len(errors) == 0 else None
    )


def contract_shipment_request(
    payload: ShipmentRequest, settings: Settings
) -> Serializable[ShipmentType]:
    package = Packages(payload.parcels, PackagePresets).single

    if package.weight.value is None:
        raise FieldError({"parcel.weight": FieldErrorCode.required})

    service = ServiceType[payload.service].value
    options = Options(payload.options)

    def compute_amount(code: str, _: Any):
        if code == OptionCode.insurance.value:
            return options.insurance.amount
        if code == OptionCode.cash_on_delivery.value:
            return options.cash_on_delivery.amount
        return None

    special_services = {
        OptionCode[name].value: compute_amount(OptionCode[name].value, value)
        for name, value in payload.options.items()
        if name in OptionCode.__members__
    }
    payment_type = (
        PaymentType[payload.payment.paid_by].value
        if payload.payment is not None
        else None
    )

    request = ShipmentType(
        customer_request_id=None,
        groupIdOrTransmitShipment=groupIdOrTransmitShipment(),
        quickship_label_requested=None,
        cpc_pickup_indicator=None,
        requested_shipping_point=payload.shipper.postal_code,
        shipping_point_id=None,
        expected_mailing_date=None,
        provide_pricing_info=True,
        provide_receipt_info=None,
        delivery_spec=DeliverySpecType(
            service_code=service,
            sender=SenderType(
                name=payload.shipper.person_name,
                company=payload.shipper.company_name,
                contact_phone=payload.shipper.phone_number,
                address_details=AddressDetailsType(
                    city=payload.shipper.city,
                    prov_state=payload.shipper.state_code,
                    country_code=payload.shipper.country_code,
                    postal_zip_code=payload.shipper.postal_code,
                    address_line_1=concat_str(payload.shipper.address_line1, join=True),
                    address_line_2=concat_str(payload.shipper.address_line2, join=True),
                ),
            ),
            destination=DestinationType(
                name=payload.recipient.person_name,
                company=payload.recipient.company_name,
                additional_address_info=None,
                client_voice_number=None,
                address_details=DestinationAddressDetailsType(
                    city=payload.recipient.city,
                    prov_state=payload.recipient.state_code,
                    country_code=payload.recipient.country_code,
                    postal_zip_code=payload.recipient.postal_code,
                    address_line_1=concat_str(
                        payload.recipient.address_line1, join=True
                    ),
                    address_line_2=concat_str(
                        payload.recipient.address_line2, join=True
                    ),
                ),
            ),
            parcel_characteristics=ParcelCharacteristicsType(
                weight=package.weight.KG,
                dimensions=dimensionsType(
                    length=package.length.CM,
                    width=package.width.CM,
                    height=package.height.CM,
                ),
                unpackaged=None,
                mailing_tube=None,
            ),
            options=optionsType(
                option=[
                    OptionType(
                        option_code=code,
                        option_amount=amount,
                        option_qualifier_1=None,
                        option_qualifier_2=None,
                    )
                    for code, amount in special_services.items()
                ]
            )
            if len(special_services) > 0
            else None,
            notification=NotificationType(
                email=options.notification.email or payload.shipper.email,
                on_shipment=True,
                on_exception=True,
                on_delivery=True,
            )
            if options.notification
            else None,
            print_preferences=PrintPreferencesType(
                output_format=PrinterType[options.printing or "regular"].value,
                encoding=None,
            ),
            preferences=PreferencesType(
                service_code=None,
                show_packing_instructions=True,
                show_postage_rate=True,
                show_insured_value=True,
            ),
            customs=CustomsType(
                currency=Currency.AUD.value,
                conversion_from_cad=None,
                reason_for_export=payload.customs.terms_of_trade,
                other_reason=payload.customs.description,
                duties_and_taxes_prepaid=payload.customs.duty.account_number,
                certificate_number=None,
                licence_number=None,
                invoice_number=None,
                sku_list=sku_listType(
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
            if payload.customs is not None
            else None,
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
    return Serializable(request, _request_serializer)


def _request_serializer(request: ShipmentType) -> str:
    request.groupIdOrTransmitShipment.original_tagname_ = "transmit-shipment"
    return export(
        request,
        name_="shipment",
        namespacedef_='xmlns="http://www.canadapost.ca/ws/shipment-v8"',
    )
