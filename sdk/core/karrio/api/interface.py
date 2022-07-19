"""The Fluent API Abstraction and interfaces definitions."""

import attr
import logging
import functools
from typing import Callable, TypeVar, Union, List, Tuple
from karrio.api.gateway import Gateway
from karrio.core.utils import Serializable, Deserializable, DP, exec_async
from karrio.core.errors import ShippingSDKDetailedError
from karrio.core.models import (
    AddressValidationRequest,
    RateRequest,
    ShipmentRequest,
    TrackingRequest,
    PickupRequest,
    PickupCancelRequest,
    PickupUpdateRequest,
    Message,
    ShipmentCancelRequest,
)

logger = logging.getLogger(__name__)

T = TypeVar("T")
S = TypeVar("S")


def abort(
    error: ShippingSDKDetailedError, gateway: Gateway
) -> Tuple[None, List[Message]]:
    """Process aborting helper

    Args:
        error (ShippingSDKDetailedError): the karrioror raised during the process
        gateway (Gateway): the gateway in use during on process

    Returns:
        Tuple[None, List[Message]]: a tuple of empty response and a list or error messages
    """
    return (
        None,
        [
            Message(
                code=(
                    error.code
                    if hasattr(error, "code")
                    else ShippingSDKDetailedError.code
                ),
                carrier_name=gateway.settings.carrier_name,
                carrier_id=gateway.settings.carrier_id,
                message=f"{error}",
                details=error.details if hasattr(error, "details") else None,
            )
        ],
    )


def fail_safe(gateway: Gateway):
    """Decorate operation and requests calls to enrich any failure context

    Args:
        gateway (Gateway): The gateway in use

    Returns:
        Decorator
    """

    def catcher(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as error:
                logger.exception(error)

                return IDeserialize(
                    functools.partial(abort, gateway=gateway, error=error)
                )

        return wrapper

    return catcher


def check_operation(gateway: Gateway, request: str, **kwargs):
    errors = gateway.check(request, **kwargs)

    if any(errors):
        return False, IDeserialize(lambda: (None, errors))  # type: ignore

    return True, None


@attr.s(auto_attribs=True)
class IDeserialize:
    """A lazy deserializer type class"""

    deserialize: Callable[[], S]

    def parse(self):
        """Execute the response deserialization"""
        result = self.deserialize()
        if isinstance(result, IDeserialize):
            return result.parse()
        return result


@attr.s(auto_attribs=True)
class IRequestFrom:
    """A lazy request (from) type class"""

    action: Callable[[Gateway], IDeserialize]

    def from_(self, gateway: Gateway) -> IDeserialize:
        """Execute the request action from the provided gateway"""
        return fail_safe(gateway)(self.action)(gateway)


@attr.s(auto_attribs=True)
class IRequestFromMany:
    """A lazy request (from one or many) type class"""

    action: Callable[[List[Gateway]], IDeserialize]

    def from_(self, *gateways: Gateway) -> IDeserialize:
        """Execute the request action(s) from the provided gateway(s)"""
        return self.action(list(gateways))


class Address:
    """The unified Address API fluent interface"""

    @staticmethod
    def validate(args: Union[AddressValidationRequest, dict]) -> IRequestFrom:
        """Validate an address

        Args:
            args (Union[TrackingRequest, dict]): the address validation validation request payload

        Returns:
            IRequestFrom: a lazy request dataclass instance
        """
        logger.debug(f"validate an address. payload: {DP.jsonify(args)}")
        payload = (
            args
            if isinstance(args, AddressValidationRequest)
            else AddressValidationRequest(**args)
        )

        def action(gateway: Gateway) -> IDeserialize:
            is_valid, abortion = check_operation(gateway, "validate_address")
            if not is_valid:
                return abortion

            request: Serializable = gateway.mapper.create_address_validation_request(
                payload
            )
            response: Deserializable = gateway.proxy.validate_address(request)

            @fail_safe(gateway)
            def deserialize():
                return gateway.mapper.parse_address_validation_response(response)

            return IDeserialize(deserialize)

        return IRequestFrom(action)


class Pickup:
    """The unified Pickup API fluent interface"""

    @staticmethod
    def schedule(args: Union[PickupRequest, dict]) -> IRequestFrom:
        """Schedule a pickup for one or many shipments

        Args:
            args (Union[TrackingRequest, dict]): the pickup schedule request payload

        Returns:
            IRequestWith: a lazy request dataclass instance
        """
        logger.debug(f"book a pickup. payload: {DP.jsonify(args)}")
        payload = args if isinstance(args, PickupRequest) else PickupRequest(**args)

        def action(gateway: Gateway):
            is_valid, abortion = check_operation(gateway, "schedule_pickup")
            if not is_valid:
                return abortion

            request: Serializable = gateway.mapper.create_pickup_request(payload)
            response: Deserializable = gateway.proxy.schedule_pickup(request)

            @fail_safe(gateway)
            def deserialize():
                return gateway.mapper.parse_pickup_response(response)

            return IDeserialize(deserialize)

        return IRequestFrom(action)

    @staticmethod
    def cancel(args: Union[PickupCancelRequest, dict]) -> IRequestFrom:
        """Cancel a pickup previously scheduled

        Args:
            args (Union[TrackingRequest, dict]): the pickup cancellation request payload

        Returns:
            IRequestFrom: a lazy request dataclass instance
        """
        logger.debug(f"cancel a pickup. payload: {DP.jsonify(args)}")
        payload = (
            args
            if isinstance(args, PickupCancelRequest)
            else PickupCancelRequest(**args)
        )

        def action(gateway: Gateway):
            is_valid, abortion = check_operation(gateway, "cancel_pickup")
            if not is_valid:
                return abortion

            request: Serializable = gateway.mapper.create_cancel_pickup_request(payload)
            response: Deserializable = gateway.proxy.cancel_pickup(request)

            @fail_safe(gateway)
            def deserialize():
                return gateway.mapper.parse_cancel_pickup_response(response)

            return IDeserialize(deserialize)

        return IRequestFrom(action)

    @staticmethod
    def update(args: Union[PickupUpdateRequest, dict]):
        """Update a pickup previously scheduled

        Args:
            args (Union[TrackingRequest, dict]): the pickup update request payload

        Returns:
            IRequestFrom: a lazy request dataclass instance
        """
        logger.debug(f"update a pickup. payload: {DP.jsonify(args)}")
        payload = (
            args
            if isinstance(args, PickupUpdateRequest)
            else PickupUpdateRequest(**args)
        )

        def action(gateway: Gateway):
            is_valid, abortion = check_operation(gateway, "modify_pickup")
            if not is_valid:
                return abortion

            request: Serializable = gateway.mapper.create_pickup_update_request(payload)
            response: Deserializable = gateway.proxy.modify_pickup(request)

            @fail_safe(gateway)
            def deserialize():
                return gateway.mapper.parse_pickup_update_response(response)

            return IDeserialize(deserialize)

        return IRequestFrom(action)


class Rating:
    """The unified Rating API fluent interface"""

    @staticmethod
    def fetch(args: Union[RateRequest, dict]) -> IRequestFromMany:
        """Fetch shipment rates from one or many carriers

        Args:
            args (Union[TrackingRequest, dict]): the rate fetching request payload

        Returns:
            IRequestFromMany: a lazy request dataclass instance
        """
        logger.debug(f"fetch shipment rates. payload: {DP.jsonify(args)}")
        payload = args if isinstance(args, RateRequest) else RateRequest(**args)

        def action(gateways: List[Gateway]):
            def process(gateway: Gateway):
                is_valid, abortion = check_operation(
                    gateway,
                    "get_rates",
                    origin_country_code=payload.shipper.country_code,
                )
                if not is_valid:
                    return abortion

                request: Serializable = gateway.mapper.create_rate_request(payload)
                response: Deserializable = gateway.proxy.get_rates(request)

                @fail_safe(gateway)
                def deserialize():
                    return gateway.mapper.parse_rate_response(response)

                return IDeserialize(deserialize)

            deserializable_collection: List[IDeserialize] = exec_async(
                lambda g: fail_safe(g)(process)(g), gateways
            )

            def flatten():
                responses = [p.parse() for p in deserializable_collection]
                flattened_rates = sum((r for r, _ in responses if r is not None), [])
                messages = sum((m for _, m in responses), [])
                return flattened_rates, messages

            return IDeserialize(flatten)

        return IRequestFromMany(action)


class Shipment:
    """The unified Shipment API fluent interface"""

    @staticmethod
    def create(args: Union[ShipmentRequest, dict]) -> IRequestFrom:
        """Submit a shipment creation to a carrier.
        This operation is often referred to as Buying a shipping label

        Args:
            args (Union[TrackingRequest, dict]): the shipment creation request payload

        Returns:
            IRequestWith: a lazy request dataclass instance
        """
        logger.debug(f"create a shipment. payload: {DP.jsonify(args)}")
        payload = args if isinstance(args, ShipmentRequest) else ShipmentRequest(**args)

        def action(gateway: Gateway):
            is_valid, abortion = check_operation(
                gateway,
                "create_shipment",
                origin_country_code=payload.shipper.country_code,
            )
            if not is_valid:
                return abortion

            request: Serializable = gateway.mapper.create_shipment_request(payload)
            response: Deserializable = gateway.proxy.create_shipment(request)

            @fail_safe(gateway)
            def deserialize():
                return gateway.mapper.parse_shipment_response(response)

            return IDeserialize(deserialize)

        return IRequestFrom(action)

    @staticmethod
    def cancel(args: Union[ShipmentCancelRequest, dict]) -> IRequestFrom:
        """Cancel a shipment previously created

        Args:
            args (Union[TrackingRequest, dict]): the shipment cancellation request payload

        Returns:
            IRequestFrom: a lazy request dataclass instance
        """
        logger.debug(f"void a shipment. payload: {DP.jsonify(args)}")
        payload = (
            args
            if isinstance(args, ShipmentCancelRequest)
            else ShipmentCancelRequest(**args)
        )

        def action(gateway: Gateway):
            is_valid, abortion = check_operation(gateway, "cancel_shipment")
            if not is_valid:
                return abortion

            request: Serializable = gateway.mapper.create_cancel_shipment_request(
                payload
            )
            response: Deserializable = gateway.proxy.cancel_shipment(request)

            @fail_safe(gateway)
            def deserialize():
                return gateway.mapper.parse_cancel_shipment_response(response)

            return IDeserialize(deserialize)

        return IRequestFrom(action)


class Tracking:
    """The unified Tracking API fluent interface"""

    @staticmethod
    def fetch(args: Union[TrackingRequest, dict]) -> IRequestFrom:
        """Fetch tracking statuses and details from a carrier

        Args:
            args (Union[TrackingRequest, dict]): the tracking request payload

        Returns:
            IRequestFrom: a lazy request dataclass instance
        """
        logger.debug(f"track a shipment. payload: {DP.jsonify(args)}")
        payload = args if isinstance(args, TrackingRequest) else TrackingRequest(**args)

        def action(gateway: Gateway) -> IDeserialize:
            is_valid, abortion = check_operation(gateway, "get_tracking")
            if not is_valid:
                return abortion

            request: Serializable = gateway.mapper.create_tracking_request(payload)
            response: Deserializable = gateway.proxy.get_tracking(request)

            @fail_safe(gateway)
            def deserialize():
                return gateway.mapper.parse_tracking_response(response)

            return IDeserialize(deserialize)

        return IRequestFrom(action)
