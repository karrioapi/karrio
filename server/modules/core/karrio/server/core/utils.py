from datetime import timedelta
import inspect
import functools
import logging
from typing import TypeVar, Union, Callable, Any, List, Optional
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django_email_verification.confirm import (
    _get_validated_field,
    EmailMultiAlternatives,
    render_to_string,
)
import rest_framework_simplejwt.tokens as jwt

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
    try:
        return callable()
    except Exception:
        if warning:
            logger.warning(warning)
        return None


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


def disable_for_loaddata(signal_handler):
    @functools.wraps(signal_handler)
    def wrapper(*args, **kwargs):
        for fr in inspect.stack():
            if inspect.getmodulename(fr[1]) == "loaddata":
                return
        signal_handler(*args, **kwargs)

    return wrapper


def email_setup_required(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if not settings.EMAIL_ENABLED:
            raise Exception(_("The email service is not configured."))

        return func(*args, **kwargs)

    return wrapper


@email_setup_required
def send_email(
    emails: List[str],
    subject: str,
    email_template: str,
    context: dict = {},
    text_template: str = None,
):
    sender = _get_validated_field("EMAIL_FROM_ADDRESS")
    html = render_to_string(email_template, context)
    text = render_to_string(text_template or email_template, context)

    msg = EmailMultiAlternatives(subject, text, sender, emails)
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
