from typing import Tuple, List
from pycanadapost.pickuprequest import (
    PickupRequestDetailsType,
    PickupLocationType,
    AlternateAddressType,
    ContactInfoType,
    LocationDetailsType,
    ItemsCharacteristicsType,
    PickupTimesType,
    OnDemandPickupTimeType,
    PickupRequestInfoType,
    PickupRequestPriceType,
    PickupRequestHeaderType
)
from purplship.core.utils import Serializable, export, Element, concat_str, build, format_date, decimal
from purplship.core.models import PickupRequest, PickupDetails, Message, ChargeDetails
from purplship.providers.canadapost.utils import Settings
from purplship.providers.canadapost.error import parse_error_response


def parse_pickup_response(response: Element, settings: Settings) -> Tuple[PickupDetails, List[Message]]:
    pickup = (
        _extract_pickup_details(response, settings)
        if len(response.xpath(".//*[local-name() = $name]", name="pickup-request-info")) > 0
        else None
    )
    return pickup, parse_error_response(response, settings)


def _extract_pickup_details(response: Element, settings: Settings) -> PickupDetails:
    pickup_info = next(
        build(PickupRequestInfoType, elt) for elt in
        response.xpath(".//*[local-name() = $name]", name="pickup-request-info")
    )
    header: PickupRequestHeaderType = pickup_info.pickup_request_header
    price: PickupRequestPriceType = pickup_info.pickup_request_price
    price_amount = sum([price.hst_amount, price.gst_amount, price.due_amount])

    return PickupDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        confirmation_number=header.request_id,
        pickup_date=format_date(header.next_pickup_date),
        pickup_charge=ChargeDetails(name="Pickup fees", amount=decimal(price_amount), currency="CAD")
    )


def pickup_request(payload: PickupRequest, settings: Settings):
    request = PickupRequestDetailsType(
        customer_request_id=settings.customer_number,
        pickup_type="Ondemand",
        pickup_location=PickupLocationType(
            business_address_flag=(payload.address.residential is False),
            alternate_address=AlternateAddressType(
                company=payload.address.company_name,
                address_line_1=concat_str(payload.address.address_line1, payload.address.address_line2, join=True),
                city=payload.address.city,
                province=payload.address.state_code,
                postal_code=payload.address.postal_code
            )
        ),
        contact_info=ContactInfoType(
            contact_name=payload.address.person_name,
            email=payload.address.email,
            contact_phone=payload.address.phone_number,
            telephone_ext=None,
            receive_email_updates_flag=(payload.address.email is not None)
        ),
        location_details=LocationDetailsType(
            five_ton_flag=None,
            loading_dock_flag=None,
            pickup_instructions=payload.instruction
        ),
        items_characteristics=ItemsCharacteristicsType(
            pww_flag=None,
            priority_flag=None,
            returns_flag=None,
            heavy_item_flag=payload.options.get('heavy')
        ),
        pickup_volume=None,
        pickup_times=PickupTimesType(
            on_demand_pickup_time=OnDemandPickupTimeType(
                date=payload.date,
                preferred_time=payload.ready_time,
                closing_time=payload.closing_time
            ),
            scheduled_pickup_times=None
        ),
        payment_info=None
    )
    return Serializable(request, _request_serializer)


def _request_serializer(request: PickupRequestDetailsType) -> str:
    return export(
        request,
        namespacedef_='xmlns="http://www.canadapost.ca/ws/pickuprequest"',
    )
