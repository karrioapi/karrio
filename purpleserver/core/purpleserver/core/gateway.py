import logging
from typing import List, Union, cast
from django.db.models import Q
from django.forms.models import model_to_dict
from purplship import package as api
from purplship.core.utils import exec_async, to_dict
from purpleserver.core.datatypes import (
    CarrierSettings, ShipmentRequest, ShipmentResponse, ShipmentRate, Shipment,
    RateResponse, RateRequest, TrackingResponse, TrackingRequest, ShipmentDetails,
    Message
)
from purpleserver.core import models

logger = logging.getLogger(__name__)


def get_carriers(carrier_type: str = None, carrier_name: str = None, test: bool = None) -> Union[CarrierSettings, List[CarrierSettings]]:
    filters = dict(carrier_name=carrier_name, test=test)
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


def create_shipment(payload: dict, carrier_settings: CarrierSettings) -> ShipmentResponse:
    request = ShipmentRequest(**payload)

    selected_rate = next(
        (rate for rate in request.rates if rate.id == request.selected_rate_id),
        None
    )

    if selected_rate is None:
        raise Exception(
            f'Invalid "selected_rate_id": {request.selected_rate_id}'
            f'Please select from {", ".join([r.id for r in request.rates])}'
        )

    gateway = api.gateway[carrier_settings.carrier].create(carrier_settings.settings)
    shipment, messages = api.shipment.create(request).from_(gateway).parse()

    return ShipmentResponse(
        shipment=Shipment(**{
            **payload,
            **to_dict(shipment),
            "selected_rate": cast(ShipmentDetails, shipment).selected_rate or selected_rate
        }),
        messages=messages
    )


def fetch_rates(payload: dict, carrier_settings_list: List[CarrierSettings]) -> RateResponse:
    request = RateRequest(**payload)

    def process(carrier_settings: CarrierSettings):
        try:
            gateway = api.gateway[carrier_settings.carrier].create(carrier_settings.settings)
            return api.rating.fetch(request).from_(gateway).parse()
        except Exception as e:
            logger.exception(e)
            return Message(
                code="00000",
                carrier=carrier_settings.carrier,
                carrier_name=carrier_settings.settings.get('carrier_name'),
                message=str(e)
            )

    rates, messages = exec_async(process, carrier_settings_list)

    return RateResponse(
        shipment=ShipmentRate(**{**payload, 'rates': to_dict(rates)}),
        messages=messages
    )


def track_shipment(payload: dict, carrier_settings: CarrierSettings) -> TrackingResponse:
    request = TrackingRequest(**payload)

    gateway = api.gateway[carrier_settings.carrier].create(carrier_settings.settings)
    results, messages = api.tracking.fetch(request).from_(gateway).parse()

    return TrackingResponse(
        tracking_details=next(iter(results), None),
        messages=messages
    )
