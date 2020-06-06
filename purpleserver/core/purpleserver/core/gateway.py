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


def get_carriers(carrier_name: str = None, carrier_ids: List[str] = None, test: bool = None) -> Union[CarrierSettings, List[CarrierSettings]]:
    mode = dict(test=test)
    filters: List[dict] = [{"carrier_id": carrier_id, **mode} for carrier_id in (carrier_ids or [])]
    carrier_models = {carrier_name: models.MODELS.get(carrier_name)} if (carrier_name is not None) else models.MODELS

    if any(carrier_models.values()) and (any(filters) or (test is not None)):
        queries = Q()
        for query in (filters if any(filters) else [mode]):
            queries |= Q(**{k: v for k, v in query.items() if v is not None})

        return sum([
            [CarrierSettings(carrier_name=name, settings=model_to_dict(s)) for s in model.objects.filter(queries)]
            for name, model in carrier_models.items()
        ], [])
    elif any(carrier_models.values()):
        return sum([
            [CarrierSettings(carrier_name=name, settings=model_to_dict(s)) for s in model.objects.all()]
            for name, model in carrier_models.items()
        ], [])
    else:
        raise Exception(f'Unknown carrier {carrier_name}')


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

    carrier_settings: CarrierSettings = next(
        iter(get_carriers(carrier_name=selected_rate.carrier_name, carrier_ids=[selected_rate.carrier_id])),
        None
    )

    request = ShipmentRequest(**{**payload, 'service': selected_rate.service})
    gateway = api.gateway[carrier_settings.carrier_name].create(carrier_settings.settings)
    shipment, messages = api.Shipment.create(request).with_(gateway).parse()

    if shipment is None:
        return ErrorResponse(messages=messages)

    shipment_rate = shipment.selected_rate or selected_rate
    shipment_rate_id = (
        selected_rate.id
        if(to_dict(selected_rate) == to_dict({**to_dict(shipment_rate), 'id': selected_rate.id})) else
        str(uuid.uuid4())
    )
    is_test = "?test" if carrier_settings.settings.get("test") else ""
    tracking_url = (
        resolve_tracking_url(shipment.tracking_number, shipment) + is_test
        if resolve_tracking_url is not None else None
    )
    return ShipmentResponse(
        shipment=Shipment(**{
            **payload,
            **to_dict(shipment),
            "service": shipment_rate.service,
            "selected_rate_id": shipment_rate,
            "selected_rate": {**to_dict(shipment_rate), 'id': shipment_rate_id},
            "tracking_url": tracking_url
        }) if shipment is not None else None,
        messages=messages
    )


def fetch_rates(payload: dict, carrier_settings_list: List[CarrierSettings]) -> Union[RateResponse, ErrorResponse]:
    request = api.Rating.fetch(ShipmentRate(**payload))

    def process(carrier_settings: CarrierSettings):
        try:
            gateway = api.gateway[carrier_settings.carrier_name].create(carrier_settings.settings)
            return request.from_(gateway).parse()
        except Exception as e:
            logger.exception(e)
            return [[], [Message(
                code="500",
                carrier_name=carrier_settings.carrier_name,
                carrier_id=carrier_settings.settings.get('carrier_id'),
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

    gateway = api.gateway[carrier_settings.carrier_name].create(carrier_settings.settings)
    results, messages = api.Tracking.fetch(request).from_(gateway).parse()

    return TrackingResponse(
        tracking_details=next(iter(results), None),
        messages=messages
    )
