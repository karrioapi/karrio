from typing import Tuple, List
from purplship.core.utils.helpers import export
from purplship.core.utils.serializable import Serializable
from purplship.core.utils.xml import Element
from pycaps.shipment import ShipmentType, ShipmentInfoType, ShipmentPriceType
from purplship.core.settings import Settings
from purplship.core.models import (
    Error, ShipmentDetails, ChargeDetails, ReferenceDetails, ShipmentRequest
)
from purplship.core.units import Currency
from purplship.carriers.caps.error import parse_error_response


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
    request = ShipmentType(
        customer_request_id=None,
        groupIdOrTransmitShipment=None,
        quickship_label_requested=None,
        cpc_pickup_indicator=None,
        requested_shipping_point=None,
        shipping_point_id=None,
        expected_mailing_date=None,
        provide_pricing_info=None,
        provide_receipt_info=None,
        delivery_spec=None,
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
