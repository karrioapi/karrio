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

import karrio.core.settings as settings

AdvisorOperation = typing.Literal["rating", "shipping"]


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
