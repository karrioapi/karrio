"""Interface."""

import attr
import logging
import functools
from typing import Callable, TypeVar, Union
from purplship.package.gateway import Gateway
from purplship.core.utils import Serializable, Deserializable, jsonify
from purplship.core.errors import PurplShipDetailedError
from purplship.core.models import (
    RateRequest,
    ShipmentRequest,
    TrackingRequest,
    PickupRequest,
    PickupCancellationRequest,
    PickupUpdateRequest,
    Message,
)

logger = logging.getLogger(__name__)

T = TypeVar("T")
S = TypeVar("S")


def abort(error: PurplShipDetailedError, gateway: Gateway):
    return (
        None,
        [
            Message(
                code=error.code if hasattr(error, 'code') else PurplShipDetailedError.code,
                carrier_name=gateway.settings.carrier_name,
                carrier_id=gateway.settings.carrier_id,
                message=f"{error}",
                details=error.details if hasattr(error, 'details') else None
            )
        ],
    )


def fail_safe(gateway: Gateway):
    def catcher(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as error:
                logger.exception(error)

                return IDeserialize(functools.partial(abort, gateway=gateway, error=error))
        return wrapper
    return catcher


@attr.s(auto_attribs=True)
class IDeserialize:
    deserialize: Callable[[], S]

    def parse(self):
        result = self.deserialize()
        if isinstance(result, IDeserialize):
            return result.parse()
        return result


@attr.s(auto_attribs=True)
class IRequestFrom:
    action: Callable[[Gateway], IDeserialize]

    def from_(self, gateway: Gateway) -> IDeserialize:
        return fail_safe(gateway)(self.action)(gateway)


@attr.s(auto_attribs=True)
class IRequestWith:
    action: Callable[[Gateway], IDeserialize]

    def with_(self, gateway: Gateway) -> IDeserialize:
        return fail_safe(gateway)(self.action)(gateway)


class Pickup:
    @staticmethod
    def book(args: Union[PickupRequest, dict]):
        logger.debug(f'book a pickup. payload: {jsonify(args)}')
        payload = args if isinstance(args, PickupRequest) else PickupRequest(**args)

        def action(gateway: Gateway):
            request: Serializable = gateway.mapper.create_pickup_request(payload)
            response: Deserializable = gateway.proxy.request_pickup(request)

            @fail_safe(gateway)
            def deserialize():
                return gateway.mapper.parse_pickup_response(response)

            return IDeserialize(deserialize)

        return IRequestWith(action)

    @staticmethod
    def cancel(args: Union[PickupCancellationRequest, dict]):
        logger.debug(f'cancel a pickup. payload: {jsonify(args)}')
        payload = (
            args
            if isinstance(args, PickupCancellationRequest)
            else PickupCancellationRequest(**args)
        )

        def action(gateway: Gateway):
            request: Serializable = gateway.mapper.create_cancel_pickup_request(payload)
            response: Deserializable = gateway.proxy.cancel_pickup(request)

            @fail_safe(gateway)
            def deserialize():
                return gateway.mapper.parse_cancel_pickup_response(response)

            return IDeserialize(deserialize)

        return IRequestFrom(action)

    @staticmethod
    def update(args: Union[PickupUpdateRequest, dict]):
        logger.debug(f'update a pickup. payload: {jsonify(args)}')
        payload = (
            args
            if isinstance(args, PickupUpdateRequest)
            else PickupUpdateRequest(**args)
        )

        def action(gateway: Gateway):
            request: Serializable = gateway.mapper.create_modify_pickup_request(payload)
            response: Deserializable = gateway.proxy.modify_pickup(request)

            @fail_safe(gateway)
            def deserialize():
                return gateway.mapper.parse_modify_pickup_response(response)

            return IDeserialize(deserialize)

        return IRequestFrom(action)


class Rating:
    @staticmethod
    def fetch(args: Union[RateRequest, dict]):
        logger.debug(f'fetch shipment rates. payload: {jsonify(args)}')
        payload = args if isinstance(args, RateRequest) else RateRequest(**args)

        def action(gateway: Gateway):
            request: Serializable = gateway.mapper.create_rate_request(payload)
            response: Deserializable = gateway.proxy.get_rates(request)

            @fail_safe(gateway)
            def deserialize():
                return gateway.mapper.parse_rate_response(response)

            return IDeserialize(deserialize)

        return IRequestFrom(action)


class Shipment:
    @staticmethod
    def create(args: Union[ShipmentRequest, dict]):
        logger.debug(f'create a shipment. payload: {jsonify(args)}')
        payload = (
            args if isinstance(args, ShipmentRequest) else ShipmentRequest(**args)
        )

        def action(gateway: Gateway):
            request: Serializable = gateway.mapper.create_shipment_request(payload)
            response: Deserializable = gateway.proxy.create_shipment(request)

            @fail_safe(gateway)
            def deserialize():
                return gateway.mapper.parse_shipment_response(response)

            return IDeserialize(deserialize)

        return IRequestWith(action)


class Tracking:
    @staticmethod
    def fetch(args: Union[TrackingRequest, dict]) -> IRequestFrom:
        logger.debug(f'track a shipment. payload: {jsonify(args)}')
        payload = (
            args if isinstance(args, TrackingRequest) else TrackingRequest(**args)
        )

        def action(gateway: Gateway) -> IDeserialize:
            request: Serializable = gateway.mapper.create_tracking_request(payload)
            response: Deserializable = gateway.proxy.get_tracking(request)

            @fail_safe(gateway)
            def deserialize():
                return gateway.mapper.parse_tracking_response(response)

            return IDeserialize(deserialize)

        return IRequestFrom(action)
