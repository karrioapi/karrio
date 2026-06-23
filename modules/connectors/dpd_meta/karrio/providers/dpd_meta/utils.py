import base64
import datetime

import karrio.core as core
import karrio.lib as lib


def decode_token_expiry(token: str) -> datetime.datetime | None:
    """Read the META JWT `exp` claim, or None if `token` is not a decodable JWT."""

    def decode() -> datetime.datetime:
        segment = token.split(".")[1]
        payload = lib.to_dict_safe(base64.urlsafe_b64decode(segment + "=" * (-len(segment) % 4)))
        # fromtimestamp yields naive LOCAL, matching _is_token_valid's now()
        return datetime.datetime.fromtimestamp(float(payload["exp"]))

    return lib.failsafe(decode)


def configured_depot(settings, *, geo_routing: bool) -> str | None:
    """The manual `sending_depot` connection-config override, if set.

    DPD requires an origin sending depot; normally it is resolved per request
    from the postal code via the DepotDataService, but a connection may pin a
    fixed depot through the `sending_depot` config value.

    geo_routing=False → the 4-digit depot expected by pickup requests.
    geo_routing=True  → the 7-digit GeoRouting code (BU code + depot) expected
                        by shipment requests.
    """
    depot = settings.connection_config.sending_depot.state
    if not depot:
        return None

    depot = str(depot)
    if not geo_routing:
        return depot

    bu = settings.dpd_bucode
    return f"{bu}{depot}" if bu else depot


class Settings(core.Settings):
    """DPD Meta base connection settings."""

    @property
    def carrier_name(self):
        return "dpd_meta"

    @property
    def server_url(self):
        return (
            "https://api-preprod.dpsin.dpdgroup.com:8443/shipping/v1"
            if self.test_mode
            else "https://api.dpdgroup.com/shipping/v1"
        )

    @property
    def public_ws_url(self):
        """Base URL for DPD Public Web Services (Login + Depot data).

        SOAP endpoints are reached as `{public_ws_url}/{ServiceName}/V{N}_0`.
        Source: DPD API developer guidelines (vendor/dpd-api.developer.guidelines-A4-20250115.pdf).
        """
        return "https://public-ws-stage.dpd.com/services" if self.test_mode else "https://public-ws.dpd.com/services"

    @property
    def tracking_url(self):
        return "https://www.dpdgroup.com/tracking?parcelNumber={}"

    @property
    def connection_config(self) -> lib.units.Options:
        from karrio.providers.dpd_meta.units import ConnectionConfig

        return lib.to_connection_config(
            self.config or {},
            option_type=ConnectionConfig,
        )
