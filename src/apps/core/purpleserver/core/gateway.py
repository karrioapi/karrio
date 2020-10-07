import uuid
import logging
from typing import List, Callable, Dict, Any

from rest_framework import status
from rest_framework.exceptions import NotFound

import purplship
from purplship.core.utils import exec_async, to_dict

from purpleserver.providers import models
from purpleserver.core.exceptions import PurplShipApiException
from purpleserver.core.datatypes import (
    CarrierSettings, ShipmentRequest, ShipmentResponse, RateRequest, Shipment,
    RateResponse, TrackingResponse, TrackingRequest, Message, Rate, ErrorResponse
)
from purpleserver.core.serializers import ShipmentStatus
from purpleserver.core.utils import identity, post_processing

logger = logging.getLogger(__name__)


class Carriers:
    @staticmethod
    def retrieve(*args, **kwargs) -> models.Carrier:
        return models.Carrier.objects.get(*args, **kwargs)

    @staticmethod
    def list(**kwargs) -> List[models.Carrier]:
        list_filter: Dict[str: Any] = kwargs
        query = {}

        if 'test' in list_filter:
            test = False if list_filter['test'] is False else True
            query.update(dict(test=test))

        if 'carrier_id' in list_filter:
            query.update(dict(carrier_id=list_filter['carrier_id']))

        if any(list_filter.get('carrier_ids', [])):
            query.update(dict(carrier_id__in=list_filter['carrier_ids']))

        if 'carrier_name' in list_filter:
            if list_filter['carrier_name'] not in models.MODELS.keys():
                raise NotFound(f"No configurations for the following carrier: '{list_filter['carrier_name']}'")

            carriers = [
                setting.carrier_ptr for setting in models.MODELS[list_filter['carrier_name']].objects.filter(**query)
            ]
        else:
            carriers = models.Carrier.objects.filter(**query)

        return carriers


class Shipments:
    @staticmethod
    def create(payload: dict, resolve_tracking_url: Callable[[Shipment], str] = None) -> ShipmentResponse:
        selected_rate = next(
            (Rate(**rate) for rate in payload.get('rates') if rate.get('id') == payload.get('selected_rate_id')),
            None
        )

        if selected_rate is None:
            raise NotFound(
                f'Invalid selected_rate_id "{payload.get("selected_rate_id")}" \n '
                f'Please select one of the following: [ {", ".join([r.get("id") for r in payload.get("rates")])} ]'
            )

        carrier = Carriers.retrieve(carrier_id=selected_rate.carrier_id).data
        request = ShipmentRequest(**{**to_dict(payload), 'service': selected_rate.service})
        gateway = purplship.gateway[carrier.carrier_name].create(carrier.dict())

        # The request is wrapped in identity to simplify mocking in tests
        shipment, messages = identity(lambda: purplship.Shipment.create(request).with_(gateway).parse())

        if shipment is None:
            raise PurplShipApiException(detail=ErrorResponse(messages=messages), status_code=status.HTTP_400_BAD_REQUEST)

        shipment_rate = shipment.selected_rate or selected_rate
        shipment_rate_id = (
            selected_rate.id
            if(to_dict(selected_rate) == to_dict({**to_dict(shipment_rate), 'id': selected_rate.id})) else
            f'prx_{uuid.uuid4().hex}'
        )
        tracking_url = None

        try:
            is_test = "?test" if carrier.test else ""
            tracking_url = (
                resolve_tracking_url(shipment) + is_test
                if resolve_tracking_url is not None else None
            )
        except Exception as e:
            logger.warning(f"Failed to generate tracking url: {e}")

        return ShipmentResponse(
            shipment=Shipment(**{
                **payload,
                **to_dict(shipment),
                "service": shipment_rate.service,
                "selected_rate_id": shipment_rate_id,
                "selected_rate": {**to_dict(shipment_rate), 'id': shipment_rate_id},
                "tracking_url": tracking_url,
                "status": ShipmentStatus.purchased.value
            }) if shipment is not None else None,
            messages=messages
        )

    @staticmethod
    def track(payload: dict, carrier_filter: dict) -> TrackingResponse:
        carrier = next(iter(Carriers.list(**carrier_filter)), None)

        if carrier is None:
            raise NotFound('No configured carrier found')

        request = purplship.Tracking.fetch(TrackingRequest(**payload))
        gateway = purplship.gateway[carrier.data.carrier_name].create(carrier.data.dict())

        # The request call is wrapped in identity to simplify mocking in tests
        results, messages = identity(lambda: request.from_(gateway).parse())

        if any(messages or []) and not any(results or []):
            raise PurplShipApiException(detail=ErrorResponse(messages=messages), status_code=status.HTTP_404_NOT_FOUND)

        return TrackingResponse(
            tracking_details=results[0],
            messages=messages
        )


@post_processing(methods=['fetch'])
class Rates:
    post_process_functions: List[Callable] = []

    @staticmethod
    def fetch(payload: dict) -> RateResponse:
        request = purplship.Rating.fetch(RateRequest(**to_dict(payload)))

        carrier_settings_list = [
            carrier.data for carrier in Carriers.list(carrier_ids=payload.get('carrier_ids', []))
        ]

        if len(carrier_settings_list) == 0:
            raise NotFound("No configured carriers specified")

        def process(carrier_settings: CarrierSettings):
            try:
                gateway = purplship.gateway[carrier_settings.carrier_name].create(carrier_settings.dict())
                return request.from_(gateway).parse()
            except Exception as e:
                logger.exception(e)
                return [[], [Message(
                    code="500",
                    carrier_name=carrier_settings.carrier_name,
                    carrier_id=carrier_settings.carrier_id,
                    message=str(e)
                )]]

        # The request call is wrapped in identity to simplify mocking in tests
        results = identity(lambda: exec_async(process, carrier_settings_list))
        flattened_rates = sum((r for r, _ in results if r is not None), [])
        messages = sum((m for _, m in results), [])

        if not any(flattened_rates) and any(messages):
            raise PurplShipApiException(detail=ErrorResponse(messages=messages), status_code=status.HTTP_400_BAD_REQUEST)

        rates: List[Rate] = [
            Rate(**{
                'id': f'rat_{uuid.uuid4().hex}',
                'carrier_ref': next((c.id for c in carrier_settings_list if c.carrier_id == r.carrier_id)),
                **{**to_dict(r)}
            }) for r in flattened_rates
        ]

        return RateResponse(
            rates=sorted(rates, key=lambda rate: rate.total_charge),
            messages=messages
        )
