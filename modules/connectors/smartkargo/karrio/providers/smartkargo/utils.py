"""SmartKargo connection utilities."""

import karrio.core as core
import karrio.lib as lib


class Settings(core.Settings):
    """SmartKargo connection settings."""

    # SmartKargo API key (passed as 'code' header)
    code: str
    # Shipper account credentials (required for booking - used as account)
    account_number: str

    @property
    def carrier_name(self):
        return "smartkargo"

    @property
    def server_url(self):
        return (
            "https://uatihub.smartkargo.com/ihub-uat-mt-api-function"
            if self.test_mode
            else "https://ihub.smartkargo.com/ihub-prod-mt-api-function"
        )

    @property
    def tracking_url(self):
        return "https://www.deliverdirect.com/tracking?ref={}"

    @property
    def connection_config(self) -> lib.units.Options:
        from karrio.providers.smartkargo.units import ConnectionConfig

        return lib.to_connection_config(
            self.config or {},
            option_type=ConnectionConfig,
        )


def parse_http_error(error) -> str:
    """Handle HTTP errors, including plain text responses.

    Used as on_error callback for lib.request(). Converts non-JSON
    error bodies (e.g. 'Entity "Site" (name) not found') into
    a JSON string so downstream lib.to_dict() always succeeds.
    """
    body = lib.failsafe(lambda: lib.decode(error.read())) or ""

    # If it's valid JSON, return as-is
    if lib.failsafe(lambda: lib.to_dict(body)) is not None:
        return body

    # Plain text error — wrap in a JSON-serializable error dict
    message = body.strip() or getattr(error, "reason", "Unknown error")
    return lib.to_json({"error": {"code": "API_ERROR", "message": message}})


def parse_void_response(raw: str) -> dict:
    """Parse void API response, handling empty or non-JSON responses."""
    return lib.to_dict_safe(raw)


def extract_booking_data(raw: str) -> dict:
    """Unwrap array-wrapped booking response and extract label URL."""
    response = lib.to_dict_safe(raw)
    # API returns array-wrapped response like [{...}], unwrap it
    data = response.get("data") if "data" in response else response
    if isinstance(data, list):
        response = data[0] if data else response
    shipment = (response.get("shipments") or [{}])[0]
    label_url = shipment.get("labelUrl") if shipment.get("status") == "Booked" else None
    return dict(response=response, label_url=label_url)
