"""Interface."""

import attr
from typing import Callable, TypeVar, Dict, Any
from purplship.domain.proxy import Proxy
from purplship.domain.mapper import Mapper
from purplship.domain.Types.models import (
    ShipmentRequest,
    TrackingRequest,
    PickupRequest,
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
    action: Callable[[Proxy, Dict[Any, Any]], IDeserialize]

    def from_(self, proxy: Proxy, defaults: dict = {}) -> IDeserialize:
        return self.action(proxy, defaults)


@attr.s(auto_attribs=True)
class IRequestWith:
    action: Callable[[T, S], IDeserialize]

    def with_(self, proxy: Proxy, defaults: dict = {}) -> IDeserialize:
        return self.action(proxy, defaults)


class pickup:

    @staticmethod
    def book(**args):

        def action(proxy: Proxy, defaults: dict = {}):
            params = dict(**{**defaults, **args})
            payload = PickupRequest(**params)
            mapper: Mapper = proxy.mapper
            request = mapper.create_pickup_request(payload)
            response = proxy.request_pickup(request)

            def deserialize():
                return mapper.parse_pickup_response(response)

            return IDeserialize(deserialize)

        return IRequestWith(action)

    @staticmethod
    def cancel(**args):

        def action(proxy: Proxy, defaults: dict = {}):
            params = dict(**{**defaults, **args})
            payload = PickupCancellationRequest(**params)
            mapper: Mapper = proxy.mapper
            request = mapper.create_pickup_cancellation_request(payload)
            response = proxy.cancel_pickup(request)

            def deserialize():
                return response

            return IDeserialize(deserialize)

        return IRequestFrom(action)

    @staticmethod
    def update(**args):

        def action(proxy: Proxy, defaults: dict = {}):
            params = dict(**{**defaults, **args})
            payload = PickupRequest(**params)
            mapper: Mapper = proxy.mapper
            request = mapper.create_pickup_request(payload)
            response = proxy.modify_pickup(request)

            def deserialize():
                return mapper.parse_pickup_response(response)

            return IDeserialize(deserialize)

        return IRequestFrom(action)


class rating:

    @staticmethod
    def fetch(**args):

        def action(proxy: Proxy, defaults: dict = {}):
            params = dict(**{**defaults, **args})
            payload = ShipmentRequest(**params)
            mapper: Mapper = proxy.mapper
            request = mapper.create_quote_request(payload)
            response = proxy.get_quotes(request)

            def deserialize():
                return mapper.parse_quote_response(response)

            return IDeserialize(deserialize)

        return IRequestFrom(action)


class shipment:

    @staticmethod
    def create(**args):

        def action(proxy: Proxy, defaults: dict = {}):
            params = dict(**{**defaults, **args})
            payload = ShipmentRequest(**params)
            mapper: Mapper = proxy.mapper
            request = mapper.create_shipment_request(payload)
            response = proxy.create_shipment(request)

            def deserialize():
                return mapper.parse_shipment_response(response)

            return IDeserialize(deserialize)

        return IRequestWith(action)


class tracking:

    @staticmethod
    def fetch(**args) -> IRequestFrom:

        def action(proxy: Proxy, defaults: dict = {}) -> IDeserialize:
            params = dict(**{**defaults, **args})
            payload = TrackingRequest(**params)
            mapper: Mapper = proxy.mapper
            request = mapper.create_tracking_request(payload)
            response = proxy.get_trackings(request)

            def deserialize():
                return mapper.parse_tracking_response(response)

            return IDeserialize(deserialize)

        return IRequestFrom(action)
