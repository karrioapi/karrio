import sys
import typing
import inspect
import functools
from concurrent import futures
from datetime import timedelta, datetime
from typing import TypeVar, Union, Callable, Any, List, Optional

from django.conf import settings
from django.utils.translation import gettext_lazy as _
import django_email_verification.confirm as confirm
import rest_framework_simplejwt.tokens as jwt
import rest_framework.status as status
from karrio.server.core.logging import logger

import karrio.lib as lib
from karrio.core.utils import DP, DF
from karrio.server.core import datatypes, serializers, exceptions

T = TypeVar("T")


def identity(value: Union[Any, Callable]) -> Any:
    """
    :param value: function or value desired to be wrapped
    :return: value or callable return
    """
    return value() if callable(value) else value


def execute_gateway_operation(
    operation_name: str,
    callable: Callable[[], T],
    carrier: Any = None,
    context: Any = None,
) -> T:
    """Execute a gateway operation with telemetry instrumentation.

    This function wraps SDK gateway calls (rates, shipments, tracking, etc.)
    with telemetry spans for observability when Sentry is configured.

    Args:
        operation_name: Name of the operation (e.g., "rates_fetch", "shipment_create")
        callable: The callable that performs the SDK operation
        carrier: Optional carrier instance for context
        context: Optional request context for accessing the tracer

    Returns:
        The result of the callable

    Example:
        result = execute_gateway_operation(
            "rates_fetch",
            lambda: karrio.Rating.fetch(request).from_(carrier.gateway).parse(),
            carrier=carrier,
            context=context,
        )
    """
    tracer = _get_tracer_from_context(context)

    # Build span attributes
    attributes = {}
    if carrier:
        attributes["carrier_name"] = getattr(carrier, "carrier_code", None)
        attributes["carrier_id"] = getattr(carrier, "carrier_id", None)
        attributes["test_mode"] = getattr(carrier, "test_mode", None)

    span_name = f"karrio_{operation_name}"

    with tracer.start_span(span_name, attributes=attributes) as span:
        try:
            result = callable()
            span.set_status("ok")

            # Record success metric
            tracer.record_metric(
                f"karrio_{operation_name}_success",
                1,
                tags={
                    "carrier": attributes.get("carrier_name", "unknown"),
                    "test_mode": str(attributes.get("test_mode", False)).lower(),
                },
            )

            return result

        except Exception as e:
            span.set_status("error", str(e))
            span.record_exception(e)

            # Record failure metric
            tracer.record_metric(
                f"karrio_{operation_name}_error",
                1,
                tags={
                    "carrier": attributes.get("carrier_name", "unknown"),
                    "error_type": type(e).__name__,
                },
            )

            raise


def _get_tracer_from_context(context: Any) -> lib.Tracer:
    """Get the tracer from request context or return a default one."""
    if context is None:
        # Try to get from current request via middleware
        try:
            from karrio.server.core.middleware import SessionContext

            request = SessionContext.get_current_request()
            if request and hasattr(request, "tracer"):
                return request.tracer
        except Exception:
            pass

    # Try to get from context object
    if hasattr(context, "tracer"):
        return context.tracer

    if hasattr(context, "request") and hasattr(context.request, "tracer"):
        return context.request.tracer

    # Return a default tracer (with NoOpTelemetry)
    return lib.Tracer()


def failsafe(callable: Callable[[], T], warning: str = None) -> T:
    """This higher order function wraps a callable in a try..except
    scope to capture any exception raised.
    Only use it when you are running something unstable that you
    don't mind if it fails.
    """
    try:
        return callable()
    except Exception as e:
        if warning:
            logger.warning(warning, error=str(e))
        return None


def run_async(callable: Callable[[], Any]) -> futures.Future:
    """This higher order function initiate the execution
    of a callable in a non-blocking thread and return a
    handle for a future response.
    """
    return futures.ThreadPoolExecutor(max_workers=1).submit(callable)


def error_wrapper(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.exception(e)
            raise e

    return wrapper


def async_wrapper(func):
    @functools.wraps(func)
    def wrapper(*args, run_synchronous: bool = False, **kwargs):
        def _run():
            return func(*args, **kwargs)

        if run_synchronous:
            return _run()

        return run_async(_run)

    return wrapper


def with_telemetry(operation_name: str = None):
    """Decorator that adds telemetry instrumentation to gateway methods.

    This decorator wraps gateway methods with telemetry spans for observability.
    When Sentry is configured, it creates spans for each operation with relevant
    context (carrier info, operation type, etc.).

    Args:
        operation_name: Optional custom operation name. If not provided,
                       the function name is used.

    Usage:
        class Shipments:
            @staticmethod
            @with_telemetry("shipment_create")
            def create(payload: dict, carrier: CarrierConnection = None, **kwargs):
                ...
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            op_name = operation_name or func.__name__

            # Extract carrier and context from kwargs if available
            carrier = kwargs.get("carrier")
            context = kwargs.get("context")

            # Get tracer from context
            tracer = _get_tracer_from_context(context)

            # Build span attributes
            attributes = {"operation": op_name}
            if carrier:
                attributes["carrier_name"] = getattr(carrier, "carrier_code", None)
                attributes["carrier_id"] = getattr(carrier, "carrier_id", None)
                attributes["test_mode"] = getattr(carrier, "test_mode", None)

            span_name = f"karrio_{op_name}"

            with tracer.start_span(span_name, attributes=attributes) as span:
                try:
                    result = func(*args, **kwargs)
                    span.set_status("ok")

                    # Record success metric
                    tracer.record_metric(
                        f"karrio_{op_name}_success",
                        1,
                        tags={
                            "carrier": attributes.get("carrier_name", "unknown")
                            or "unknown",
                        },
                    )

                    return result

                except Exception as e:
                    span.set_status("error", str(e))
                    span.record_exception(e)

                    # Record error metric
                    tracer.record_metric(
                        f"karrio_{op_name}_error",
                        1,
                        tags={
                            "carrier": attributes.get("carrier_name", "unknown")
                            or "unknown",
                            "error_type": type(e).__name__,
                        },
                    )

                    raise

        return wrapper

    return decorator


def tenant_aware(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if settings.MULTI_TENANTS:
            import django_tenants.utils as tenant_utils

            schema = kwargs.get("schema") or "public"

            with tenant_utils.schema_context(schema):
                return func(*args, **kwargs)
        else:
            return func(*args, **kwargs)

    return wrapper


def run_on_all_tenants(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if settings.MULTI_TENANTS:
            import django_tenants.utils as tenant_utils

            tenants = tenant_utils.get_tenant_model().objects.exclude(
                schema_name="public"
            )

            for tenant in tenants:
                with tenant_utils.tenant_context(tenant):
                    func(*args, **kwargs, schema=tenant.schema_name)
        else:
            func(*args, **kwargs)

    return wrapper


def disable_for_loaddata(signal_handler):
    @functools.wraps(signal_handler)
    def wrapper(*args, **kwargs):
        if is_system_loading_data():
            return

        signal_handler(*args, **kwargs)

    return wrapper


def skip_on_loadata(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if "loaddata" in sys.argv:
            return

        return func(*args, **kwargs)

    return wrapper


def skip_on_commands(
    commands: typing.List[str] = ["loaddata", "migrate", "makemigrations"]
):
    def _decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if any(cmd in sys.argv for cmd in commands):
                return

            return func(*args, **kwargs)

        return wrapper

    return _decorator


def email_setup_required(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if not settings.EMAIL_ENABLED:
            raise Exception(_("The email service is not configured."))

        return func(*args, **kwargs)

    return wrapper


def post_processing(methods: List[str] = None):
    def class_wrapper(klass):
        setattr(
            klass,
            "post_process_functions",
            getattr(klass, "post_process_functions") or [],
        )

        for name in methods:
            method = getattr(klass, name)

            def wrapper(*args, _method=method, **kwargs):
                result = _method(*args, **kwargs)
                processes = klass.post_process_functions
                context = kwargs.get("context")

                return functools.reduce(
                    lambda cummulated_result, process: process(
                        context, cummulated_result
                    ),
                    processes,
                    result,
                )

            setattr(klass, name, wrapper)

        return klass

    return class_wrapper


def upper(value_str: Optional[str]) -> Optional[str]:
    if value_str is None:
        return None

    return value_str.upper().replace("_", " ")


def batch_get_constance_values(keys: List[str]) -> dict:
    """
    Batch fetch multiple configuration values from Django Constance.

    This function uses Constance's mget() method to fetch all requested
    configuration keys in a single database query, avoiding N+1 query issues.

    Args:
        keys: List of configuration key names to fetch

    Returns:
        Dictionary mapping configuration keys to their values

    Example:
        >>> flags = batch_get_constance_values(['AUDIT_LOGGING', 'ALLOW_SIGNUP'])
        >>> print(flags['AUDIT_LOGGING'])
        True
    """
    from constance import config

    try:
        # Use mget to fetch all config values in a single query
        # mget returns a generator of (key, value) tuples
        return dict(config._backend.mget(keys))
    except Exception as e:
        logger.warning(
            "Failed to batch fetch constance values, returning empty dict", error=str(e)
        )
        return {}


def compute_tracking_status(
    details: Optional[datatypes.Tracking] = None,
) -> serializers.TrackerStatus:
    if details is None:
        return serializers.TrackerStatus.pending
    elif details.delivered:
        return serializers.TrackerStatus.delivered
    elif (len(details.events) == 0) or (
        len(details.events) == 1 and details.events[0].code == "CREATED"
    ):
        return serializers.TrackerStatus.pending

    if (
        any(details.status or "")
        and serializers.TrackerStatus.map(details.status).value is not None
    ):
        return serializers.TrackerStatus.map(details.status)

    return serializers.TrackerStatus.in_transit


def is_sdk_message(
    message: Optional[Union[datatypes.Message, List[datatypes.Message]]],
) -> bool:
    msg = next(iter(message), None) if isinstance(message, list) else message

    return "SHIPPING_SDK_" in str(getattr(msg, "code", ""))


def filter_rate_carrier_compatible_gateways(
    carriers: List, carrier_ids: List[str], shipper_country_code: Optional[str] = None
) -> List:
    """
    This function filters the carriers based on the capability to "rating"
    and if no explicit carrier list is provided, it will filter out any
    carrier that does not support the shipper's country code.
    Carriers with no account_country_code set are always included.
    """
    _gateways = [
        carrier.gateway
        for carrier in carriers
        if (
            # If explicit carrier list is provided and gateway has "rating" capability.
            ("rating" in carrier.gateway.capabilities and len(carrier_ids) > 0)
            # If no carrier list is provided, and gateway is in the list.
            or (
                # the gateway has "rating" capability.
                "rating" in carrier.gateway.capabilities
                # and no explicit carrier list is provided.
                and len(carrier_ids) == 0
                # and the shipper country code is provided.
                and shipper_country_code is not None
                and (
                    # Carriers with no account_country_code work across countries
                    not carrier.gateway.settings.account_country_code
                    or carrier.gateway.settings.account_country_code
                    == shipper_country_code
                )
            )
        )
    ]

    return ({_.settings.carrier_id: _ for _ in _gateways}).values()


def is_system_loading_data() -> bool:
    try:
        for fr in inspect.stack():
            if inspect.getmodulename(fr[1]) == "loaddata":
                return True
    except:
        pass

    return False


@email_setup_required
def send_email(
    emails: List[str],
    subject: str,
    email_template: str,
    context: dict = {},
    text_template: str = None,
    **kwargs,
):
    sender = confirm._get_validated_field("EMAIL_FROM_ADDRESS")
    html = confirm.render_to_string(email_template, context)
    text = confirm.render_to_string(text_template or email_template, context)

    msg = confirm.EmailMultiAlternatives(subject, text, sender, emails)
    msg.attach_alternative(html, "text/html")
    msg.send()


class ConfirmationToken(jwt.Token):
    token_type = "confirmation"
    lifetime = timedelta(hours=2)

    @classmethod
    def for_data(cls, user, data: dict) -> str:
        token = super().for_user(user)

        for k, v in data.items():
            token[k] = v

        return token


class ResourceAccessToken(jwt.Token):
    """JWT token for limited resource access (documents, exports, etc.)."""

    token_type = "resource_access"
    lifetime = timedelta(minutes=5)

    @classmethod
    def for_resource(
        cls,
        user,
        resource_type: str,
        resource_ids: List[str],
        access: List[str],
        format: Optional[str] = None,
        org_id: Optional[str] = None,
        test_mode: Optional[bool] = None,
        expires_in: Optional[int] = None,
    ) -> "ResourceAccessToken":
        """Generate a resource access token.

        Args:
            user: The authenticated user
            resource_type: Type of resource (shipment, manifest, template, document)
            resource_ids: List of resource IDs to grant access to
            access: List of access permissions (label, invoice, manifest, render, etc.)
            format: Document format (pdf, png, zpl)
            org_id: Organization ID for multi-tenant environments
            test_mode: Whether this is test mode
            expires_in: Custom expiration time in seconds

        Returns:
            ResourceAccessToken instance
        """
        token = cls()
        token["user_id"] = user.id if hasattr(user, "id") else user
        token["resource_type"] = resource_type
        token["resource_ids"] = resource_ids
        token["access"] = access

        if format:
            token["format"] = format
        if org_id:
            token["org_id"] = org_id
        if test_mode is not None:
            token["test_mode"] = test_mode
        if expires_in:
            token.set_exp(lifetime=timedelta(seconds=expires_in))

        return token

    @classmethod
    def decode(cls, token_string: str) -> dict:
        """Decode and validate a resource access token.

        Args:
            token_string: The JWT token string

        Returns:
            Dictionary with token claims

        Raises:
            rest_framework_simplejwt.exceptions.TokenError: If token is invalid
        """
        token = cls(token_string)
        return {
            "user_id": token.get("user_id"),
            "resource_type": token.get("resource_type"),
            "resource_ids": token.get("resource_ids", []),
            "access": token.get("access", []),
            "format": token.get("format"),
            "org_id": token.get("org_id"),
            "test_mode": token.get("test_mode"),
        }

    @classmethod
    def validate_access(
        cls,
        token_string: str,
        resource_type: str,
        resource_id: str,
        access: str,
    ) -> dict:
        """Validate token grants access to specific resource and action.

        Args:
            token_string: The JWT token string
            resource_type: Expected resource type
            resource_id: Resource ID to check access for
            access: Access permission to check

        Returns:
            Token claims if valid

        Raises:
            rest_framework_simplejwt.exceptions.TokenError: If token is invalid
            PermissionError: If access is not granted
        """
        claims = cls.decode(token_string)

        if claims["resource_type"] != resource_type:
            raise PermissionError(f"Token not valid for resource type: {resource_type}")

        if resource_id not in claims["resource_ids"]:
            raise PermissionError(f"Token not valid for resource: {resource_id}")

        if access not in claims["access"]:
            raise PermissionError(f"Token does not grant access: {access}")

        return claims

    @classmethod
    def validate_batch_access(
        cls,
        token_string: str,
        resource_type: str,
        resource_ids: List[str],
        access: str,
    ) -> dict:
        """Validate token grants access to multiple resources.

        Args:
            token_string: The JWT token string
            resource_type: Expected resource type
            resource_ids: List of resource IDs to check access for
            access: Access permission to check

        Returns:
            Token claims if valid

        Raises:
            rest_framework_simplejwt.exceptions.TokenError: If token is invalid
            PermissionError: If access is not granted
        """
        claims = cls.decode(token_string)

        if claims["resource_type"] != resource_type:
            raise PermissionError(f"Token not valid for resource type: {resource_type}")

        if access not in claims["access"]:
            raise PermissionError(f"Token does not grant access: {access}")

        token_ids = set(claims["resource_ids"])
        request_ids = set(resource_ids)
        if not request_ids.issubset(token_ids):
            missing = request_ids - token_ids
            raise PermissionError(
                f"Token does not grant access to resources: {', '.join(missing)}"
            )

        return claims


def validate_resource_token(
    request,
    resource_type: str,
    resource_ids: List[str],
    access: str,
):
    """Validate resource access token, skipping if user is already authenticated.

    If the request has an authenticated user (via API token, JWT, etc.),
    the resource token check is skipped. Otherwise, it validates the
    resource access token from the query parameter.

    Note: For this to work with non-DRF views, use the `APITokenAuthMixin`
    on your view class to run DRF authentication before this function is called.

    Args:
        request: The HTTP request object
        resource_type: Expected resource type (shipment, manifest, template, etc.)
        resource_ids: List of resource IDs to validate access for
        access: Required access permission (label, invoice, manifest, render, etc.)

    Returns:
        HttpResponseForbidden if validation fails, None if valid

    Example:
        error = validate_resource_token(request, "shipment", [pk], "label")
        if error:
            return error
    """
    from django.http import HttpResponseForbidden
    from django.contrib.auth.models import AnonymousUser

    # Skip resource token check if user is already authenticated
    if hasattr(request, "user") and request.user and not isinstance(request.user, AnonymousUser):
        if request.user.is_authenticated:
            return None

    # Fall back to resource access token validation
    token = request.GET.get("token")

    if not token:
        return HttpResponseForbidden(
            "Access token required. Use /api/tokens to generate one, or provide API token in Authorization header."
        )

    try:
        ResourceAccessToken.validate_batch_access(
            token_string=token,
            resource_type=resource_type,
            resource_ids=resource_ids,
            access=access,
        )
        return None
    except PermissionError as e:
        return HttpResponseForbidden(
            "You do not have permission to access these resources."
        )
    except Exception as e:
        logger.warning("Invalid resource access token: %s", str(e))
        return HttpResponseForbidden("Invalid or expired token.")


def require_resource_token(
    resource_type: str,
    access: str,
    get_resource_ids: Callable[..., List[str]],
):
    """Decorator for views requiring resource access token validation.

    Args:
        resource_type: Expected resource type (shipment, manifest, template, etc.)
        access: Required access permission (label, invoice, manifest, render, etc.)
        get_resource_ids: Callable that extracts resource IDs from request and view kwargs.
                         Receives (request, **kwargs), returns list of resource IDs.

    Example:
        @require_resource_token(
            resource_type="document",
            access="batch_labels",
            get_resource_ids=lambda req, **kw: req.GET.get("shipments", "").split(","),
        )
        def get(self, request, **kwargs):
            ...
    """

    def decorator(method):
        @functools.wraps(method)
        def wrapper(self, request, *args, **kwargs):
            resource_ids = get_resource_ids(request, **kwargs)
            error = validate_resource_token(
                request, resource_type, resource_ids, access
            )
            if error:
                return error
            return method(self, request, *args, **kwargs)

        return wrapper

    return decorator


def app_tracking_query_params(url: str, carrier) -> str:
    hub_flag = f"&hub={carrier.carrier_name}" if carrier.gateway.is_hub else ""

    return f"{url}{hub_flag}"


def default_tracking_event(
    event_at: datetime = None,
    code: str = None,
    description: str = None,
):
    return [
        DP.to_dict(
            datatypes.TrackingEvent(
                date=DF.fdate(event_at or datetime.now()),
                description=(description or "Label created and ready for shipment"),
                location="",
                code=(code or "CREATED"),
                time=DF.ftime(event_at or datetime.now()),
            )
        )
    ]


def get_carrier_tracking_link(carrier, tracking_number: str):
    tracking_url = getattr(carrier.gateway.settings, "tracking_url", None)

    return tracking_url.format(tracking_number) if tracking_url is not None else None


def _ensure_picked_up_status(events: typing.List[dict]) -> typing.List[dict]:
    """Transform the chronologically first in_transit event to picked_up if none exists."""
    if not events or any(e.get("status") == "picked_up" for e in events):
        return events

    # Events are sorted desc, so first in_transit chronologically is last in list
    first_idx = next(
        (i for i in range(len(events) - 1, -1, -1) if events[i].get("status") == "in_transit"),
        None,
    )

    return (
        [{**e, "status": "picked_up"} if i == first_idx else e for i, e in enumerate(events)]
        if first_idx is not None
        else events
    )


def process_events(
    response_events: typing.List[datatypes.TrackingEvent],
    current_events: typing.List[dict],
) -> typing.List[dict]:
    """Merge new tracking events with existing ones, avoiding duplicates by comparing event hashes.
    Latest events are kept at the top of the list."""
    if not any(response_events):
        return current_events

    new_events = lib.to_dict(response_events)

    # If no current events, return new events as-is (already sorted by SDK)
    if not any(current_events):
        return new_events

    # Merge events: add only new non-duplicate events to existing ones
    current_hashes = {lib.to_json(event) for event in current_events}
    unique_new_events = [
        event for event in new_events if lib.to_json(event) not in current_hashes
    ]

    # If no new unique events, return current events unchanged
    if not any(unique_new_events):
        return current_events

    # When merging, we need to re-sort because new events may have timestamps
    # that fall between existing events. We must parse datetimes properly
    # (not use string comparison) to handle 12-hour AM/PM format correctly.
    def try_parse_datetime(value: str, fmt: str) -> typing.Optional[datetime]:
        """Safely attempt to parse a datetime string with a given format."""
        return failsafe(lambda: datetime.strptime(value, fmt))

    def parse_date(event: dict) -> typing.Optional[datetime]:
        """Parse date from event using multiple format attempts."""
        date_str = event.get("date", "")
        date_formats = ["%Y-%m-%d", "%m/%d/%Y", "%-m/%d/%Y"]
        return (
            functools.reduce(
                lambda acc, fmt: acc or try_parse_datetime(date_str, fmt),
                date_formats,
                None,
            )
            if date_str
            else None
        )

    def parse_time(event: dict) -> typing.Optional[datetime.time]:
        """Parse time from event using multiple format attempts."""
        time_str = event.get("time", "")
        time_formats = ["%I:%M %p", "%H:%M:%S", "%H:%M", "%I:%M"]
        parsed = (
            functools.reduce(
                lambda acc, fmt: acc or try_parse_datetime(time_str, fmt),
                time_formats,
                None,
            )
            if time_str
            else None
        )
        return parsed.time() if parsed else None

    def parse_event_datetime(event: dict) -> typing.Optional[datetime]:
        """Parse complete datetime from event date and time."""
        parsed_date = parse_date(event)
        parsed_time = parse_time(event) if parsed_date else None
        return (
            datetime.combine(parsed_date.date(), parsed_time)
            if parsed_date and parsed_time
            else parsed_date
        )

    def create_sort_key(event: dict) -> tuple:
        """Create sort key: dated events first (by datetime desc), undated last (by original order)."""
        dt = parse_event_datetime(event)
        return (0 if dt else 1, dt if dt else datetime.min)

    # Merge and sort all events
    merged_events = current_events + unique_new_events
    sorted_events = sorted(merged_events, key=create_sort_key, reverse=True)

    # Transform first in_transit to picked_up if no picked_up exists
    # This provides a consistent pickup milestone across all carriers
    return _ensure_picked_up_status(sorted_events)


def _get_carrier_for_service(service: str, context=None) -> typing.Optional[str]:
    """Resolve carrier name from service code using karrio references."""
    import karrio.server.core.dataunits as dataunits

    services_map = dataunits.contextual_reference(context).get("services", {})

    return next(
        (
            carrier_name
            for carrier_name, services in services_map.items()
            if service in services
        ),
        None,
    )


def load_and_apply_shipping_method(
    validated_data: dict,
    shipping_method_id: str,
    context: typing.Any,
) -> dict:
    """
    Load a shipping method and apply its configuration to shipment data.

    This function loads a ShippingMethod by ID and applies its configuration
    to the validated_data dictionary using the shared apply_shipping_method_to_data
    helper from the shipping module.

    Args:
        validated_data: The shipment data dictionary
        shipping_method_id: The ID of the shipping method to load
        context: The request context for access control

    Returns:
        dict: Modified validated_data with shipping method configuration applied

    Raises:
        APIException: If shipping method not found, inactive, or module not installed
    """
    try:
        from karrio.server.shipping.models import ShippingMethod
        from karrio.server.shipping.serializers import apply_shipping_method_to_data
    except ImportError:
        raise exceptions.APIException(
            "Shipping methods module is not installed.",
            code="module_not_installed",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    # Load the shipping method with access control
    try:
        method = ShippingMethod.access_by(context).get(
            id=shipping_method_id,
            is_active=True,
        )
    except ShippingMethod.DoesNotExist:
        raise exceptions.APIException(
            f"Shipping method '{shipping_method_id}' not found or inactive.",
            code="shipping_method_not_found",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    # Apply shipping method configuration using shared helper
    result_data = apply_shipping_method_to_data(validated_data, method, context)

    logger.info(
        "Applied shipping method to shipment",
        shipping_method_id=method.id,
        shipping_method_name=method.name,
        carrier_service=method.carrier_service,
    )

    return result_data


def apply_rate_selection(payload: typing.Union[dict, typing.Any], **kwargs):
    """
    Select the appropriate rate based on the following priority hierarchy:

    1. selected_rate (already provided) - highest priority
    2. rate_id or service - try to find matching rate
    3. has_alternative_services fallback - try carrier-based fallback
    4. apply_shipping_rules - FALLBACK when no rate found from above

    Shipping rules act as a fallback when:
    - No service/rate_id provided, OR
    - service/rate_id provided but no matching rate found
    """
    data = kwargs.get("data") or kwargs
    get = lambda key, default=None: lib.identity(
        payload.get(key, data.get(key, default))
        if isinstance(payload, dict)
        else getattr(payload, key, data.get(key, default))
    )

    ctx = kwargs.get("context")
    rates = get("rates") or data.get("rates", [])
    options = get("options") or data.get("options", {})
    service = get("service") or data.get("service", None)
    rate_id = get("selected_rate_id") or data.get("selected_rate_id", None)
    selected_rate = get("selected_rate") or data.get("selected_rate", None)
    apply_shipping_rules = lib.identity(
        getattr(settings, "SHIPPING_RULES", False)
        and options.get("apply_shipping_rules", False)
    )

    if selected_rate:
        kwargs.update(selected_rate=selected_rate)
        return kwargs

    # Select by id or service if provided
    if rate_id or service:
        kwargs.update(
            selected_rate=next(
                (
                    rate
                    for rate in rates
                    if (rate_id and rate.get("id") == rate_id)
                    or (service and rate.get("service") == service)
                ),
                None,
            )
        )

        # has_alternative_services fallback when no exact match found
        has_alternative_services = options.get("has_alternative_services", False)

        if kwargs.get("selected_rate") is None and has_alternative_services and service:
            carrier_name = _get_carrier_for_service(service, ctx)
            fallback_rate = lib.identity(
                next(
                    (r for r in rates if r.get("carrier_name") == carrier_name),
                    None,
                )
                if carrier_name
                else None
            )

            kwargs.update(
                selected_rate=lib.identity(
                    {
                        **fallback_rate,
                        "service": service,
                        "meta": {
                            **(fallback_rate.get("meta") or {}),
                            "has_alternative_services": True,
                        },
                    }
                    if fallback_rate
                    else None
                )
            )

        return kwargs

    # Apply shipping rules if enabled and no selected rate is provided
    if apply_shipping_rules:
        # Import rules engine only when needed
        import karrio.server.automation.models as automation_models
        import karrio.server.automation.services.rules_engine as engine

        # Get active shipping rules
        active_rules = list(
            automation_models.ShippingRule.access_by(ctx).filter(is_active=True)
        )

        # Always run rule evaluation for activity tracking
        if active_rules:
            _, rule_selected_rate, rule_activity = engine.process_shipping_rules(
                shipment=payload,
                rules=active_rules,
                context=ctx,
            )

            kwargs.update(
                selected_rate=rule_selected_rate,
                rule_activity=rule_activity,
            )

    return kwargs


def require_selected_rate(func):
    """
    Decorator for rate selection process.
    - Checks if shipping rules are enabled
    - Evaluates and applies rules to modify service if needed
    - Augments response metadata with applied rules
    """

    @functools.wraps(func)
    def wrapper(payload, **kwargs):

        kwargs = apply_rate_selection(payload, **kwargs)

        if kwargs.get("selected_rate") is None:
            raise exceptions.APIException(
                "The service you selected is not available for this shipment.",
                code="service_unavailable",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        # Execute original function
        result = func(payload, **kwargs)

        if isinstance(result, datatypes.Shipment) and kwargs.get("rule_activity"):
            return lib.to_object(
                datatypes.Shipment,
                {
                    **lib.to_dict(result),
                    "meta": {
                        **(result.meta or {}),
                        **({"rule_activity": kwargs.get("rule_activity")}),
                    },
                },
            )

        if hasattr(result, "save") and kwargs.get("rule_activity"):
            result.meta = {
                **(result.meta or {}),
                **({"rule_activity": kwargs.get("rule_activity")}),
            }
            result.save()
            return result

        return result

    return wrapper


# ─────────────────────────────────────────────────────────────────────────────
# CARRIER CONNECTION UTILITIES
# ─────────────────────────────────────────────────────────────────────────────


class ConnectionType:
    """Connection type constants for carrier snapshots."""

    ACCOUNT = "account"
    SYSTEM = "system"
    BROKERED = "brokered"


def create_carrier_snapshot(connection: typing.Any) -> dict:
    """
    Create a snapshot dict from a carrier connection.

    Works with any connection type (CarrierConnection, SystemConnection, BrokeredConnection).
    The snapshot contains enough information to:
    - Resolve back to the live connection if it still exists
    - Display carrier identity if the connection is deleted

    Args:
        connection: Live connection object (CarrierConnection, SystemConnection, or BrokeredConnection)

    Returns:
        Snapshot dict suitable for storage in JSONField:
        {
            "connection_id": str,      # ID for resolution
            "connection_type": str,    # "account", "system", or "brokered"
            "carrier_code": str,       # Carrier type (e.g., "dhl_express")
            "carrier_id": str,         # User-defined identifier
            "carrier_name": str,       # Carrier type/code (API convention)
            "test_mode": bool,         # Test/production mode
        }

    Note:
        For BrokeredConnection, stores SystemConnection.id as connection_id
        (more stable if brokered is deleted) but uses brokered's computed values.
    """
    if connection is None:
        return {}

    class_name = connection.__class__.__name__

    # Determine connection type and ID
    if class_name == "BrokeredConnection":
        conn_type = ConnectionType.BROKERED
        # Store system connection ID for stability (per decision #30)
        conn_id = connection.system_connection_id
        carrier_id = connection.effective_carrier_id
        carrier_code = connection.carrier_code
        test_mode = connection.test_mode
    elif class_name == "SystemConnection":
        conn_type = ConnectionType.SYSTEM
        conn_id = connection.id
        carrier_id = connection.carrier_id
        carrier_code = connection.carrier_code
        test_mode = connection.test_mode
    else:  # CarrierConnection (account connection)
        conn_type = ConnectionType.ACCOUNT
        conn_id = connection.id
        carrier_id = connection.carrier_id
        carrier_code = connection.carrier_code
        test_mode = connection.test_mode

    # carrier_name follows API convention: use carrier_code (e.g., "canadapost")
    # display_name is available via carrier_code lookup if needed
    carrier_name = carrier_code

    return {
        "connection_id": conn_id,
        "connection_type": conn_type,
        "carrier_code": carrier_code,
        "carrier_id": carrier_id,
        "carrier_name": carrier_name,
        "test_mode": test_mode,
    }


def resolve_carrier(
    snapshot: typing.Optional[dict],
    context: typing.Any = None,
) -> typing.Optional[typing.Any]:
    """
    Resolve a live carrier connection from a snapshot.

    Resolution chain:
    1. Direct lookup by connection_id based on connection_type
    2. For brokered: try to find user's BrokeredConnection for that SystemConnection
    3. Fallback to SystemConnection if brokered not found
    4. Return None if connection cannot be resolved (use snapshot for display)

    Args:
        snapshot: Connection snapshot dict with connection_id, connection_type, etc.
        context: Request context for access control (user/org)

    Returns:
        Live connection object (CarrierConnection, SystemConnection, or BrokeredConnection)
        or None if connection cannot be resolved.

    Note:
        Returns None when access is denied (per decision #29).
        Caller should use snapshot data for display-only purposes.
    """
    if not snapshot:
        return None

    from karrio.server.providers.models import (
        CarrierConnection,
        SystemConnection,
        BrokeredConnection,
    )

    conn_type = snapshot.get("connection_type", ConnectionType.ACCOUNT)
    # Support both new format (connection_id) and legacy format (carrier_connection_id)
    conn_id = snapshot.get("connection_id") or snapshot.get("carrier_connection_id")

    if not conn_id:
        return None

    # Direct lookup by type
    if conn_type == ConnectionType.ACCOUNT:
        # Account connection (CarrierConnection)
        queryset = CarrierConnection.objects.filter(id=conn_id, active=True)

        # Apply access control in Insiders mode
        if context is not None and hasattr(CarrierConnection, "access_by"):
            queryset = CarrierConnection.access_by(context).filter(id=conn_id, active=True)

        return queryset.first()

    if conn_type == ConnectionType.SYSTEM:
        # System connection
        return SystemConnection.objects.filter(id=conn_id, active=True).first()

    if conn_type == ConnectionType.BROKERED:
        # Brokered connection - conn_id is actually system_connection_id (per decision #30)
        # Try to find user's BrokeredConnection for that SystemConnection (per decision #33)
        system_conn = SystemConnection.objects.filter(id=conn_id, active=True).first()

        if not system_conn:
            return None

        # Try to find user's brokered connection
        brokered_qs = BrokeredConnection.objects.filter(
            system_connection=system_conn,
            is_enabled=True,
        )

        # Apply access control based on context
        if context is not None:
            user = getattr(context, "user", None)
            org = getattr(context, "org", None)

            if settings.MULTI_ORGANIZATIONS and org:
                # Insiders: Check for org-linked brokered connection
                brokered_qs = brokered_qs.filter(link__org=org)
            elif user:
                # OSS: Check for user's brokered connection
                brokered_qs = brokered_qs.filter(created_by=user)

        brokered = brokered_qs.first()

        # Return brokered if found, else return system connection as fallback
        return brokered if brokered else system_conn

    # Unknown connection type
    return None
