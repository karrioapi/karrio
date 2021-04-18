import uuid
import logging
from datetime import datetime
from typing import List, Callable, Dict, Any

from django.db.models import Q
from rest_framework import status
from rest_framework.exceptions import NotFound, ValidationError

import purplship
from purplship.core.utils import DP

from purpleserver.providers import models
from purpleserver.core.models import get_access_filter
from purpleserver.core import datatypes, serializers, exceptions, validators
from purpleserver.core.utils import identity, post_processing

logger = logging.getLogger(__name__)


class Carriers:
    @staticmethod
    def list(**kwargs) -> List[models.Carrier]:
        list_filter: Dict[str: Any] = kwargs
        query = tuple()

        # Check if the system_only flag is not specified and there is a provided user, get the users carriers
        if not list_filter.get('system_only') and 'user' in list_filter:
            access = get_access_filter(list_filter.get('user'))
            if len(access) > 0:
                query += (Q(created_by__isnull=True) | access,)

        if list_filter.get('system_only') is True:
            query += (Q(created_by__isnull=True),)

        # Check if the test filter is specified then set it otherwise return all carriers prod and test mode
        if list_filter.get('test') is not None:
            query += (Q(test=list_filter['test']), )

        # Check if the active flag is specified and return all active carrier is active is not set to false
        if list_filter.get('active') is not None:
            active = False if list_filter['active'] is False else True
            query += (Q(active=active), )

        # Check if a specific carrier_id is provide, to add it to the query
        if 'carrier_id' in list_filter:
            query += (Q(carrier_id=list_filter['carrier_id']), )

        # Check if a list of carrier_ids are provided, to add the list to the query
        if any(list_filter.get('carrier_ids', [])):
            query += (Q(carrier_id__in=list_filter['carrier_ids']), )

        if 'carrier_name' in list_filter:
            carrier_name = list_filter['carrier_name']
            if carrier_name not in models.MODELS.keys():
                raise NotFound(f"No configurations for the following carrier: '{carrier_name}'")

            carriers = [
                setting.carrier_ptr for setting in models.MODELS[carrier_name].objects.filter(*query)
            ]
        else:
            carriers = models.Carrier.objects.filter(*query)

        return carriers


class Address:
    @staticmethod
    def validate(payload: dict) -> datatypes.AddressValidation:
        # Currently only support GoogleGeocode validation. Refactor this for other methods
        validation = validators.GoogleGeocode.validate(datatypes.Address(**payload))

        if validation.success is False:
            raise ValidationError(detail="Invalid Address")

        return validation


class Shipments:
    @staticmethod
    def create(payload: dict, resolve_tracking_url: Callable[[datatypes.Shipment], str] = None, carrier: models.Carrier = None) -> datatypes.Shipment:
        selected_rate = next(
            (datatypes.Rate(**rate) for rate in payload.get('rates') if rate.get('id') == payload.get('selected_rate_id')),
            None
        )

        if selected_rate is None:
            raise NotFound(
                f'Invalid selected_rate_id "{payload.get("selected_rate_id")}" \n '
                f'Please select one of the following: [ {", ".join([r.get("id") for r in payload.get("rates")])} ]'
            )

        carrier = carrier or models.Carrier.objects.get(carrier_id=selected_rate.carrier_id).data
        request = datatypes.ShipmentRequest(**{**DP.to_dict(payload), 'service': selected_rate.service})
        gateway = purplship.gateway[carrier.carrier_name].create(carrier.dict())

        # The request is wrapped in identity to simplify mocking in tests
        shipment, messages = identity(lambda: purplship.Shipment.create(request).from_(gateway).parse())

        if shipment is None:
            raise exceptions.PurplShipApiException(detail=datatypes.ErrorResponse(messages=messages), status_code=status.HTTP_400_BAD_REQUEST)

        shipment_rate = (
            {**DP.to_dict(shipment.selected_rate), 'id': f'rat_{uuid.uuid4().hex}'}
            if shipment.selected_rate is not None else
            DP.to_dict(selected_rate)
        )

        def generate_tracking_url():
            if resolve_tracking_url is None:
                return ''

            return f"{resolve_tracking_url(shipment)}{'?test' if carrier.test else ''}"

        return datatypes.Shipment(**{
            **payload,
            **DP.to_dict(shipment),
            "id": f"shp_{uuid.uuid4().hex}",
            "test_mode": carrier.test,
            "selected_rate": shipment_rate,
            "service": shipment_rate["service"],
            "selected_rate_id": shipment_rate["id"],
            "tracking_url": generate_tracking_url(),
            "status": serializers.ShipmentStatus.purchased.value,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f%z"),
            "messages": messages
        })

    @staticmethod
    def cancel(payload: dict, carrier_filter: dict = None, carrier: models.Carrier = None) -> datatypes.ConfirmationResponse:
        carrier = carrier or next(iter(Carriers.list(**{**(carrier_filter or {}), 'active': True})), None)

        if carrier is None:
            raise NotFound('No configured and active carrier found')

        request = purplship.Shipment.cancel(datatypes.ShipmentCancelRequest(**payload))
        gateway = purplship.gateway[carrier.data.carrier_name].create(carrier.data.dict())

        # The request call is wrapped in identity to simplify mocking in tests
        confirmation, messages = identity(lambda: request.from_(gateway).parse())

        if confirmation is None:
            raise exceptions.PurplShipApiException(detail=datatypes.ErrorResponse(messages=messages), status_code=status.HTTP_400_BAD_REQUEST)

        return datatypes.ConfirmationResponse(
            confirmation=confirmation,
            messages=messages
        )

    @staticmethod
    def track(payload: dict, carrier_filter: dict = None, carrier: models.Carrier = None) -> datatypes.TrackingResponse:
        carrier = carrier or next(iter(Carriers.list(**{**(carrier_filter or {}), 'active': True})), None)

        if carrier is None:
            raise NotFound('No configured and active carrier found')

        request = purplship.Tracking.fetch(datatypes.TrackingRequest(**DP.to_dict(payload)))
        gateway = purplship.gateway[carrier.data.carrier_name].create(carrier.data.dict())

        # The request call is wrapped in identity to simplify mocking in tests
        results, messages = identity(lambda: request.from_(gateway).parse())

        if any(messages or []) and not any(results or []):
            raise exceptions.PurplShipApiException(detail=datatypes.ErrorResponse(messages=messages), status_code=status.HTTP_404_NOT_FOUND)

        return datatypes.TrackingResponse(
            tracking=(datatypes.Tracking(**{
                **DP.to_dict(results[0]),
                'id': f'trk_{uuid.uuid4().hex}',
                'test_mode': carrier.test,
            }) if any(results) else None),
            messages=messages
        )


class Pickups:
    @staticmethod
    def schedule(payload: dict, carrier_filter: dict = None, carrier: models.Carrier = None) -> datatypes.PickupResponse:
        carrier = carrier or next(iter(Carriers.list(**{**(carrier_filter or {}), 'active': True})), None)

        if carrier is None:
            raise NotFound('No configured and active carrier found')

        request = purplship.Pickup.schedule(datatypes.PickupRequest(**DP.to_dict(payload)))
        gateway = purplship.gateway[carrier.data.carrier_name].create(carrier.data.dict())

        # The request call is wrapped in identity to simplify mocking in tests
        pickup, messages = identity(lambda: request.from_(gateway).parse())

        if pickup is None:
            raise exceptions.PurplShipApiException(detail=datatypes.ErrorResponse(messages=messages), status_code=status.HTTP_400_BAD_REQUEST)

        return datatypes.PickupResponse(
            pickup=datatypes.Pickup(**{
                **payload,
                **DP.to_dict(pickup),
                'id': f'pck_{uuid.uuid4().hex}',
                'test_mode': carrier.test,
            }),
            messages=messages
        )

    @staticmethod
    def update(payload: dict, carrier_filter: dict = None, carrier: models.Carrier = None) -> datatypes.PickupResponse:
        carrier = carrier or next(iter(Carriers.list(**{**(carrier_filter or {}), 'active': True})), None)

        if carrier is None:
            raise NotFound('No configured and active carrier found')

        request = purplship.Pickup.update(datatypes.PickupUpdateRequest(**DP.to_dict(payload)))
        gateway = purplship.gateway[carrier.data.carrier_name].create(carrier.data.dict())

        # The request call is wrapped in identity to simplify mocking in tests
        pickup, messages = identity(lambda: request.from_(gateway).parse())

        if pickup is None:
            raise exceptions.PurplShipApiException(detail=datatypes.ErrorResponse(messages=messages), status_code=status.HTTP_400_BAD_REQUEST)

        return datatypes.PickupResponse(
            pickup=datatypes.Pickup(**{
                **payload,
                **DP.to_dict(pickup),
                'test_mode': carrier.test,
            }),
            messages=messages
        )

    @staticmethod
    def cancel(payload: dict, carrier_filter: dict = None, carrier: models.Carrier = None) -> datatypes.ConfirmationResponse:
        carrier = carrier or next(iter(Carriers.list(**{**(carrier_filter or {}), 'active': True})), None)

        if carrier is None:
            raise NotFound('No configured and active carrier found')

        request = purplship.Pickup.cancel(datatypes.PickupCancelRequest(**DP.to_dict(payload)))
        gateway = purplship.gateway[carrier.data.carrier_name].create(carrier.data.dict())

        # The request call is wrapped in identity to simplify mocking in tests
        confirmation, messages = identity(lambda: request.from_(gateway).parse())

        if confirmation is None:
            raise exceptions.PurplShipApiException(detail=datatypes.ErrorResponse(messages=messages), status_code=status.HTTP_400_BAD_REQUEST)

        return datatypes.ConfirmationResponse(
            confirmation=confirmation,
            messages=messages
        )


@post_processing(methods=['fetch'])
class Rates:
    post_process_functions: List[Callable] = []

    @staticmethod
    def fetch(payload: dict, user=None) -> datatypes.RateResponse:
        request = purplship.Rating.fetch(datatypes.RateRequest(**DP.to_dict(payload)))

        carrier_settings_list = [
            carrier.data for carrier in Carriers.list(carrier_ids=payload.get('carrier_ids', []), active=True, user=user)
        ]
        gateways = [
            purplship.gateway[c.carrier_name].create(c.dict()) for c in carrier_settings_list
        ]
        compatible_gateways = [g for g in gateways if 'get_rates' in g.features]

        if len(compatible_gateways) == 0:
            raise NotFound("No configured and active carriers specified")

        # The request call is wrapped in identity to simplify mocking in tests
        rates, messages = identity(lambda: request.from_(*compatible_gateways).parse())

        if not any(rates) and any(messages):
            raise exceptions.PurplShipApiException(detail=datatypes.ErrorResponse(messages=messages), status_code=status.HTTP_400_BAD_REQUEST)

        def consolidate_rate(rate: datatypes.Rate) -> datatypes.Rate:
            carrier = next((c for c in carrier_settings_list if c.carrier_id == rate.carrier_id))
            return datatypes.Rate(**{
                'id': f'rat_{uuid.uuid4().hex}',
                'carrier_ref': carrier.id,
                'test_mode': carrier.test,
                **DP.to_dict(rate)
            })

        rates: List[datatypes.Rate] = sorted(map(consolidate_rate, rates), key=lambda rate: rate.total_charge)

        return datatypes.RateResponse(
            rates=sorted(rates, key=lambda rate: rate.total_charge),
            messages=messages
        )
