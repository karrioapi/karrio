"""Interface."""

import attr
from typing import Callable, TypeVar, Union
from purplship.package.gateway import Gateway
from purplship.core.models import (
    RateRequest, ShipmentRequest,
    TrackingRequest, PickupRequest,
    PickupCancellationRequest
)

T = TypeVar('T')
S = TypeVar('S')


@attr.s(auto_attribs=True)
class IDeserialize:
    deserialize: Callable[[], S]

    def parse(self):
        return self.deserialize()


@attr.s(auto_attribs=True)
class IRequestFrom:
    action: Callable[[Gateway], IDeserialize]

    def from_(self, gateway: Gateway) -> IDeserialize:
        return self.action(gateway)


@attr.s(auto_attribs=True)
class IRequestWith:
    action: Callable[[Gateway], IDeserialize]

    def with_(self, gateway: Gateway) -> IDeserialize:
        return self.action(gateway)


class pickup:

    @staticmethod
    def book(args: Union[PickupRequest, dict]):

        def action(gateway: Gateway):
            payload = (
                args if isinstance(args, PickupRequest)
                else PickupRequest(**args)
            )
            request = gateway.mapper.create_pickup_request(payload)
            response = gateway.proxy.request_pickup(request)

            def deserialize():
                return gateway.mapper.parse_pickup_response(response)

            return IDeserialize(deserialize)

        return IRequestWith(action)

    @staticmethod
    def cancel(args: Union[PickupCancellationRequest, dict]):

        def action(gateway: Gateway):
            payload = (
                args if isinstance(args, PickupCancellationRequest)
                else PickupCancellationRequest(**args)
            )
            request = gateway.mapper.create_cancel_pickup_request(payload)
            response = gateway.proxy.cancel_pickup(request)

            def deserialize():
                return response

            return IDeserialize(deserialize)

        return IRequestFrom(action)

    @staticmethod
    def update(args: Union[PickupRequest, dict]):

        def action(gateway: Gateway):
            payload = (
                args if isinstance(args, PickupRequest)
                else PickupRequest(**args)
            )
            request = gateway.mapper.create_pickup_request(payload)
            response = gateway.proxy.modify_pickup(request)

            def deserialize():
                return gateway.mapper.parse_pickup_response(response)

            return IDeserialize(deserialize)

        return IRequestFrom(action)


class rating:

    @staticmethod
    def fetch(args: Union[RateRequest, dict]):

        def action(gateway: Gateway):
            payload = (
                args if isinstance(args, RateRequest)
                else RateRequest(**args)
            )
            request = gateway.mapper.create_rate_request(payload)
            response = gateway.proxy.get_rates(request)

            def deserialize():
                return gateway.mapper.parse_rate_response(response)

            return IDeserialize(deserialize)

        return IRequestFrom(action)


class shipment:

    @staticmethod
    def create(args: Union[ShipmentRequest, dict]):

        def action(gateway: Gateway):
            payload = (
                args if isinstance(args, ShipmentRequest)
                else ShipmentRequest(**args)
            )
            request = gateway.mapper.create_shipment_request(payload)
            response = gateway.proxy.create_shipment(request)

            def deserialize():
                return gateway.mapper.parse_shipment_response(response)

            return IDeserialize(deserialize)

        return IRequestWith(action)


class tracking:

    @staticmethod
    def fetch(args: Union[TrackingRequest, dict]) -> IRequestFrom:

        def action(gateway: Gateway) -> IDeserialize:
            payload = (
                args if isinstance(args, TrackingRequest)
                else TrackingRequest(**args)
            )
            request = gateway.mapper.create_tracking_request(payload)
            response = gateway.proxy.get_tracking(request)

            def deserialize():
                return gateway.mapper.parse_tracking_response(response)

            return IDeserialize(deserialize)

        return IRequestFrom(action)
