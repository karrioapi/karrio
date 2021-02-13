import uuid
import logging
from datetime import datetime
from typing import List, Callable, Dict, Any

from django.db.models import Q
from rest_framework import status
from rest_framework.exceptions import NotFound

import purplship
from purplship.core.utils import DP

from purpleserver.providers import models
from purpleserver.core.exceptions import PurplShipApiException
from purpleserver.core.datatypes import (
    ShipmentRequest, RateRequest, Shipment,
    RateResponse, TrackingResponse, TrackingRequest, Rate, ErrorResponse,
    PickupRequest, Pickup, PickupUpdateRequest, PickupResponse, AddressValidation,
    ConfirmationResponse, PickupCancelRequest, ShipmentCancelRequest,
    AddressValidationRequest, Tracking,
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
        query = tuple()
        users = []

        # Check if the test filter is specified then set it otherwise return all carriers prod and test mode
        if list_filter.get('test') is not None:
            query += (Q(test=list_filter['test']), )

        # Check if the system_only flag is not specified and there is a provided user, get the users carriers
        if list_filter.get('system_only') is False and 'user' in list_filter:
            users += [list_filter.get('user')]

        # Check if the active flag is specified and return all active carrier is active is not set to false
        if 'active' in list_filter:
            active = False if list_filter['active'] is False else True
            query += (Q(active=active), )

        # Check if a specific carrier_id is provide, to add it to the query
        if 'carrier_id' in list_filter:
            query += (Q(carrier_id=list_filter['carrier_id']), )

        # Check if a list of carrier_ids are provided, to add the list to the query
        if any(list_filter.get('carrier_ids', [])):
            query += (Q(carrier_id__in=list_filter['carrier_ids']), )

        # Always return all system carriers and any additional carrier from the users list
        query += (Q(user__isnull=True) | Q(user__in=users),)

        if 'carrier_name' in list_filter:
            if list_filter['carrier_name'] not in models.MODELS.keys():
                raise NotFound(f"No configurations for the following carrier: '{list_filter['carrier_name']}'")

            carriers = [
                setting.carrier_ptr for setting in models.MODELS[list_filter['carrier_name']].objects.filter(*query)
            ]
        else:
            carriers = models.Carrier.objects.filter(*query)

        return carriers


class Address:
    @staticmethod
    def validate(payload: dict, carrier_filter: dict) -> AddressValidation:
        carrier = next(iter(Carriers.list(**(carrier_filter or {}))), None)

        if carrier is None:
            raise NotFound('No configured and active carrier found')

        request = purplship.Address.validate(AddressValidationRequest(**DP.to_dict(payload)))
        gateway = purplship.gateway[carrier.data.carrier_name].create(carrier.data.dict())

        # The request call is wrapped in identity to simplify mocking in tests
        validation, messages = identity(lambda: request.from_(gateway).parse())

        if validation is None:
            raise PurplShipApiException(detail=ErrorResponse(messages=messages), status_code=status.HTTP_400_BAD_REQUEST)

        return AddressValidation(
            validation=validation,
            messages=messages
        )


class Shipments:
    @staticmethod
    def create(payload: dict, resolve_tracking_url: Callable[[Shipment], str] = None, carrier: models.Carrier = None) -> Shipment:
        selected_rate = next(
            (Rate(**rate) for rate in payload.get('rates') if rate.get('id') == payload.get('selected_rate_id')),
            None
        )

        if selected_rate is None:
            raise NotFound(
                f'Invalid selected_rate_id "{payload.get("selected_rate_id")}" \n '
                f'Please select one of the following: [ {", ".join([r.get("id") for r in payload.get("rates")])} ]'
            )

        carrier = carrier or Carriers.retrieve(carrier_id=selected_rate.carrier_id).data
        request = ShipmentRequest(**{**DP.to_dict(payload), 'service': selected_rate.service})
        gateway = purplship.gateway[carrier.carrier_name].create(carrier.dict())

        # The request is wrapped in identity to simplify mocking in tests
        shipment, messages = identity(lambda: purplship.Shipment.create(request).with_(gateway).parse())

        if shipment is None:
            raise PurplShipApiException(detail=ErrorResponse(messages=messages), status_code=status.HTTP_400_BAD_REQUEST)

        shipment_rate = (
            {**DP.to_dict(shipment.selected_rate), 'id': f'rat_{uuid.uuid4().hex}'}
            if shipment.selected_rate is not None else
            DP.to_dict(selected_rate)
        )

        def generate_tracking_url():
            if resolve_tracking_url is None:
                return ''

            return f"{resolve_tracking_url(shipment)}{'?test' if carrier.test else ''}"

        return Shipment(**{
            **payload,
            **DP.to_dict(shipment),
            "id": f"shp_{uuid.uuid4().hex}",
            "test_mode": carrier.test,
            "selected_rate": shipment_rate,
            "service": shipment_rate["service"],
            "selected_rate_id": shipment_rate["id"],
            "tracking_url": generate_tracking_url(),
            "status": ShipmentStatus.purchased.value,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f%z"),
            "messages": messages
        })

    @staticmethod
    def cancel(payload: dict, carrier_filter: dict = None, carrier: models.Carrier = None) -> ConfirmationResponse:
        carrier = carrier or next(iter(Carriers.list(**{**(carrier_filter or {}), 'active': True})), None)

        if carrier is None:
            raise NotFound('No configured and active carrier found')

        request = purplship.Shipment.cancel(ShipmentCancelRequest(**payload))
        gateway = purplship.gateway[carrier.data.carrier_name].create(carrier.data.dict())

        # The request call is wrapped in identity to simplify mocking in tests
        confirmation, messages = identity(lambda: request.from_(gateway).parse())

        if confirmation is None:
            raise PurplShipApiException(detail=ErrorResponse(messages=messages), status_code=status.HTTP_400_BAD_REQUEST)

        return ConfirmationResponse(
            confirmation=confirmation,
            messages=messages
        )

    @staticmethod
    def track(payload: dict, carrier_filter: dict = None, carrier: models.Carrier = None) -> TrackingResponse:
        carrier = carrier or next(iter(Carriers.list(**{**(carrier_filter or {}), 'active': True})), None)

        if carrier is None:
            raise NotFound('No configured and active carrier found')

        request = purplship.Tracking.fetch(TrackingRequest(**DP.to_dict(payload)))
        gateway = purplship.gateway[carrier.data.carrier_name].create(carrier.data.dict())

        # The request call is wrapped in identity to simplify mocking in tests
        results, messages = identity(lambda: request.from_(gateway).parse())

        if any(messages or []) and not any(results or []):
            raise PurplShipApiException(detail=ErrorResponse(messages=messages), status_code=status.HTTP_404_NOT_FOUND)

        return TrackingResponse(
            tracking=Tracking(**{
                **DP.to_dict(results[0]),
                'id': f'trk_{uuid.uuid4().hex}',
                'test_mode': carrier.test,
            }),
            messages=messages
        )


class Pickups:
    @staticmethod
    def schedule(payload: dict, carrier_filter: dict = None, carrier: models.Carrier = None) -> PickupResponse:
        carrier = carrier or next(iter(Carriers.list(**{**(carrier_filter or {}), 'active': True})), None)

        if carrier is None:
            raise NotFound('No configured and active carrier found')

        request = purplship.Pickup.schedule(PickupRequest(**DP.to_dict(payload)))
        gateway = purplship.gateway[carrier.data.carrier_name].create(carrier.data.dict())

        # The request call is wrapped in identity to simplify mocking in tests
        pickup, messages = identity(lambda: request.with_(gateway).parse())

        if pickup is None:
            raise PurplShipApiException(detail=ErrorResponse(messages=messages), status_code=status.HTTP_400_BAD_REQUEST)

        return PickupResponse(
            pickup=Pickup(**{
                **payload,
                **DP.to_dict(pickup),
                'id': f'pck_{uuid.uuid4().hex}',
                'test_mode': carrier.test,
            }),
            messages=messages
        )

    @staticmethod
    def update(payload: dict, carrier_filter: dict = None, carrier: models.Carrier = None) -> PickupResponse:
        carrier = carrier or next(iter(Carriers.list(**{**(carrier_filter or {}), 'active': True})), None)

        if carrier is None:
            raise NotFound('No configured and active carrier found')

        request = purplship.Pickup.update(PickupUpdateRequest(**DP.to_dict(payload)))
        gateway = purplship.gateway[carrier.data.carrier_name].create(carrier.data.dict())

        # The request call is wrapped in identity to simplify mocking in tests
        pickup, messages = identity(lambda: request.from_(gateway).parse())

        if pickup is None:
            raise PurplShipApiException(detail=ErrorResponse(messages=messages), status_code=status.HTTP_400_BAD_REQUEST)

        return PickupResponse(
            pickup=Pickup(**{
                **payload,
                **DP.to_dict(pickup),
                'test_mode': carrier.test,
            }),
            messages=messages
        )

    @staticmethod
    def cancel(payload: dict, carrier_filter: dict = None, carrier: models.Carrier = None) -> ConfirmationResponse:
        carrier = carrier or next(iter(Carriers.list(**{**(carrier_filter or {}), 'active': True})), None)
        print(carrier)
        if carrier is None:
            raise NotFound('No configured and active carrier found')

        request = purplship.Pickup.cancel(PickupCancelRequest(**DP.to_dict(payload)))
        gateway = purplship.gateway[carrier.data.carrier_name].create(carrier.data.dict())

        # The request call is wrapped in identity to simplify mocking in tests
        confirmation, messages = identity(lambda: request.from_(gateway).parse())

        if confirmation is None:
            raise PurplShipApiException(detail=ErrorResponse(messages=messages), status_code=status.HTTP_400_BAD_REQUEST)

        return ConfirmationResponse(
            confirmation=confirmation,
            messages=messages
        )


@post_processing(methods=['fetch'])
class Rates:
    post_process_functions: List[Callable] = []

    @staticmethod
    def fetch(payload: dict, user = None) -> RateResponse:
        request = purplship.Rating.fetch(RateRequest(**DP.to_dict(payload)))

        carrier_settings_list = [
            carrier.data for carrier in Carriers.list(carrier_ids=payload.get('carrier_ids', []), active=True, user=user)
        ]

        if len(carrier_settings_list) == 0:
            raise NotFound("No configured and active carriers specified")

        gateways = (purplship.gateway[c.carrier_name].create(c.dict()) for c in carrier_settings_list)

        # The request call is wrapped in identity to simplify mocking in tests
        rates, messages = identity(lambda: request.from_(*gateways).parse())

        if not any(rates) and any(messages):
            raise PurplShipApiException(detail=ErrorResponse(messages=messages), status_code=status.HTTP_400_BAD_REQUEST)

        def consolidate_rate(rate: Rate) -> Rate:
            carrier = next((c for c in carrier_settings_list if c.carrier_id == rate.carrier_id))
            return Rate(**{
                'id': f'rat_{uuid.uuid4().hex}',
                'carrier_ref': carrier.id,
                'test_mode': carrier.test,
                **DP.to_dict(rate)
            })

        rates: List[Rate] = sorted(map(consolidate_rate, rates), key=lambda rate: rate.total_charge)

        return RateResponse(
            rates=sorted(rates, key=lambda rate: rate.total_charge),
            messages=messages
        )
