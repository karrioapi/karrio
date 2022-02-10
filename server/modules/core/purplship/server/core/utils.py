import functools
from typing import TypeVar, Union, Callable, Any, List, Optional

from purplship.server.core import datatypes, serializers

T = TypeVar("T")


def identity(value: Union[Any, Callable]) -> T:
    """
    :param value: function or value desired to be wrapped
    :return: value or callable return
    """
    return value() if callable(value) else value


def failsafe(callable: Callable[[], T]) -> T:
    try:
        return callable()
    except Exception:
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
            ("get_rates" in carrier.gateway.capabilities and len(carrier_ids) > 0)
            or (
                "get_rates" in carrier.gateway.capabilities
                and len(carrier_ids) == 0
                and shipper_country_code is not None
                and any(carrier.gateway.settings.account_country_code or [])
                and (
                    carrier.gateway.settings.account_country_code
                    == shipper_country_code
                )
            )
        )
    ]
