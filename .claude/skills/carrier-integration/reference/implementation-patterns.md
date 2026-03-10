# Implementation Patterns

Patterns for implementing provider functions, proxy, settings, and error handling.

## Settings Pattern (`karrio/providers/[carrier]/utils.py`)

```python
import attr
import karrio.lib as lib
import karrio.core.settings as settings


@attr.s(auto_attribs=True)
class Settings(settings.Settings):
    """[Carrier] connection settings."""

    # Carrier credentials
    api_key: str = None
    secret_key: str = None
    account_number: str = None

    # Base settings (inherited)
    carrier_id: str = "[carrier_slug]"
    test_mode: bool = False
    metadata: dict = {}
    config: dict = {}
    id: str = None

    @property
    def carrier_name(self):
        return "[carrier_slug]"

    @property
    def server_url(self):
        return (
            "https://sandbox-api.carrier.com"
            if self.test_mode
            else "https://api.carrier.com"
        )

    @property
    def tracking_url(self):
        return "https://track.carrier.com/{tracking_number}"

    @property
    def connection_config(self) -> lib.units.Options:
        from karrio.providers.[carrier].units import ConnectionConfig
        return lib.to_connection_config(
            self.config or {},
            option_type=ConnectionConfig,
        )
```

### OAuth Settings Pattern (e.g., FedEx)

```python
    @property
    def access_token(self):
        """Cached OAuth token."""
        cache_key = f"{self.carrier_name}|{self.client_id}|{self.client_secret}"
        now = datetime.datetime.now() + datetime.timedelta(minutes=30)

        auth = self.connection_cache.get(cache_key) or {}
        token = auth.get("access_token")
        expiry = lib.to_date(auth.get("expiry"), current_format="%Y-%m-%d %H:%M:%S")

        if token is not None and expiry is not None and expiry > now:
            return token

        self.connection_cache[cache_key] = login.parse_token_response(
            lib.request(
                url=f"{self.server_url}/oauth/token",
                data=lib.to_query_string(dict(
                    grant_type="client_credentials",
                    client_id=self.client_id,
                    client_secret=self.client_secret,
                )),
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                method="POST",
            ),
        )
        return self.connection_cache[cache_key]["access_token"]
```

## Proxy Pattern (`karrio/mappers/[carrier]/proxy.py`)

```python
import karrio.lib as lib
import karrio.api.proxy as proxy
import karrio.providers.[carrier].utils as provider_utils
import karrio.mappers.[carrier].settings as provider_settings


class Proxy(proxy.Proxy):
    settings: provider_settings.Settings

    def get_rates(self, request: lib.Serializable) -> lib.Deserializable:
        response = lib.request(
            url=f"{self.settings.server_url}/v1/rates",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.settings.api_key}",
            },
        )
        return lib.Deserializable(response, lib.to_dict)

    def get_tracking(self, request: lib.Serializable) -> lib.Deserializable:
        response = lib.request(
            url=f"{self.settings.server_url}/v1/tracking/{request.serialize()}",
            trace=self.trace_as("json"),
            method="GET",
            headers={
                "Authorization": f"Bearer {self.settings.api_key}",
            },
        )
        return lib.Deserializable(response, lib.to_dict)

    def create_shipment(self, request: lib.Serializable) -> lib.Deserializable:
        response = lib.request(
            url=f"{self.settings.server_url}/v1/shipments",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.settings.api_key}",
            },
        )
        return lib.Deserializable(response, lib.to_dict, request.ctx)

    def cancel_shipment(self, request: lib.Serializable) -> lib.Deserializable:
        response = lib.request(
            url=f"{self.settings.server_url}/v1/shipments/{request.serialize()}",
            trace=self.trace_as("json"),
            method="DELETE",
            headers={
                "Authorization": f"Bearer {self.settings.api_key}",
            },
        )
        return lib.Deserializable(response, lib.to_dict)
```

### Multi-Tracking Proxy Pattern

```python
    def get_tracking(self, request: lib.Serializable) -> lib.Deserializable:
        def _get_tracking(tracking_number: str):
            return tracking_number, lib.request(
                url=f"{self.settings.server_url}/v1/tracking/{tracking_number}",
                trace=self.trace_as("json"),
                method="GET",
                headers={"Authorization": f"Bearer {self.settings.api_key}"},
            )

        responses: list = lib.run_concurently(
            _get_tracking, request.serialize(), max_workers=2
        )
        return lib.Deserializable(responses, lambda res: [
            (num, lib.to_dict(r)) for num, r in res
        ])
```

## Rate Provider Pattern (`karrio/providers/[carrier]/rate.py`)

```python
import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.[carrier].error as error
import karrio.providers.[carrier].utils as provider_utils
import karrio.providers.[carrier].units as provider_units
import karrio.schemas.[carrier].rate_request as carrier_req
import karrio.schemas.[carrier].rate_response as carrier_res


def parse_rate_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.RateDetails], typing.List[models.Message]]:
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)
    rates = [
        _extract_details(rate, settings)
        for rate in (response.get("rates") or [])
        if rate.get("total_charge")  # Filter invalid rates
    ]
    return rates, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
) -> models.RateDetails:
    rate = lib.to_object(carrier_res.RateResponseType, data)
    service = provider_units.ShippingService.map(rate.service_code)

    return models.RateDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        service=service.name_or_key,
        total_charge=lib.to_money(rate.total_charge),
        currency=rate.currency or "USD",
        transit_days=rate.transit_days,
        extra_charges=[
            models.ChargeDetails(
                name=charge.name,
                amount=lib.to_money(charge.amount),
                currency=rate.currency or "USD",
            )
            for charge in (rate.charges or [])
        ],
    )


def rate_request(
    payload: models.RateRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    shipper = lib.to_address(payload.shipper)
    recipient = lib.to_address(payload.recipient)
    packages = lib.to_packages(payload.parcels)
    services = lib.to_services(payload.services, provider_units.ShippingService)
    options = lib.to_shipping_options(payload.options)

    request = carrier_req.RateRequestType(
        origin=carrier_req.AddressType(
            postal_code=shipper.postal_code,
            country_code=shipper.country_code,
            city=shipper.city,
            state_code=shipper.state_code,
        ),
        destination=carrier_req.AddressType(
            postal_code=recipient.postal_code,
            country_code=recipient.country_code,
            city=recipient.city,
            state_code=recipient.state_code,
        ),
        packages=[
            carrier_req.PackageType(
                weight=carrier_req.WeightType(
                    value=pkg.weight.value,
                    unit=provider_units.WeightUnit[pkg.weight.unit].value,
                ),
                dimensions=lib.identity(
                    carrier_req.DimensionsType(
                        length=pkg.length.value,
                        width=pkg.width.value,
                        height=pkg.height.value,
                        unit=provider_units.DimensionUnit[
                            pkg.dimension_unit or "IN"
                        ].value,
                    )
                    if all([pkg.length, pkg.width, pkg.height])
                    else None
                ),
            )
            for pkg in packages
        ],
        services=[svc.value_or_key for svc in services],
    )

    return lib.Serializable(request, lib.to_dict)
```

## Tracking Provider Pattern

```python
def parse_tracking_response(
    _response: lib.Deserializable[list],
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.List[models.TrackingDetails], typing.List[models.Message]]:
    responses = _response.deserialize()

    messages = sum(
        [
            error.parse_error_response(response, settings, tracking_number=number)
            for number, response in responses
        ],
        start=[],
    )
    tracking_details = [
        _extract_details(number, response, settings)
        for number, response in responses
        if response.get("tracking_number")  # Filter failed lookups
    ]
    return tracking_details, messages


def _extract_details(
    tracking_number: str,
    data: dict,
    settings: provider_utils.Settings,
) -> models.TrackingDetails:
    details = lib.to_object(carrier_res.TrackingResponseType, data)
    status = next(
        (s.name for s in list(provider_units.TrackingStatus)
         if details.status in s.value),
        "in_transit",
    )

    return models.TrackingDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=tracking_number,
        status=status,
        delivered=status == "delivered",
        events=[
            models.TrackingEvent(
                date=lib.fdate(event.date),
                time=lib.ftime(event.time),
                description=event.description,
                location=lib.text(event.city, event.state, separator=", "),
                code=event.code,
            )
            for event in (details.events or [])
        ],
        info=models.TrackingInfo(
            carrier_tracking_link=settings.tracking_url.format(
                tracking_number=tracking_number
            ),
        ),
    )


def tracking_request(
    payload: models.TrackingRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    return lib.Serializable(payload.tracking_numbers)
```

## Shipment Provider Pattern

```python
# shipment/create.py
def parse_shipment_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.ShipmentDetails, typing.List[models.Message]]:
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)
    shipment = lib.identity(
        _extract_details(response, settings, ctx=_response.ctx)
        if not any(m.code for m in messages if m.level == "error")
        else None
    )
    return shipment, messages


def _extract_details(
    data: dict,
    settings: provider_utils.Settings,
    ctx: dict = {},
) -> models.ShipmentDetails:
    shipment = lib.to_object(carrier_res.ShipmentResponseType, data)

    return models.ShipmentDetails(
        carrier_id=settings.carrier_id,
        carrier_name=settings.carrier_name,
        tracking_number=shipment.tracking_number,
        shipment_identifier=shipment.shipment_id,
        label_type=ctx.get("label_type", "PDF"),
        docs=models.Documents(label=shipment.label),
        meta=dict(
            carrier_tracking_link=settings.tracking_url.format(
                tracking_number=shipment.tracking_number
            ),
        ),
    )
```

## Error Parser Pattern (`karrio/providers/[carrier]/error.py`)

```python
import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.[carrier].utils as provider_utils


def parse_error_response(
    response: typing.Union[typing.List[dict], dict],
    settings: provider_utils.Settings,
    **details,
) -> typing.List[models.Message]:
    responses = response if isinstance(response, list) else [response]
    errors = sum(
        [
            result.get("errors") or []
            for result in responses
            if isinstance(result, dict)
        ],
        [],
    )

    return [
        models.Message(
            carrier_name=settings.carrier_name,
            carrier_id=settings.carrier_id,
            code=err.get("code", "UNKNOWN"),
            message=err.get("message", "Unknown error"),
            details={**details, **({k: v for k, v in err.items()
                     if k not in ("code", "message")})},
        )
        for err in errors
    ]
```

## Plugin Metadata Pattern (`karrio/plugins/[carrier]/__init__.py`)

```python
import karrio.core.metadata as metadata
import karrio.mappers.[carrier] as mappers
import karrio.providers.[carrier].units as units

METADATA = metadata.PluginMetadata(
    status="beta",                    # "beta" or "production-ready"
    id="[carrier_slug]",
    label="[Carrier Display Name]",
    Mapper=mappers.Mapper,
    Proxy=mappers.Proxy,
    Settings=mappers.Settings,
    # Units
    services=units.ShippingService,
    service_levels=units.DEFAULT_SERVICES,
    options=units.ShippingOption,
    package_presets=units.PackagePresets,
    connection_configs=units.ConnectionConfig,
    # Flags
    is_hub=False,                     # True for aggregator carriers
    website="https://www.carrier.com",
    description="[Carrier] shipping integration",
)
```
