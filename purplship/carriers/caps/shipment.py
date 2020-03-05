from typing import Tuple, List

from purplship.carriers.caps.error import parse_error_response
from purplship.carriers.caps.units import OptionCode, ServiceType
from purplship.carriers.caps.utils import Settings
from purplship.core.models import (
    Error, ShipmentDetails, ChargeDetails, ReferenceDetails, ShipmentRequest
)
from purplship.core.units import Currency, Weight, WeightUnit, DimensionUnit, Dimension
from purplship.core.utils.helpers import export
from purplship.core.utils.serializable import Serializable
from purplship.core.utils.xml import Element
from pycaps.shipment import (
    ShipmentType, ShipmentInfoType, ShipmentPriceType, DeliverySpecType,
    SenderType, AddressDetailsType, DestinationType, DestinationAddressDetailsType,
    ParcelCharacteristicsType, optionsType, ReferencesType,
    sku_listType, SkuType, dimensionsType, OptionType, CustomsType
)


def parse_shipment_response(response: Element, settings: Settings) -> Tuple[ShipmentDetails, List[Error]]:
    shipment = (
        _extract_shipment(response, settings)
        if len(response.xpath(".//*[local-name() = $name]", name="shipment-id")) > 0
        else None
    )
    return shipment, parse_error_response(response, settings)


def _extract_shipment(response: Element, settings: Settings) -> ShipmentDetails:
    info = ShipmentInfoType()
    data = ShipmentPriceType()

    info.build(response.xpath(".//*[local-name() = $name]", name="shipment-info")[0])
    data.build(response.xpath(".//*[local-name() = $name]", name="shipment-price")[0])
    currency_ = Currency.CAD.name

    return ShipmentDetails(
        carrier=settings.carrier_name,
        tracking_numbers=[info.tracking_pin],
        total_charge=ChargeDetails(name="Shipment charge", amount=data.due_amount, currency=currency_),
        charges=(
            [
                ChargeDetails(name="base-amount", amount=data.base_amount, currency=currency_),
                ChargeDetails(name="gst-amount", amount=data.gst_amount, currency=currency_),
                ChargeDetails(name="pst-amount", amount=data.pst_amount, currency=currency_),
                ChargeDetails(name="hst-amount", amount=data.hst_amount, currency=currency_),
            ]
            + [
                ChargeDetails(name=adjustment.adjustment_code, amount=adjustment.adjustment_amount, currency=currency_)
                for adjustment in data.adjustments.get_adjustment()
            ]
            + [
                ChargeDetails(name=option.option_code, amount=option.option_price, currency=currency_)
                for option in data.priced_options.get_priced_option()
            ]
        ),
        shipment_date=data.service_standard.expected_delivery_date,
        services=(
            [data.service_code] + [option.option_code for option in data.priced_options.get_priced_option()]
        ),
        documents=[
            link.get("href")
            for link in response.xpath(".//*[local-name() = $name]", name="link")
            if link.get("rel") == "label"
        ],
        reference=ReferenceDetails(value=info.shipment_id, type="Shipment Id"),
    )


def shipment_request(payload: ShipmentRequest, settings: Settings) -> Serializable[ShipmentType]:
    package = payload.shipment.items[0]
    requested_services = [
        svc for svc in payload.shipment.services if svc in ServiceType.__members__
    ]
    requested_options = dict(
        (opt, value) for opt, value in payload.shipment.options.items() if opt in OptionCode.__members__
    )
    request = ShipmentType(
        customer_request_id=payload.shipper.account_number or settings.customer_number,
        groupIdOrTransmitShipment=None,
        quickship_label_requested=None,
        cpc_pickup_indicator=None,
        requested_shipping_point=None,
        shipping_point_id=None,
        expected_mailing_date=None,
        provide_pricing_info=True,
        provide_receipt_info=None,
        delivery_spec=DeliverySpecType(
            service_code=ServiceType[requested_services[0]].value
            if len(requested_services) > 0
            else None,
            sender=SenderType(
                name=payload.shipper.person_name,
                company=payload.shipper.company_name,
                contact_phone=payload.shipper.phone_number,
                address_details=AddressDetailsType(
                    city=payload.shipper.city,
                    prov_state=payload.shipper.state_code,
                    country_code=payload.shipper.country_code,
                    postal_zip_code=payload.shipper.postal_code,
                    address_line_1=payload.shipper.address_lines[0]
                    if len(payload.shipper.address_lines) > 0
                    else None,
                    address_line_2=payload.shipper.address_lines[1]
                    if len(payload.shipper.address_lines) > 1
                    else None,
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
                    address_line_1=payload.recipient.address_lines[0]
                    if len(payload.recipient.address_lines) > 0
                    else None,
                    address_line_2=payload.recipient.address_lines[1]
                    if len(payload.recipient.address_lines) > 1
                    else None,
                ),
            ),
            parcel_characteristics=ParcelCharacteristicsType(
                weight=Weight(
                    payload.shipment.total_weight or package.weight,
                    WeightUnit[payload.shipment.weight_unit],
                ).KG,
                dimensions=dimensionsType(
                    length=Dimension(
                        package.length, DimensionUnit[payload.shipment.dimension_unit]
                    ).CM,
                    width=Dimension(
                        package.width, DimensionUnit[payload.shipment.dimension_unit]
                    ).CM,
                    height=Dimension(
                        package.height, DimensionUnit[payload.shipment.dimension_unit]
                    ).CM,
                ),
                unpackaged=None,
                mailing_tube=None,
            ),
            options=optionsType(
                option=[
                    OptionType(
                        option_code=OptionCode[code].value,
                        option_amount=None,
                        option_qualifier_1=None,
                        option_qualifier_2=None,
                    )
                    for code, value in requested_options
                ]
            )
            if len(requested_options) > 0
            else None,
            notification=None,
            preferences=None,
            customs=CustomsType(
                currency=payload.shipment.currency,
                conversion_from_cad=None,
                reason_for_export=payload.shipment.customs.terms_of_trade,
                other_reason=payload.shipment.customs.description,
                duties_and_taxes_prepaid=payload.shipment.duty_payment_account,
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
                            customs_unit_of_measure=DimensionUnit.CM.value,
                            country_of_origin=item.origin_country,
                            province_of_origin=None,
                        )
                        for item in payload.shipment.items
                    ]
                ),
            )
            if payload.shipment.customs is not None
            else None,
            references=ReferencesType(
                cost_centre=None,
                customer_ref_1=payload.shipment.references[0]
                if len(payload.shipment.references) > 0
                else None,
                customer_ref_2=payload.shipment.references[1]
                if len(payload.shipment.references) > 1
                else None,
            )
            if len(payload.shipment.references) > 0
            else None,
        ),
        return_spec=None,
        pre_authorized_payment=None
    )
    return Serializable(request, _request_serializer)


def _request_serializer(request: ShipmentType) -> str:
    return export(
        request,
        name_="shipment",
        namespacedef_='xmlns="http://www.canadapost.ca/ws/shipment-v8"'
    )
