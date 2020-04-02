"""Interface."""

import attr
import logging
from typing import Callable, TypeVar, Union
from purplship.freight.gateway import Gateway
from purplship.core.utils.serializable import Serializable, Deserializable
from purplship.core.models import (
    RateRequest,
    ShipmentRequest,
    TrackingRequest,
    PickupRequest,
    PickupCancellationRequest,
    PickupUpdateRequest,
    Message,
)

logger = logging.getLogger("purplship")

T = TypeVar("T")
S = TypeVar("S")


@attr.s(auto_attribs=True)
class IDeserialize:
    deserialize: Callable[[], S]

    def parse(self):
        return self.deserialize()


def abort(gateway: Gateway, error: Exception) -> IDeserialize:
    logger.exception(error)

    def deserialize():
        return (
            [],
            [
                Message(
                    code="500",
                    carrier=gateway.settings.carrier,
                    carrier_name=gateway.settings.carrier_name,
                    message=f"{error}",
                )
            ],
        )

    return IDeserialize(deserialize)


@attr.s(auto_attribs=True)
class IRequestFrom:
    action: Callable[[Gateway], IDeserialize]

    def from_(self, gateway: Gateway) -> IDeserialize:
        try:
            return self.action(gateway)
        except Exception as e:
            return abort(gateway, e)


@attr.s(auto_attribs=True)
class IRequestWith:
    action: Callable[[Gateway], IDeserialize]

    def with_(self, gateway: Gateway) -> IDeserialize:
        try:
            return self.action(gateway)
        except Exception as e:
            return abort(gateway, e)


class Pickup:
    @staticmethod
    def book(args: Union[PickupRequest, dict]):
        payload = args if isinstance(args, PickupRequest) else PickupRequest(**args)

        def action(gateway: Gateway):
            request: Serializable = gateway.mapper.create_pickup_request(payload)
            response: Deserializable = gateway.proxy.request_pickup(request)

            def deserialize():
                return gateway.mapper.parse_pickup_response(response)

            return IDeserialize(deserialize)

        return IRequestWith(action)

    @staticmethod
    def cancel(args: Union[PickupCancellationRequest, dict]):
        payload = (
            args
            if isinstance(args, PickupCancellationRequest)
            else PickupCancellationRequest(**args)
        )

        def action(gateway: Gateway):
            request: Serializable = gateway.mapper.create_cancel_pickup_request(payload)
            response: Deserializable = gateway.proxy.cancel_pickup(request)

            def deserialize():
                return gateway.mapper.parse_cancel_pickup_response(response)

            return IDeserialize(deserialize)

        return IRequestFrom(action)

    @staticmethod
    def update(args: Union[PickupUpdateRequest, dict]):
        payload = (
            args
            if isinstance(args, PickupUpdateRequest)
            else PickupUpdateRequest(**args)
        )

        def action(gateway: Gateway):
            request: Serializable = gateway.mapper.create_modify_pickup_request(payload)
            response: Deserializable = gateway.proxy.modify_pickup(request)

            def deserialize():
                return gateway.mapper.parse_modify_pickup_response(response)

            return IDeserialize(deserialize)

        return IRequestFrom(action)


class Rating:
    @staticmethod
    def fetch(args: Union[RateRequest, dict]):
        payload = args if isinstance(args, RateRequest) else RateRequest(**args)

        def action(gateway: Gateway):
            request: Serializable = gateway.mapper.create_rate_request(payload)
            response: Deserializable = gateway.proxy.get_rates(request)

            def deserialize():
                return gateway.mapper.parse_rate_response(response)

            return IDeserialize(deserialize)

        return IRequestFrom(action)


class Shipment:
    @staticmethod
    def create(args: Union[ShipmentRequest, dict]):
        payload = (
            args if isinstance(args, ShipmentRequest) else ShipmentRequest(**args)
        )

        def action(gateway: Gateway):
            request: Serializable = gateway.mapper.create_shipment_request(payload)
            response: Deserializable = gateway.proxy.create_shipment(request)

            def deserialize():
                return gateway.mapper.parse_shipment_response(response)

            return IDeserialize(deserialize)

        return IRequestWith(action)


class Tracking:
    @staticmethod
    def fetch(args: Union[TrackingRequest, dict]) -> IRequestFrom:
        payload = (
            args if isinstance(args, TrackingRequest) else TrackingRequest(**args)
        )

        def action(gateway: Gateway) -> IDeserialize:
            request: Serializable = gateway.mapper.create_tracking_request(payload)
            response: Deserializable = gateway.proxy.get_tracking(request)

            def deserialize():
                return gateway.mapper.parse_tracking_response(response)

            return IDeserialize(deserialize)

        return IRequestFrom(action)
