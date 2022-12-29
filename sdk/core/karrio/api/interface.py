"""The Fluent API Abstraction and interfaces definitions."""

import attr
import typing
import logging
import functools
import karrio.lib as lib
import karrio.core.errors as errors
import karrio.core.models as models
import karrio.api.gateway as gateway

logger = logging.getLogger(__name__)

T = typing.TypeVar("T")
S = typing.TypeVar("S")


def abort(
    error: errors.ShippingSDKDetailedError, gateway: gateway.Gateway
) -> typing.Tuple[None, typing.List[models.Message]]:
    """Process aborting helper

    Args:
        error (errors.ShippingSDKDetailedError): the karrioror raised during the process
        gateway (gateway.Gateway): the gateway in use during on process

    Returns:
        Tuple[None, List[models.Message]]: a tuple of empty response and a list or error messages
    """
    return (
        None,
        [
            models.Message(
                code=(
                    error.code
                    if hasattr(error, "code")
                    else errors.ShippingSDKDetailedError.code
                ),
                carrier_name=gateway.settings.carrier_name,
                carrier_id=gateway.settings.carrier_id,
                message=f"{error}",
                details=error.details if hasattr(error, "details") else None,
            )
        ],
    )


def fail_safe(gateway: gateway.Gateway):
    """Decorate operation and requests calls to enrich any failure context

    Args:
        gateway (gateway.Gateway): The gateway in use

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


def check_operation(gateway: gateway.Gateway, request: str, **kwargs):
    errors = gateway.check(request, **kwargs)

    if any(errors):
        return False, IDeserialize(lambda: (None, errors))  # type: ignore

    return True, None


@attr.s(auto_attribs=True)
class IDeserialize:
    """A lazy deserializer type class"""

    deserialize: typing.Callable[[typing.Any], S]

    def parse(self):
        """Execute the response deserialization"""
        result = self.deserialize()
        if isinstance(result, IDeserialize):
            return result.parse()
        return result


@attr.s(auto_attribs=True)
class IRequestFrom:
    """A lazy request (from) type class"""

    action: typing.Callable[[gateway.Gateway], IDeserialize]

    def from_(self, gateway: gateway.Gateway) -> IDeserialize:
        """Execute the request action from the provided gateway"""
        return fail_safe(gateway)(self.action)(gateway)


@attr.s(auto_attribs=True)
class IRequestFromMany:
    """A lazy request (from one or many) type class"""

    action: typing.Callable[[typing.List[gateway.Gateway]], IDeserialize]

    def from_(self, *gateways: gateway.Gateway) -> IDeserialize:
        """Execute the request action(s) from the provided gateway(s)"""
        return self.action(list(gateways))


class Address:
    """The unified Address API fluent interface"""

    @staticmethod
    def validate(
        args: typing.Union[models.AddressValidationRequest, dict]
    ) -> IRequestFrom:
        """Validate an address

        Args:
            args (Union[TrackingRequest, dict]): the address validation validation request payload

        Returns:
            IRequestFrom: a lazy request dataclass instance
        """
        logger.debug(f"validate an address. payload: {lib.to_json(args)}")
        payload = lib.to_object(models.AddressValidationRequest, lib.to_dict(args))

        def action(gateway: gateway.Gateway) -> IDeserialize:
            is_valid, abortion = check_operation(gateway, "validate_address")
            if not is_valid:
                return abortion

            request: lib.Serializable = (
                gateway.mapper.create_address_validation_request(payload)
            )
            response: lib.Deserializable = gateway.proxy.validate_address(request)

            @fail_safe(gateway)
            def deserialize():
                return gateway.mapper.parse_address_validation_response(response)

            return IDeserialize(deserialize)

        return IRequestFrom(action)


class Pickup:
    """The unified Pickup API fluent interface"""

    @staticmethod
    def schedule(args: typing.Union[models.PickupRequest, dict]) -> IRequestFrom:
        """Schedule a pickup for one or many shipments

        Args:
            args (Union[TrackingRequest, dict]): the pickup schedule request payload

        Returns:
            IRequestWith: a lazy request dataclass instance
        """
        logger.debug(f"book a pickup. payload: {lib.to_json(args)}")
        payload = lib.to_object(models.PickupRequest, lib.to_dict(args))

        def action(gateway: gateway.Gateway):
            is_valid, abortion = check_operation(gateway, "schedule_pickup")
            if not is_valid:
                return abortion

            request: lib.Serializable = gateway.mapper.create_pickup_request(payload)
            response: lib.Deserializable = gateway.proxy.schedule_pickup(request)

            @fail_safe(gateway)
            def deserialize():
                return gateway.mapper.parse_pickup_response(response)

            return IDeserialize(deserialize)

        return IRequestFrom(action)

    @staticmethod
    def cancel(args: typing.Union[models.PickupCancelRequest, dict]) -> IRequestFrom:
        """Cancel a pickup previously scheduled

        Args:
            args (Union[TrackingRequest, dict]): the pickup cancellation request payload

        Returns:
            IRequestFrom: a lazy request dataclass instance
        """
        logger.debug(f"cancel a pickup. payload: {lib.to_json(args)}")
        payload = lib.to_object(models.PickupCancelRequest, lib.to_dict(args))

        def action(gateway: gateway.Gateway):
            is_valid, abortion = check_operation(gateway, "cancel_pickup")
            if not is_valid:
                return abortion

            request: lib.Serializable = gateway.mapper.create_cancel_pickup_request(
                payload
            )
            response: lib.Deserializable = gateway.proxy.cancel_pickup(request)

            @fail_safe(gateway)
            def deserialize():
                return gateway.mapper.parse_cancel_pickup_response(response)

            return IDeserialize(deserialize)

        return IRequestFrom(action)

    @staticmethod
    def update(args: typing.Union[models.PickupUpdateRequest, dict]):
        """Update a pickup previously scheduled

        Args:
            args (Union[TrackingRequest, dict]): the pickup update request payload

        Returns:
            IRequestFrom: a lazy request dataclass instance
        """
        logger.debug(f"update a pickup. payload: {lib.to_json(args)}")
        payload = lib.to_object(models.PickupUpdateRequest, lib.to_dict(args))

        def action(gateway: gateway.Gateway):
            is_valid, abortion = check_operation(gateway, "modify_pickup")
            if not is_valid:
                return abortion

            request: lib.Serializable = gateway.mapper.create_pickup_update_request(
                payload
            )
            response: lib.Deserializable = gateway.proxy.modify_pickup(request)

            @fail_safe(gateway)
            def deserialize():
                return gateway.mapper.parse_pickup_update_response(response)

            return IDeserialize(deserialize)

        return IRequestFrom(action)


class Rating:
    """The unified Rating API fluent interface"""

    @staticmethod
    def fetch(args: typing.Union[models.RateRequest, dict]) -> IRequestFromMany:
        """Fetch shipment rates from one or many carriers

        Args:
            args (Union[TrackingRequest, dict]): the rate fetching request payload

        Returns:
            IRequestFromMany: a lazy request dataclass instance
        """
        logger.debug(f"fetch shipment rates. payload: {lib.to_json(args)}")
        payload = lib.to_object(models.RateRequest, lib.to_dict(args))

        def action(gateways: typing.List[gateway.Gateway]):
            def process(gateway: gateway.Gateway):
                is_valid, abortion = check_operation(
                    gateway,
                    "get_rates",
                    origin_country_code=payload.shipper.country_code,
                )
                if not is_valid:
                    return abortion

                request: lib.Serializable = gateway.mapper.create_rate_request(payload)
                response: lib.Deserializable = gateway.proxy.get_rates(request)

                @fail_safe(gateway)
                def deserialize():
                    return gateway.mapper.parse_rate_response(response)

                return IDeserialize(deserialize)

            deserializable_collection: typing.List[
                IDeserialize
            ] = lib.run_asynchronously(lambda g: fail_safe(g)(process)(g), gateways)

            def flatten(*args):
                responses = [p.parse() for p in deserializable_collection]
                flattened_rates = sum((r for r, _ in responses if r is not None), [])
                messages = sum((m for _, m in responses), [])
                return flattened_rates, messages

            return IDeserialize(flatten)

        return IRequestFromMany(action)


class Shipment:
    """The unified Shipment API fluent interface"""

    @staticmethod
    def create(args: typing.Union[models.ShipmentRequest, dict]) -> IRequestFrom:
        """Submit a shipment creation to a carrier.
        This operation is often referred to as Buying a shipping label

        Args:
            args (Union[TrackingRequest, dict]): the shipment creation request payload

        Returns:
            IRequestWith: a lazy request dataclass instance
        """
        logger.debug(f"create a shipment. payload: {lib.to_json(args)}")
        payload = lib.to_object(models.ShipmentRequest, lib.to_dict(args))

        def action(gateway: gateway.Gateway):
            is_valid, abortion = check_operation(
                gateway,
                "create_shipment",
                origin_country_code=payload.shipper.country_code,
            )
            if not is_valid:
                return abortion

            request: lib.Serializable = gateway.mapper.create_shipment_request(payload)
            response: lib.Deserializable = gateway.proxy.create_shipment(request)

            @fail_safe(gateway)
            def deserialize():
                return gateway.mapper.parse_shipment_response(response)

            return IDeserialize(deserialize)

        return IRequestFrom(action)

    @staticmethod
    def cancel(args: typing.Union[models.ShipmentCancelRequest, dict]) -> IRequestFrom:
        """Cancel a shipment previously created

        Args:
            args (Union[TrackingRequest, dict]): the shipment cancellation request payload

        Returns:
            IRequestFrom: a lazy request dataclass instance
        """
        logger.debug(f"void a shipment. payload: {lib.to_json(args)}")
        payload = lib.to_object(models.ShipmentCancelRequest, lib.to_dict(args))

        def action(gateway: gateway.Gateway):
            is_valid, abortion = check_operation(gateway, "cancel_shipment")
            if not is_valid:
                return abortion

            request: lib.Serializable = gateway.mapper.create_cancel_shipment_request(
                payload
            )
            response: lib.Deserializable = gateway.proxy.cancel_shipment(request)

            @fail_safe(gateway)
            def deserialize():
                return gateway.mapper.parse_cancel_shipment_response(response)

            return IDeserialize(deserialize)

        return IRequestFrom(action)


class Tracking:
    """The unified Tracking API fluent interface"""

    @staticmethod
    def fetch(args: typing.Union[models.TrackingRequest, dict]) -> IRequestFrom:
        """Fetch tracking statuses and details from a carrier

        Args:
            args (Union[TrackingRequest, dict]): the tracking request payload

        Returns:
            IRequestFrom: a lazy request dataclass instance
        """
        logger.debug(f"track a shipment. payload: {lib.to_json(args)}")
        payload = lib.to_object(models.TrackingRequest, lib.to_dict(args))

        def action(gateway: gateway.Gateway) -> IDeserialize:
            is_valid, abortion = check_operation(gateway, "get_tracking")
            if not is_valid:
                return abortion

            request: lib.Serializable = gateway.mapper.create_tracking_request(payload)
            response: lib.Deserializable = gateway.proxy.get_tracking(request)

            @fail_safe(gateway)
            def deserialize():
                return gateway.mapper.parse_tracking_response(response)

            return IDeserialize(deserialize)

        return IRequestFrom(action)


class Document:
    """The unified Document API fluent interface"""

    @staticmethod
    def upload(args: typing.Union[models.DocumentUploadRequest, dict]) -> IRequestFrom:
        """Submit a shipment document upload to a carrier.
        This operation is often used to upload customs documents to fast track shipment at borders

        Args:
            args (Union[DocumentUploadRequest, dict]): the document upload request payload

        Returns:
            IRequestWith: a lazy request dataclass instance
        """
        logger.debug(f"upload a document. payload: {lib.to_json(args)}")
        payload = lib.to_object(models.DocumentUploadRequest, lib.to_dict(args))

        def action(gateway: gateway.Gateway):
            is_valid, abortion = check_operation(
                gateway,
                "upload_document",
            )
            if not is_valid:
                return abortion

            request: lib.Serializable = gateway.mapper.create_document_upload_request(
                payload
            )
            response: lib.Deserializable = gateway.proxy.upload_document(request)

            @fail_safe(gateway)
            def deserialize():
                return gateway.mapper.parse_document_upload_response(response)

            return IDeserialize(deserialize)

        return IRequestFrom(action)
