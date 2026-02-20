"""SmartKargo connection utilities."""

import karrio.lib as lib
import karrio.core as core


def parse_void_response(raw: str) -> dict:
    """Parse void API response, handling empty or non-JSON responses."""
    if not raw:
        return {"error": {"code": "EMPTY_RESPONSE", "message": "Void API returned empty response"}}
    try:
        return lib.to_dict(raw)
    except (ValueError, TypeError):
        # API may return plain text errors like 'Entity "Shipment (...) not found'
        return {"error": {"code": "API_ERROR", "message": str(raw).strip()}}


def extract_booking_data(raw: str) -> dict:
    """Unwrap array-wrapped booking response and extract label URL."""
    response = lib.to_dict(raw)
    # API returns array-wrapped response like [{...}], unwrap it
    response = response[0] if isinstance(response, list) else response
    shipment = (response.get("shipments") or [{}])[0]
    label_url = (
        shipment.get("labelUrl")
        if shipment.get("status") == "Booked"
        else None
    )
    return dict(response=response, label_url=label_url)


class Settings(core.Settings):
    """SmartKargo connection settings."""

    # SmartKargo API key (passed as 'code' header)
    api_key: str
    # Shipper account credentials (required for booking - used as primaryId and account)
    account_number: str
    account_id: str

    @property
    def carrier_name(self):
        return "smartkargo"

    @property
    def server_url(self):
        return (
            "https://uatihub.smartkargo.com/ihub-uat-mt-api-function"
            if self.test_mode
            else "https://ihub.smartkargo.com/ihub-mt-api-function"
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
