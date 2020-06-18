import logging
import uuid
from typing import List, Union, Callable, Type, Dict, Any
from django.forms.models import model_to_dict
from purplship import package as api
from purplship.core.utils import exec_async, to_dict
from purpleserver.core.datatypes import (
    CarrierSettings, ShipmentRequest, ShipmentResponse, ShipmentRate, Shipment,
    RateResponse, TrackingResponse, TrackingRequest, Message, RateDetails, ErrorResponse
)
from purpleserver.core import models

logger = logging.getLogger(__name__)


class Carriers:
    @staticmethod
    def retrieve(*args, **kwargs) -> CarrierSettings:
        carrier = models.Carrier.objects.get(*args, **kwargs).settings()
        return CarrierSettings.create({**model_to_dict(carrier), 'carrier_name': carrier.CARRIER_NAME})

    @staticmethod
    def list(**kwargs) -> List[CarrierSettings]:
        list_filter: Dict[str: Any] = kwargs
        query = {}
        model: Type[models.Carrier] = models.Carrier

        if 'test' in list_filter:
            test = False if list_filter['test'] is False else True
            query.update(dict(test=test))

        if any(list_filter.get('carrier_ids', [])):
            query.update(dict(carrier_id__in=list_filter['carrier_ids']))

        if 'carrier_name' in list_filter:
            if list_filter['carrier_name'] not in models.MODELS:
                raise Exception(f"No configurations for the following carrier: '{list_filter['carrier_name']}'")

            model = models.MODELS[list_filter['carrier_name']]

        return [
            CarrierSettings.create((
                lambda s: {
                    **model_to_dict(s),
                    'carrier_name': s.CARRIER_NAME
                }
            )(s.settings() or s))
            for s in model.objects.filter(**query)
        ]


class Shipments:
    @staticmethod
    def create(payload: dict, resolve_tracking_url: Callable[[str, dict], str] = None) -> Union[ShipmentResponse, ErrorResponse]:
        selected_rate = next(
            (RateDetails(**rate) for rate in payload.get('rates') if rate.get('id') == payload.get('selected_rate_id')),
            None
        )

        if selected_rate is None:
            raise Exception(
                f'Invalid "selected_rate_id": {payload.get("selected_rate_id")}'
                f'Please select from {", ".join([r.id for r in payload.get("rates")])}'
            )

        carrier_settings: CarrierSettings = Carriers.retrieve(carrier_id=selected_rate.carrier_id)

        request = ShipmentRequest(**{**payload, 'service': selected_rate.service})
        gateway = api.gateway[carrier_settings.carrier_name].create(carrier_settings.dict())
        shipment, messages = api.Shipment.create(request).with_(gateway).parse()

        if shipment is None:
            return ErrorResponse(messages=messages)

        shipment_rate = shipment.selected_rate or selected_rate
        shipment_rate_id = (
            selected_rate.id
            if(to_dict(selected_rate) == to_dict({**to_dict(shipment_rate), 'id': selected_rate.id})) else
            f'prx_{uuid.uuid4().hex}'
        )
        is_test = "?test" if carrier_settings.test else ""
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

    @staticmethod
    def track(payload: dict, carrier_settings: CarrierSettings) -> TrackingResponse:
        request = TrackingRequest(**payload)

        gateway = api.gateway[carrier_settings.carrier_name].create(carrier_settings.dict())
        results, messages = api.Tracking.fetch(request).from_(gateway).parse()

        return TrackingResponse(
            tracking_details=next(iter(results), None),
            messages=messages
        )


class Rates:
    @staticmethod
    def fetch(payload: dict, carrier_settings_list: List[CarrierSettings]) -> Union[RateResponse, ErrorResponse]:
        request = api.Rating.fetch(ShipmentRate(**payload))

        def process(carrier_settings: CarrierSettings):
            try:
                gateway = api.gateway[carrier_settings.carrier_name].create(carrier_settings.dict())
                return request.from_(gateway).parse()
            except Exception as e:
                logger.exception(e)
                return [[], [Message(
                    code="500",
                    carrier_name=carrier_settings.carrier_name,
                    carrier_id=carrier_settings.carrier_id,
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
                    {**{**to_dict(r), 'id': f'prx_{uuid.uuid4().hex}'}} for r in rates
                ]
            }) if len(rates) > 0 else None,
            messages=messages
        )
