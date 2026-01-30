"""The Fluent API Abstraction and interfaces definitions."""

import attr
import typing
import functools
import karrio.lib as lib
import karrio.core.errors as errors
import karrio.core.models as models
import karrio.api.gateway as gateway
from karrio.core.utils.logger import logger
from karrio.universal.mappers.rating_proxy import RatingMixinProxy
from karrio.universal.providers.rating import (
    RatingMixinSettings,
    parse_rate_response,
)

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

    if isinstance(error, errors.ParsedMessagesError):
        return None, error.messages

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
                logger.exception(
                    "Operation failed", carrier=gateway.settings.carrier_name
                )

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


def filter_rates(rates: typing.List[models.RateDetails], gateway: gateway.Gateway):
    """Filter rates by gateway

    Args:
        rates (List[models.Rate]): the rates to filter
        gateways (List[gateway.Gateway]): the gateways to filter by

    Returns:
        List[models.Rate]: the filtered rates
    """
    restricted_services = (
        gateway.settings.connection_config.shipping_services.state or []
    )

    return [
        rate
        for rate in rates
        if (not any(restricted_services) or rate.service in restricted_services)
    ]


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
        return self.action(list({_.settings.carrier_id: _ for _ in gateways}.values()))


def _is_rating_compatible(obj) -> bool:
    """Check if object is duck-type compatible with RatingMixinProxy requirements."""
    return all(hasattr(obj, attr) for attr in ["carrier_id", "shipping_services"])


@attr.s(auto_attribs=True)
class IResolveFromMany:
    """A lazy resolve (from rate sheet settings) type class for static rate resolution."""

    action: typing.Callable[[typing.List[typing.Any]], IDeserialize]

    def from_(self, *carrier_settings) -> IDeserialize:
        """Resolve rates using provided carrier settings with rate sheet data.

        Args:
            carrier_settings: One or more carrier settings objects with:
                - carrier_id, carrier_name (optional), account_country_code (optional)
                - shipping_services: List of ServiceLevel with zones/surcharges

        Returns:
            IDeserialize: Lazy deserializer with (rates, messages) tuple
        """
        # Filter to only include settings that are duck-type compatible
        settings_list = [s for s in carrier_settings if _is_rating_compatible(s)]
        # Deduplicate by carrier_id
        unique_settings = list({s.carrier_id: s for s in settings_list}.values())
        return self.action(unique_settings)


class Address:
    """The unified Address API fluent interface"""

    @staticmethod
    def validate(
        args: typing.Union[models.AddressValidationRequest, dict],
    ) -> IRequestFrom:
        """Validate an address

        Args:
            args (Union[TrackingRequest, dict]): the address validation validation request payload

        Returns:
            IRequestFrom: a lazy request dataclass instance
        """
        logger.debug("Validating address", payload=lib.to_dict(args))
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
        logger.debug("Scheduling pickup", payload=lib.to_dict(args))
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
        logger.debug("Canceling pickup", payload=lib.to_dict(args))
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
        logger.debug("Updating pickup", payload=lib.to_dict(args))
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
        logger.debug("Fetching shipment rates", payload=lib.to_dict(args))
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

            deserializable_collection: typing.List[IDeserialize] = (
                lib.run_asynchronously(lambda g: fail_safe(g)(process)(g), gateways)
            )

            def flatten(*args):
                responses = [p.parse() for p in deserializable_collection]
                flattened_rates = sum(
                    (
                        (
                            (lambda gateway: filter_rates(rates, gateway))(
                                # find the gateway that matches the carrier_id of the rates
                                next(
                                    (
                                        g
                                        for g in gateways
                                        if (
                                            g.settings.carrier_id == rates[0].carrier_id
                                        )
                                    )
                                )
                            )
                            if len(rates) > 0
                            else rates
                        )
                        for rates, _ in responses
                        if rates is not None
                    ),
                    [],
                )
                messages = sum((m for _, m in responses), [])
                return flattened_rates, messages

            return IDeserialize(flatten)

        return IRequestFromMany(action)

    @staticmethod
    def resolve(args: typing.Union[models.RateRequest, dict]) -> IResolveFromMany:
        """Resolve shipment rates from static rate sheets (no API calls).

        Unlike fetch(), this method uses rate sheet data directly without
        calling carrier APIs. It requires carrier settings with services
        containing zones and surcharges.

        Args:
            args (Union[RateRequest, dict]): the rate request payload

        Returns:
            IResolveFromMany: a lazy resolve dataclass instance
        """
        logger.debug("Resolving shipment rates from rate sheets", payload=lib.to_dict(args))
        payload = lib.to_object(models.RateRequest, lib.to_dict(args))

        def action(settings_list: typing.List[RatingMixinSettings]):
            def process(settings: RatingMixinSettings):
                try:
                    proxy = RatingMixinProxy(settings=settings)
                    request: lib.Serializable = lib.Serializable(payload)
                    response = proxy.get_rates(request)
                    return parse_rate_response(response, settings)
                except Exception as error:
                    logger.exception(
                        "Rate resolution failed", carrier=settings.carrier_name
                    )
                    return (
                        None,
                        [
                            models.Message(
                                code="SHIPPING_SDK_RESOLVE_ERROR",
                                carrier_name=settings.carrier_name,
                                carrier_id=settings.carrier_id,
                                message=f"{error}",
                            )
                        ],
                    )

            responses: typing.List[typing.Any] = lib.run_asynchronously(process, settings_list)

            def flatten(*args):
                flattened_rates = sum(
                    (rates for rates, _ in responses if rates is not None),
                    [],
                )
                messages = sum((m for _, m in responses), [])
                return flattened_rates, messages

            return IDeserialize(flatten)

        return IResolveFromMany(action)


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
        logger.debug("Creating shipment", payload=lib.to_dict(args))
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
        logger.debug("Canceling shipment", payload=lib.to_dict(args))
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
        logger.debug("Tracking shipment", payload=lib.to_dict(args))
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
        logger.debug("Uploading document", payload=lib.to_dict(args))
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


class Manifest:
    """The unified Manifest API fluent interface"""

    @staticmethod
    def create(args: typing.Union[models.ManifestRequest, dict]) -> IRequestFrom:
        """Submit a manifest creation to a carrier.
        This operation is often referred to as manifesting a batch of shipments

        Args:
            args (Union[ManifestRequest, dict]): the manifest creation request payload

        Returns:
            IRequestWith: a lazy request dataclass instance
        """
        logger.debug("Creating manifest", payload=lib.to_dict(args))
        payload = lib.to_object(models.ManifestRequest, lib.to_dict(args))

        def action(gateway: gateway.Gateway):
            is_valid, abortion = check_operation(
                gateway,
                "create_manifest",
            )
            if not is_valid:
                return abortion

            request: lib.Serializable = gateway.mapper.create_manifest_request(payload)
            response: lib.Deserializable = gateway.proxy.create_manifest(request)

            @fail_safe(gateway)
            def deserialize():
                return gateway.mapper.parse_manifest_response(response)

            return IDeserialize(deserialize)

        return IRequestFrom(action)


class Duties:
    """The unified Duties API fluent interface"""

    @staticmethod
    def calculate(
        args: typing.Union[models.DutiesCalculationRequest, dict],
    ) -> IRequestFrom:
        """Calculate duties for a shipment

        Args:
            args (Union[DutiesCalculationRequest, dict]): the duties calculation request payload

        Returns:
            IRequestFrom: a lazy request dataclass instance
        """
        logger.debug("Calculating duties", payload=lib.to_dict(args))
        payload = lib.to_object(models.DutiesCalculationRequest, lib.to_dict(args))

        def action(gateway: gateway.Gateway) -> IDeserialize:
            is_valid, abortion = check_operation(gateway, "calculate_duties")
            if not is_valid:
                return abortion

            request: lib.Serializable = (
                gateway.mapper.create_duties_calculation_request(payload)
            )
            response: lib.Deserializable = gateway.proxy.calculate_duties(request)

            @fail_safe(gateway)
            def deserialize():
                return gateway.mapper.parse_duties_calculation_response(response)

            return IDeserialize(deserialize)

        return IRequestFrom(action)


class Insurance:
    """The unified Insurance API fluent interface"""

    @staticmethod
    def apply(args: typing.Union[models.InsuranceRequest, dict]) -> IRequestFrom:
        """Apply insurance coverage to a package

        Args:
            args (Union[InsuranceRequest, dict]): the insurance request payload

        Returns:
            IRequestFrom: a lazy request dataclass instance
        """
        logger.debug(
            "Applying insurance coverage to package", payload=lib.to_dict(args)
        )
        payload = lib.to_object(models.InsuranceRequest, lib.to_dict(args))

        def action(gateway: gateway.Gateway) -> IDeserialize:
            is_valid, abortion = check_operation(gateway, "apply_insurance_coverage")
            if not is_valid:
                return abortion

            request: lib.Serializable = gateway.mapper.create_insurance_request(payload)
            response: lib.Deserializable = gateway.proxy.apply_insurance_coverage(
                request
            )

            @fail_safe(gateway)
            def deserialize():
                return gateway.mapper.parse_insurance_response(response)

            return IDeserialize(deserialize)

        return IRequestFrom(action)


class Webhook:
    """The unified Webhook API fluent interface"""

    @staticmethod
    def register(
        args: typing.Union[models.WebhookRegistrationRequest, dict],
    ) -> IRequestFrom:
        """Register a webhook for a carrier

        Args:
            args (Union[WebhookRegistrationRequest, dict]): the webhook registration request payload

        Returns:
            IRequestFrom: a lazy request dataclass instance
        """
        logger.debug("Registering webhook", payload=lib.to_dict(args))
        payload = lib.to_object(models.WebhookRegistrationRequest, lib.to_dict(args))

        def action(gateway: gateway.Gateway) -> IDeserialize:
            is_valid, abortion = check_operation(gateway, "register_webhook")
            if not is_valid:
                return abortion

            request: lib.Serializable = (
                gateway.mapper.create_webhook_registration_request(payload)
            )
            response: lib.Deserializable = gateway.proxy.register_webhook(request)

            @fail_safe(gateway)
            def deserialize():
                return gateway.mapper.parse_webhook_registration_response(response)

            return IDeserialize(deserialize)

        return IRequestFrom(action)

    @staticmethod
    def deregister(
        args: typing.Union[models.WebhookDeregistrationRequest, dict],
    ) -> IRequestFrom:
        """Deregister a webhook for a carrier

        Args:
            args (Union[WebhookDeregistrationRequest, dict]): the webhook deregistration request payload

        Returns:
            IRequestFrom: a lazy request dataclass instance
        """
        logger.debug("Deregistering webhook", payload=lib.to_dict(args))
        payload = lib.to_object(models.WebhookDeregistrationRequest, lib.to_dict(args))

        def action(gateway: gateway.Gateway) -> IDeserialize:
            is_valid, abortion = check_operation(gateway, "deregister_webhook")
            if not is_valid:
                return abortion

            request: lib.Serializable = (
                gateway.mapper.create_webhook_deregistration_request(payload)
            )
            response: lib.Deserializable = gateway.proxy.deregister_webhook(request)

            @fail_safe(gateway)
            def deserialize():
                return gateway.mapper.parse_webhook_deregistration_response(response)

            return IDeserialize(deserialize)

        return IRequestFrom(action)


class Hooks:
    """The unified Hooks API fluent interface"""

    @staticmethod
    def on_webhook_event(
        args: typing.Union[models.RequestPayload, dict],
    ) -> IRequestFrom:
        """Process a webhook event from a carrier

        Args:
            args (Union[RequestPayload, dict]): the webhook event request payload
        """
        logger.debug("Processing webhook event", payload=lib.to_dict(args))
        payload = lib.to_object(models.RequestPayload, lib.to_dict(args))

        def action(gateway: gateway.Gateway) -> IDeserialize:
            is_valid, abortion = check_operation(gateway, "on_webhook_event")
            if not is_valid:
                return abortion

            result = gateway.hooks.on_webhook_event(payload)

            @fail_safe(gateway)
            def deserialize():
                return result

            return IDeserialize(deserialize)

        return IRequestFrom(action)

    @staticmethod
    def on_oauth_authorize(
        args: typing.Union[models.OAuthAuthorizePayload, dict],
    ) -> IRequestFrom:
        """Create a OAuth authorize request for a carrier OAuth flow

        Args:
            args (Union[OAuthAuthorizePayload, dict]): the OAuth authorize request payload
        """
        logger.debug("Creating OAuth authorize request", payload=lib.to_dict(args))
        payload = lib.to_object(models.OAuthAuthorizePayload, lib.to_dict(args))

        def action(gateway: gateway.Gateway) -> IDeserialize:
            is_valid, abortion = check_operation(gateway, "on_oauth_authorize")
            if not is_valid:
                return abortion

            result = gateway.hooks.on_oauth_authorize(payload)

            @fail_safe(gateway)
            def deserialize():
                return result

            return IDeserialize(deserialize)

        return IRequestFrom(action)

    @staticmethod
    def on_oauth_callback(
        args: typing.Union[models.RequestPayload, dict],
    ) -> IRequestFrom:
        """Process a OAuth callback from a carrier

        Args:
            args (Union[RequestPayload, dict]): the OAuth callback request payload
        """
        logger.debug("Processing OAuth callback", payload=lib.to_dict(args))
        payload = lib.to_object(models.RequestPayload, lib.to_dict(args))

        def action(gateway: gateway.Gateway) -> IDeserialize:
            is_valid, abortion = check_operation(gateway, "on_oauth_callback")
            if not is_valid:
                return abortion

            result = gateway.hooks.on_oauth_callback(payload)

            @fail_safe(gateway)
            def deserialize():
                return result

            return IDeserialize(deserialize)

        return IRequestFrom(action)
