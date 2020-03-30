from typing import List, Union
from django.db.models import Q
from django.forms.models import model_to_dict
from purplship import package as api
from purplship.core.utils import exec_async, to_dict
from purpleserver.core.datatypes import (
    RateRequest, TrackingRequest, ShipmentRequest, CarrierSettings, Shipment, Message,
    ShipmentDetails, ShipmentRate, TrackingDetails, RateDetails,
    CompleteTrackingResponse, CompleteShipmentResponse, CompleteRateResponse
)
from purpleserver.core import models


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


def create_shipment(payload: dict, carrier_settings: CarrierSettings) -> CompleteShipmentResponse:
    request = ShipmentRequest(**{
        key: value for key, value in payload.items() if key in ShipmentRequest.__annotations__
    })

    gateway = api.gateway[carrier_settings.carrier].create(carrier_settings.settings)
    shipment, messages = api.shipment.create(request).from_(gateway).parse()

    return CompleteShipmentResponse(
        shipment=Shipment(**{**payload, **to_dict(shipment)}),
        messages=messages
    )


def fetch_rates(payload: dict, carrier_settings_list: List[CarrierSettings]) -> CompleteShipmentResponse:
    request = RateRequest(**payload)

    def process(carrier_settings: CarrierSettings):
        gateway = api.gateway[carrier_settings.carrier].create(carrier_settings.settings)
        return api.rating.fetch(request).from_(gateway).parse()

    rates, messages = exec_async(process, carrier_settings_list)

    return CompleteShipmentResponse(
        shipment=ShipmentRate(**{**payload, 'rates': to_dict(rates)}),
        messages=messages
    )


def track_shipment(payload: dict, carrier_settings: CarrierSettings) -> CompleteTrackingResponse:
    request = TrackingRequest(**payload)

    gateway = api.gateway[carrier_settings.carrier].create(carrier_settings.clean_settings)
    results, messages = api.tracking.fetch(request).from_(gateway).parse()

    return CompleteTrackingResponse(
        tracking_details=next(iter(results), None),
        messages=messages
    )
