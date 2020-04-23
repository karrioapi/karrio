import logging
import uuid
from typing import List, Union, Callable
from django.db.models import Q
from django.forms.models import model_to_dict
from purplship import package as api
from purplship.core.utils import exec_async, to_dict
from purpleserver.core.datatypes import (
    CarrierSettings, ShipmentRequest, ShipmentResponse, ShipmentRate, Shipment,
    RateResponse, TrackingResponse, TrackingRequest, Message, RateDetails, ErrorResponse
)
from purpleserver.core import models

logger = logging.getLogger(__name__)


def get_carriers(carrier_type: str = None, carrier_name: str = None, test: bool = None) -> Union[CarrierSettings, List[CarrierSettings]]:
    filters = dict(carrier_name=carrier_name, test=(bool(test) if test is not None else None))
    carrier_models = {carrier_type: models.MODELS.get(carrier_type)} if carrier_type is not None else models.MODELS

    if any(carrier_models.values()) and any(filters.values()):
        query = Q(**{k: v for k, v in filters.items() if v is not None})
        return sum([
            [CarrierSettings(carrier=carrier, settings=model_to_dict(s)) for s in model.objects.filter(query)]
            for carrier, model in carrier_models.items()
        ], [])
    elif any(carrier_models.values()):
        return sum([
            [CarrierSettings(carrier=type_, settings=model_to_dict(s)) for s in model.objects.all()]
            for type_, model in carrier_models.items()
        ], [])
    else:
        raise Exception(f'Unknown carrier {carrier_type}')


def create_shipment(payload: dict, resolve_tracking_url: Callable[[str, dict], str] = None) -> Union[ShipmentResponse, ErrorResponse]:
    selected_rate = next(
        (RateDetails(**rate) for rate in payload.get('rates') if rate.get('id') == payload.get('selected_rate_id')),
        None
    )

    if selected_rate is None:
        raise Exception(
            f'Invalid "selected_rate_id": {payload.get("selected_rate_id")}'
            f'Please select from {", ".join([r.id for r in payload.get("rates")])}'
        )

    carrier_settings = next(
        iter(get_carriers(carrier_type=selected_rate.carrier, carrier_name=selected_rate.carrier_name)),
        None
    )

    request = ShipmentRequest(**{**payload, 'service': selected_rate.service})
    gateway = api.gateway[carrier_settings.carrier].create(carrier_settings.settings)
    shipment, messages = api.Shipment.create(request).with_(gateway).parse()

    if shipment is None:
        return ErrorResponse(messages=messages)

    shipment_rate = shipment.selected_rate or selected_rate
    is_test = "?test=true" if carrier_settings.settings.get("test") else ""
    tracking_url = (
        resolve_tracking_url(shipment.tracking_number, shipment) + is_test
        if resolve_tracking_url is not None else None
    )
    return ShipmentResponse(
        shipment=Shipment(**{
            **payload,
            **to_dict(shipment),
            "service": shipment_rate.service,
            "selected_rate": to_dict(shipment_rate),
            "tracking_url": tracking_url
        }) if shipment is not None else None,
        messages=messages
    )


def fetch_rates(payload: dict, carrier_settings_list: List[CarrierSettings]) -> Union[RateResponse, ErrorResponse]:
    request = api.Rating.fetch(payload)

    def process(carrier_settings: CarrierSettings):
        try:
            gateway = api.gateway[carrier_settings.carrier].create(carrier_settings.settings)
            return request.from_(gateway).parse()
        except Exception as e:
            logger.exception(e)
            return [[], [Message(
                code="500",
                carrier=carrier_settings.carrier,
                carrier_name=carrier_settings.settings.get('carrier_name'),
                message=str(e)
            )]]

    results = exec_async(process, carrier_settings_list)
    rates = sum((r for r, _ in results if r is not None), [])
    messages = sum((m for _, m in results), [])

    if len(rates) == 0:
        return ErrorResponse(messages=messages)

    return RateResponse(
        shipment=ShipmentRate(**{
            **payload,
            'rates': [
                {**{**to_dict(r), 'id': str(uuid.uuid4())}} for r in rates
            ]
        }) if len(rates) > 0 else None,
        messages=messages
    )


def track_shipment(payload: dict, carrier_settings: CarrierSettings) -> TrackingResponse:
    request = TrackingRequest(**payload)

    gateway = api.gateway[carrier_settings.carrier].create(carrier_settings.settings)
    results, messages = api.Tracking.fetch(request).from_(gateway).parse()

    return TrackingResponse(
        tracking_details=next(iter(results), None),
        messages=messages
    )
