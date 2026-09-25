"""Karrio shipment advisors.

Shipment advisors are plugin-provided callables declared through
``PluginMetadata.shipment_advisors``. Each advisor has the signature
``(request, context) -> Iterable[Message]`` where ``request`` is the unified
``RateRequest`` or ``ShipmentRequest`` as sent to the carrier and ``context``
is an ``AdvisorContext``. Advisors contribute advisory messages only.
"""

import copy
import attr
import typing

import karrio.references as references
import karrio.core.models as models
import karrio.core.settings as settings
from karrio.core.utils.logger import logger

AdvisorOperation = typing.Literal["rating", "shipping"]
Advisor = typing.Callable[
    [typing.Any, "AdvisorContext"], typing.Iterable[models.Message]
]
ADVISORY_LEVELS = ("info", "warning")


@attr.s(auto_attribs=True, frozen=True)
class AdvisorContext:
    """Non-secret carrier connection context passed to shipment advisors.

    Built from an allowlist of connection settings fields, so connector
    specific credentials are never reachable from an advisor.
    """

    carrier_name: typing.Optional[str] = None
    carrier_id: typing.Optional[str] = None
    account_country_code: typing.Optional[str] = None
    test_mode: bool = False
    operation: typing.Optional[AdvisorOperation] = None
    config: dict = attr.Factory(dict)

    @staticmethod
    def from_settings(
        connection: settings.Settings, operation: AdvisorOperation
    ) -> "AdvisorContext":
        return AdvisorContext(
            carrier_name=connection.carrier_name,
            carrier_id=connection.carrier_id,
            account_country_code=connection.account_country_code,
            test_mode=connection.test_mode,
            operation=operation,
            config=copy.deepcopy(dict(connection.config or {})),
        )


def run_advisors(
    request: typing.Union[models.RateRequest, models.ShipmentRequest],
    connection: settings.Settings,
    operation: AdvisorOperation,
) -> typing.List[models.Message]:
    """Run every collected shipment advisor for one carrier connection.

    Args:
        request: the unified request as sent to the carrier
        connection: the carrier connection settings of the gateway in use
        operation: "rating" or "shipping"

    Returns:
        The advisory messages, with carrier identity filled from the context
        and any level other than info or warning reported as warning.
    """
    registered = references.get_advisors()

    if not registered:
        return []

    context = AdvisorContext.from_settings(connection, operation)

    return [
        message
        for plugin_id, advisor in registered
        for message in _advise(plugin_id, advisor, request, context)
    ]


def _advise(
    plugin_id: str,
    advisor: Advisor,
    request: typing.Any,
    context: AdvisorContext,
) -> typing.List[models.Message]:
    """Run one advisor on its own copy of the request, isolating its failures.

    This is the single place where a broad ``except Exception`` is used on
    purpose: advisors are third-party plugin code whose failure modes are
    unknown, and a broken advisor must never fail rating or shipping. The
    failure is reported as a ``shipment_advisor_failed`` warning naming the
    plugin instead of being discarded, which is why ``lib.failsafe`` is not
    used here.
    """
    try:
        return [
            _normalize(message, context)
            for message in (advisor(copy.deepcopy(request), context) or [])
        ]
    except Exception as error:
        logger.warning("Shipment advisor failed", plugin=plugin_id, error=str(error))
        return [
            models.Message(
                carrier_name=context.carrier_name,
                carrier_id=context.carrier_id,
                code="shipment_advisor_failed",
                level="warning",
                message=f"Shipment advisor from plugin '{plugin_id}' failed",
                details=dict(plugin=plugin_id, error=str(error)),
            )
        ]


def _normalize(message: models.Message, context: AdvisorContext) -> models.Message:
    return attr.evolve(
        message,
        carrier_name=message.carrier_name or context.carrier_name,
        carrier_id=message.carrier_id or context.carrier_id,
        level=message.level if message.level in ADVISORY_LEVELS else "warning",
    )
