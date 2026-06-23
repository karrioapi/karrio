"""ParcelOne REST API connection utilities and settings."""

import base64

import karrio.core as core
import karrio.core.dynamic as core_dynamic
import karrio.core.models as core_models
import karrio.lib as lib

_PROFILE_CACHE: dict[tuple[str, str | None, str | None], dict] = {}


class Settings(core.Settings, core_dynamic.DynamicMetadataMixin):
    """ParcelOne REST API connection settings."""

    username: str
    password: str
    api_key: str

    mandator_id: str = None
    consigner_id: str = None

    id: str = None
    test_mode: bool = False
    carrier_id: str = "parcelone"
    account_country_code: str = "DE"
    metadata: dict = {}
    config: dict = {}

    @property
    def carrier_name(self):
        return "parcelone"

    @property
    def server_url(self):
        return "https://sandbox.parcelone.io" if self.test_mode else "https://production.parcelone.io"

    @property
    def tracking_link(self):
        return "https://parcel.one/tracking?trackno={}"

    @property
    def authorization(self):
        """HTTP Basic Auth header value."""
        credentials = f"{self.username}:{self.password}"
        encoded = base64.b64encode(credentials.encode()).decode()
        return f"Basic {encoded}"

    @property
    def connection_config(self) -> lib.units.Options:
        from karrio.providers.parcelone.units import ConnectionConfig

        return lib.to_connection_config(
            self.config or {},
            option_type=ConnectionConfig,
        )

    @property
    def connection_app_identifier(self) -> str:
        """Source-software marker sent as ``ShippingData.Software``."""
        return (
            self.connection_config.app_identifier.state
            or self.connection_system_config.get("PARCELONE_APP_IDENTIFIER")
            or "JTL-Shipping"
        )

    @property
    def dynamic_ttl_seconds(self) -> int:
        return int(self.connection_system_config.get("PARCELONE_DYNAMIC_TTL_SECONDS") or 3600)

    @property
    def dynamic_timeout_seconds(self) -> float:
        return float(self.connection_system_config.get("PARCELONE_DYNAMIC_TIMEOUT_SECONDS") or 1.5)

    @property
    def dynamic_negative_ttl_seconds(self) -> int:
        return int(self.connection_system_config.get("PARCELONE_DYNAMIC_NEGATIVE_TTL_SECONDS") or 60)

    @property
    def profile(self) -> dict:
        """Return the cached ``GET /profile`` payload for this connection.

        Caches per ``(id|username, mandator_id, consigner_id)`` for the lifetime
        of the worker. On any network/HTTP failure we fall back to the offline
        :data:`units.STATIC_PROFILE` snapshot so the connector keeps working.
        """
        from karrio.providers.parcelone import units as provider_units

        cache_key = (self.id or self.username, self.mandator_id, self.consigner_id)
        cached = _PROFILE_CACHE.get(cache_key)
        if cached is not None:
            return cached

        profile = lib.failsafe(self._fetch_profile) or provider_units.STATIC_PROFILE
        _PROFILE_CACHE[cache_key] = profile
        return profile

    def _fetch_profile(self) -> dict | None:
        """Hit ``GET /shippingapi/v1/profile`` and normalize the response."""
        response = lib.request(
            url=f"{self.server_url}/shippingapi/v1/profile",
            method="GET",
            headers={
                "Accept": "application/json",
                "Authorization": self.authorization,
                "Apikey": self.api_key,
            },
        )
        data = lib.to_dict(response) or {}
        results = data.get("results") or []
        if not results:
            return None

        mandator = results[0]
        return {
            "mandator": mandator.get("MandatorID"),
            "consigners": [c.get("ConsignerID") for c in mandator.get("Consigners") or []],
            "ceps": {
                cep.get("CEPID"): {
                    "name": cep.get("CEPLongname"),
                    "products": {
                        product.get("ProductID"): {
                            "name": product.get("ProductName"),
                            "services": [s.get("ServiceID") for s in product.get("Services") or []],
                        }
                        for product in cep.get("Products") or []
                    },
                }
                for cep in mandator.get("CEPs") or []
            },
        }

    def fetch_dynamic_metadata(self) -> core_dynamic.DynamicMetadata:
        """Project the live ``/profile`` payload into a karrio :class:`DynamicMetadata`.

        Falls back to :data:`units.STATIC_PROFILE` if the live fetch fails.
        """
        from karrio.providers.parcelone import units as provider_units

        profile = self.profile or provider_units.STATIC_PROFILE
        if not profile or not profile.get("ceps"):
            return core_dynamic.DynamicMetadata.empty(source="error")

        services: list[core_models.ServiceLevel] = []
        service_availability: dict[str, list[str]] = {}
        seen_option_codes: set[str] = set()
        options: list[core_dynamic.OptionDescriptor] = []

        for cep_id, cep in (profile.get("ceps") or {}).items():
            cep_name = cep.get("name") or cep_id
            for product_id, product in (cep.get("products") or {}).items():
                service_code = f"parcelone_{cep_id.lower()}_{product_id.lower()}"
                services.append(
                    core_models.ServiceLevel(
                        service_code=service_code,
                        service_name=f"{cep_name} — {product.get('name') or product_id}",
                        currency="EUR",
                        domicile=cep_id != "DHL" or product_id == "101",
                        international=cep_id != "DHL" or product_id != "101",
                    )
                )

                option_keys: list[str] = []
                for raw_code in product.get("services") or []:
                    descriptor = _option_descriptor_for(raw_code, provider_units.ShippingOption)
                    option_keys.append(descriptor.name)
                    if descriptor.code not in seen_option_codes:
                        seen_option_codes.add(descriptor.code)
                        options.append(descriptor)

                if option_keys:
                    service_availability[service_code] = list(dict.fromkeys(option_keys))

        default_cep, default_product = _pick_default_route(profile)
        connection_config_defaults: dict[str, str] = {}
        if default_cep:
            connection_config_defaults["cep_id"] = default_cep
        if default_product:
            connection_config_defaults["product_id"] = default_product

        return core_dynamic.DynamicMetadata(
            services=services,
            options=options,
            service_availability=service_availability,
            connection_config_defaults=connection_config_defaults,
            raw=profile,
            source="profile",
            ttl_seconds=self.dynamic_ttl_seconds,
            exclusive=True,
        )


def _option_descriptor_for(
    raw_code: str,
    option_enum,
) -> core_dynamic.OptionDescriptor:
    """Map a vendor ServiceID to an :class:`OptionDescriptor`.

    Uses the static :class:`ShippingOption` enum where possible so the dynamic
    catalog reuses the same option keys / metadata the rest of the system
    already understands. Unknown ServiceIDs fall through as a bare descriptor
    keyed on the wire code itself.
    """
    for member in option_enum:
        value = member.value
        if getattr(value, "code", None) == raw_code:
            value_type = "bool"
            inner_type = getattr(value, "type", None)
            if inner_type in (int, float):
                value_type = "float" if inner_type is float else "int"
            elif inner_type is str:
                value_type = "string"
            return core_dynamic.OptionDescriptor(
                code=raw_code,
                name=member.name,
                value_type=value_type,
                meta=dict(getattr(value, "meta", {}) or {}),
            )

    return core_dynamic.OptionDescriptor(
        code=raw_code,
        name=raw_code,
        value_type="bool",
        meta={"category": "DYNAMIC"},
    )


def _pick_default_route(profile: dict) -> tuple[str | None, str | None]:
    """Return (cep_id, product_id) for the first CEP that exposes a product.

    Used to seed the dashboard's ``cep_id`` / ``product_id`` connection-config
    defaults. PA1 is preferred when present so customers see a JTL-routable
    default; otherwise we take the first CEP with at least one product.
    """
    ceps = profile.get("ceps") or {}
    preferred = ("PA1", "DHL", "UPS")
    candidates = [cep for cep in preferred if cep in ceps and (ceps[cep].get("products") or {})]
    candidates.extend(cep for cep in ceps if cep not in candidates and (ceps[cep].get("products") or {}))

    for cep in candidates:
        products = ceps[cep].get("products") or {}
        first_product = next(iter(products), None)
        if first_product:
            return cep, first_product
    return None, None
