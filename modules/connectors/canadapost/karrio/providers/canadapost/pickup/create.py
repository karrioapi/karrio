from typing import Tuple, List, Union
from functools import partial
from karrio.schemas.canadapost.pickup import pickup_availability
from karrio.schemas.canadapost.pickuprequest import (
    PickupRequestDetailsType,
    PickupRequestUpdateDetailsType,
    PickupLocationType,
    AlternateAddressType,
    ContactInfoType,
    LocationDetailsType,
    ItemsCharacteristicsType,
    PickupTimesType,
    OnDemandPickupTimeType,
    PickupRequestPriceType,
    PickupRequestHeaderType,
    PickupTypeType as PickupType,
)
import karrio.lib as lib
from karrio.core.utils import (
    Serializable,
    Element,
    Job,
    Pipeline,
    DF,
    NF,
    XP,
)
from karrio.core.models import (
    PickupRequest,
    PickupDetails,
    Message,
    ChargeDetails,
    PickupUpdateRequest,
)
from karrio.core.units import Packages
from karrio.providers.canadapost.units import PackagePresets
from karrio.providers.canadapost.utils import Settings
from karrio.providers.canadapost.error import parse_error_response

PickupRequestDetails = Union[PickupRequestDetailsType, PickupRequestUpdateDetailsType]


def parse_pickup_response(
    _response: lib.Deserializable[Element], settings: Settings
) -> Tuple[PickupDetails, List[Message]]:
    response = (
        _response.deserialize() if hasattr(_response, "deserialize") else _response
    )
    pickup = (
        _extract_pickup_details(response, settings)
        if len(lib.find_element("pickup-request-header", response)) > 0
        else None
    )
    return pickup, parse_error_response(response, settings)


def _extract_pickup_details(response: Element, settings: Settings) -> PickupDetails:
    header = lib.find_element(
        "pickup-request-header", response, PickupRequestHeaderType, first=True
    )
    price = lib.find_element(
        "pickup-request-price", response, PickupRequestPriceType, first=True
    )
    price_amount = (
        sum(
            [
                NF.decimal(price.hst_amount or 0.0),
                NF.decimal(price.gst_amount or 0.0),
                NF.decimal(price.due_amount or 0.0),
            ],
            0.0,
        )
        if price is not None
        else None
    )

    return PickupDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        confirmation_number=header.request_id,
        pickup_date=DF.fdate(header.next_pickup_date),
        pickup_charge=ChargeDetails(
            name="Pickup fees", amount=NF.decimal(price_amount), currency="CAD"
        )
        if price is not None
        else None,
    )


def pickup_request(payload: PickupRequest, settings: Settings) -> Serializable:
    request: Pipeline = Pipeline(
        get_availability=lambda *_: _get_pickup_availability(payload),
        create_pickup=partial(_create_pickup, payload=payload, settings=settings),
    )
    return Serializable(request)


def _create_pickup_request(
    payload: PickupRequest, settings: Settings, update: bool = False
) -> Serializable:
    """
    pickup_request create a serializable typed PickupRequestDetailsType

    Options:
        - five_ton_flag
        - loading_dock_flag

    :param update: bool
    :param payload: PickupRequest
    :param settings: Settings
    :return: Serializable
    """
    RequestType = PickupRequestUpdateDetailsType if update else PickupRequestDetailsType
    packages = Packages(payload.parcels, PackagePresets, required=["weight"])
    heavy = any([p for p in packages if p.weight.KG > 23])
    location_details = dict(
        instruction=payload.instruction,
        five_ton_flag=payload.options.get("five_ton_flag"),
        loading_dock_flag=payload.options.get("loading_dock_flag"),
    )
    address = lib.to_address(payload.address)

    # Map unified pickup_type to CanadaPost pickup type
    # one_time -> OnDemand, daily/recurring -> Scheduled
    unified_pickup_type = getattr(payload, "pickup_type", "one_time") or "one_time"
    cp_pickup_type = (
        PickupType.SCHEDULED.value
        if unified_pickup_type in ("daily", "recurring")
        else PickupType.ON_DEMAND.value
    )

    request = RequestType(
        customer_request_id=settings.customer_number,
        pickup_type=cp_pickup_type,
        pickup_location=PickupLocationType(
            business_address_flag=(not payload.address.residential),
            alternate_address=AlternateAddressType(
                company=address.company_name or "",
                address_line_1=address.address_line,
                city=address.city,
                province=address.state_code,
                postal_code=address.postal_code,
            )
            if payload.address
            else None,
        ),
        contact_info=ContactInfoType(
            contact_name=payload.address.person_name,
            email=payload.address.email or "",
            contact_phone=payload.address.phone_number,
            telephone_ext=None,
            receive_email_updates_flag=(payload.address.email is not None),
        ),
        location_details=(
            LocationDetailsType(
                five_ton_flag=location_details["five_ton_flag"],
                loading_dock_flag=location_details["loading_dock_flag"],
                pickup_instructions=location_details["instruction"],
            )
            if any(location_details.values())
            else None
        ),
        items_characteristics=(
            ItemsCharacteristicsType(
                pww_flag=None,
                priority_flag=None,
                returns_flag=None,
                heavy_item_flag=heavy,
            )
            if heavy
            else None
        ),
        pickup_volume=f"{len(packages) or 1}",
        pickup_times=PickupTimesType(
            on_demand_pickup_time=OnDemandPickupTimeType(
                date=payload.pickup_date,
                preferred_time=payload.ready_time,
                closing_time=payload.closing_time,
            ),
            scheduled_pickup_times=None,
        ),
        payment_info=None,
    )
    return Serializable(request, partial(_request_serializer, update=update))


def _get_pickup_availability(payload: PickupRequest):
    return Job(
        id="availability", data=(payload.address.postal_code or "").replace(" ", "")
    )


def _create_pickup(
    availability_response: str, payload: PickupRequest, settings: Settings
):
    availability = XP.to_object(pickup_availability, XP.to_xml(availability_response))
    data = (
        _create_pickup_request(payload, settings)
        if availability.on_demand_tour
        else None
    )

    return Job(id="create_pickup", data=data, fallback="" if data is None else "")


def _get_pickup(
    update_response: str, payload: PickupUpdateRequest, settings: Settings
) -> Job:
    errors = parse_error_response(XP.to_xml(XP.bundle_xml([update_response])), settings)
    data = (
        None
        if any(errors)
        else f"/enab/{settings.customer_number}/pickuprequest/{payload.confirmation_number}/details"
    )

    return Job(
        id="get_pickup", data=Serializable(data), fallback="" if data is None else ""
    )


def _request_serializer(request: PickupRequestDetails, update: bool = False) -> str:
    return XP.export(
        request,
        name_=("pickup-request-update" if update else "pickup-request-details"),
        namespacedef_='xmlns="http://www.canadapost.ca/ws/pickuprequest"',
    )
