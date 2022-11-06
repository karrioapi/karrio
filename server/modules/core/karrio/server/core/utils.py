import sys
import inspect
import functools
import logging
from string import Template
from concurrent import futures
from datetime import timedelta, datetime
from typing import TypeVar, Union, Callable, Any, List, Optional
import typing
from django.utils.translation import gettext_lazy as _
from django.conf import settings
import django_email_verification.confirm as confirm
import rest_framework_simplejwt.tokens as jwt

from karrio.core.utils import DP, DF
from karrio.server.core import datatypes, serializers

T = TypeVar("T")
logger = logging.getLogger(__name__)


def identity(value: Union[Any, Callable]) -> T:
    """
    :param value: function or value desired to be wrapped
    :return: value or callable return
    """
    return value() if callable(value) else value


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
            logger.warning(Template(warning).substitute(error=e))
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
            func(*args, **kwargs)
        except Exception as e:
            logger.error(e)
            raise e

    return wrapper


def async_wrapper(func):
    @functools.wraps(func)
    def wrapper(*args, run_synchronous: bool = False, **kwargs):
        def _run():
            func(*args, **kwargs)

        if run_synchronous:
            return _run()

        return run_async(_run)

    return wrapper


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
        if ("loaddata" in sys.argv):
            return

        return func(*args, **kwargs)

    return wrapper


def skip_on_commands(commands: typing.List[str] = ["loaddata", "migrate", "makemigrations"]):
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

            def wrapper(*args, **kwargs):
                result = method(*args, **kwargs)
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

    return serializers.TrackerStatus.in_transit


def is_sdk_message(
    message: Optional[Union[datatypes.Message, List[datatypes.Message]]]
) -> bool:
    msg = next(iter(message), None) if isinstance(message, list) else message

    return "SHIPPING_SDK_" in getattr(msg, "code", "")


def filter_rate_carrier_compatible_gateways(
    carriers: List, carrier_ids: List[str], shipper_country_code: Optional[str] = None
) -> List:
    """
    This function filters the carriers based on the capability to "get_rates"
    and if no explicit carrier list is provided, it will filter out any
    carrier that does not support the shipper's country code.
    """
    return [
        carrier.gateway
        for carrier in carriers
        if (
            # If no carrier list is provided, and gateway has get_rates capability.
            ("get_rates" in carrier.gateway.capabilities and len(carrier_ids) > 0)
            # If a carrier list is provided, and gateway is in the list.
            or (
                # the gateway has get_rates capability.
                "get_rates" in carrier.gateway.capabilities
                # and no explicit carrier list is provided.
                and len(carrier_ids) == 0
                # and the shipper country code is provided.
                and shipper_country_code is not None
                and (
                    carrier.gateway.settings.account_country_code
                    == shipper_country_code
                    or carrier.gateway.settings.account_country_code is None
                )
            )
        )
    ]


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
