"""Example: Error Handling, Proxy & Settings Patterns

This example demonstrates comprehensive patterns for:
1. Error parsing (JSON and XML)
2. Proxy implementation (all HTTP methods, auth types)
3. Settings/Utils (credentials, OAuth, caching)
"""

# =============================================================================
# ERROR HANDLING PATTERNS
# =============================================================================

# === FILE: karrio/providers/[carrier]/error.py ===

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.[carrier].utils as provider_utils


def parse_error_response(
    response: typing.Union[dict, lib.Element],
    settings: provider_utils.Settings,
    **kwargs,
) -> typing.List[models.Message]:
    """Parse carrier error response into Karrio messages.
    
    This function MUST handle various error formats from the carrier API.
    Always check for errors in the standard locations.
    """
    
    # For JSON APIs
    if isinstance(response, dict):
        return _parse_json_errors(response, settings, **kwargs)
    
    # For XML APIs
    return _parse_xml_errors(response, settings, **kwargs)


def _parse_json_errors(
    response: dict,
    settings: provider_utils.Settings,
    **kwargs,
) -> typing.List[models.Message]:
    """Parse JSON error responses.
    
    Common patterns to check:
    - response.get("errors", [])
    - response.get("error", {})
    - response.get("errorResponse", {}).get("errors", [])
    - response.get("fault", {})
    - response.get("message") with response.get("code")
    """
    messages = []
    
    # Pattern 1: errors array
    errors = response.get("errors", [])
    if isinstance(errors, dict):
        errors = [errors]
    
    # Pattern 2: single error object
    if not errors and response.get("error"):
        error_obj = response.get("error")
        if isinstance(error_obj, str):
            errors = [{"message": error_obj}]
        else:
            errors = [error_obj]
    
    # Pattern 3: nested errorResponse
    if not errors and response.get("errorResponse"):
        errors = response.get("errorResponse", {}).get("errors", [])
    
    # Pattern 4: fault (SOAP-style in JSON)
    if not errors and response.get("fault"):
        fault = response.get("fault")
        errors = [fault] if isinstance(fault, dict) else [{"message": str(fault)}]
    
    # Pattern 5: top-level code + message
    if not errors and response.get("code") and response.get("message"):
        errors = [{"code": response.get("code"), "message": response.get("message")}]
    
    # Pattern 6: validation errors
    if not errors and response.get("validationErrors"):
        val_errors = response.get("validationErrors", [])
        errors = val_errors if isinstance(val_errors, list) else [val_errors]
    
    # Build Message objects
    for error in errors:
        # Extract code - try multiple field names
        code = (
            error.get("code")
            or error.get("errorCode")
            or error.get("Code")
            or error.get("type")
            or ""
        )
        
        # Extract message - try multiple field names
        message = (
            error.get("message")
            or error.get("errorMessage")
            or error.get("Message")
            or error.get("description")
            or error.get("detail")
            or str(error)
        )
        
        # Determine severity level
        level = (
            "warning"
            if error.get("severity", "").lower() == "warning"
            or error.get("type", "").lower() == "warning"
            else "error"
        )
        
        # Build details dict with additional context
        details = {
            k: v for k, v in {
                **kwargs,  # Include any passed context (e.g., tracking_number)
                "field": error.get("field") or error.get("property"),
                "details": error.get("details") or error.get("additionalInfo"),
            }.items()
            if v is not None
        }
        
        messages.append(
            models.Message(
                carrier_id=settings.carrier_id,
                carrier_name=settings.carrier_name,
                code=str(code),
                message=str(message),
                level=level,
                details=details or None,
            )
        )
    
    return messages


def _parse_xml_errors(
    response: lib.Element,
    settings: provider_utils.Settings,
    **kwargs,
) -> typing.List[models.Message]:
    """Parse XML error responses.
    
    Use XPath to find error elements in various locations.
    """
    messages = []
    
    # Try different XPath patterns for error elements
    error_xpaths = [
        ".//error",
        ".//Error",
        ".//errors/error",
        ".//fault",
        ".//Fault",
        ".//errorResponse/error",
        ".//Errors/Error",
    ]
    
    error_elements = []
    for xpath in error_xpaths:
        found = response.xpath(xpath)
        if found:
            error_elements = found
            break
    
    for error in error_elements:
        # Extract code
        code_element = (
            error.find("code")
            or error.find("Code")
            or error.find("errorCode")
            or error.find("ErrorCode")
        )
        code = code_element.text if code_element is not None else ""
        
        # Extract message
        message_element = (
            error.find("message")
            or error.find("Message")
            or error.find("description")
            or error.find("Description")
        )
        message = message_element.text if message_element is not None else error.text or ""
        
        messages.append(
            models.Message(
                carrier_id=settings.carrier_id,
                carrier_name=settings.carrier_name,
                code=str(code),
                message=str(message),
                details=kwargs or None,
            )
        )
    
    return messages


# =============================================================================
# PROXY IMPLEMENTATION PATTERNS
# =============================================================================

# === FILE: karrio/mappers/[carrier]/proxy.py ===

import karrio.lib as lib
import karrio.api.proxy as proxy
import karrio.mappers.[carrier].settings as provider_settings


class Proxy(proxy.Proxy):
    """Carrier API proxy implementing HTTP communication.
    
    Key responsibilities:
    1. Build request URLs
    2. Set authentication headers
    3. Make HTTP requests
    4. Handle response deserialization
    """
    settings: provider_settings.Settings

    # ----- JSON API Methods -----
    
    def get_rates(self, request: lib.Serializable) -> lib.Deserializable[str]:
        """Fetch shipping rates."""
        response = lib.request(
            url=f"{self.settings.server_url}/v1/rates",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                **self._get_auth_headers(),
            },
        )
        return lib.Deserializable(response, lib.to_dict)
    
    def create_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        """Create shipment and generate label."""
        response = lib.request(
            url=f"{self.settings.server_url}/v1/shipments",
            data=lib.to_json(request.serialize()),
            trace=self.trace_as("json"),
            method="POST",
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                **self._get_auth_headers(),
            },
        )
        return lib.Deserializable(response, lib.to_dict)
    
    def cancel_shipment(self, request: lib.Serializable) -> lib.Deserializable[str]:
        """Cancel/void a shipment."""
        data = request.serialize()
        shipment_id = data.get("shipmentId") or data.get("shipment_id")
        
        # Some carriers use DELETE, others use POST to cancel endpoint
        response = lib.request(
            url=f"{self.settings.server_url}/v1/shipments/{shipment_id}",
            trace=self.trace_as("json"),
            method="DELETE",  # Or POST to /shipments/{id}/cancel
            headers={
                "Accept": "application/json",
                **self._get_auth_headers(),
            },
        )
        return lib.Deserializable(response, lib.to_dict)
    
    def get_tracking(self, request: lib.Serializable) -> lib.Deserializable:
        """Fetch tracking for multiple numbers concurrently."""
        
        def _get_tracking(tracking_number: str):
            """Fetch single tracking number."""
            return tracking_number, lib.request(
                url=f"{self.settings.server_url}/v1/tracking/{tracking_number}",
                trace=self.trace_as("json"),
                method="GET",
                headers={
                    "Accept": "application/json",
                    **self._get_auth_headers(),
                },
            )
        
        # Execute tracking requests concurrently
        responses = lib.run_concurently(
            _get_tracking,
            request.serialize(),  # List of tracking numbers
            max_workers=2,
        )
        
        return lib.Deserializable(
            responses,
            lambda res: [
                (num, lib.to_dict(r)) for num, r in res if any(r.strip())
            ],
        )
    
    # ----- XML API Methods -----
    
    def get_rates_xml(self, request: lib.Serializable) -> lib.Deserializable[lib.Element]:
        """Fetch rates via XML API."""
        response = lib.request(
            url=f"{self.settings.server_url}/api/rate",
            data=request.serialize(),  # Already XML string
            trace=self.trace_as("xml"),
            method="POST",
            headers={
                "Content-Type": "application/xml",
                "Accept": "application/xml",
                **self._get_auth_headers(),
            },
        )
        return lib.Deserializable(response, lib.to_element)
    
    # ----- SOAP API Methods -----
    
    def get_rates_soap(self, request: lib.Serializable) -> lib.Deserializable[lib.Element]:
        """Fetch rates via SOAP API."""
        response = lib.request(
            url=f"{self.settings.server_url}/RatingService",
            data=request.serialize(),  # SOAP envelope XML
            trace=self.trace_as("xml"),
            method="POST",
            headers={
                "Content-Type": "text/xml; charset=utf-8",
                "SOAPAction": "http://carrier.com/RatingService/GetRates",
                **self._get_auth_headers(),
            },
        )
        return lib.Deserializable(response, lib.to_element)
    
    # ----- Authentication Helpers -----
    
    def _get_auth_headers(self) -> dict:
        """Build authentication headers based on auth type."""
        
        # API Key authentication
        if hasattr(self.settings, 'api_key') and self.settings.api_key:
            return {
                "Authorization": f"Bearer {self.settings.api_key}",
                # Or some carriers use custom headers:
                # "X-API-Key": self.settings.api_key,
            }
        
        # Basic authentication
        if hasattr(self.settings, 'authorization'):
            return {
                "Authorization": f"Basic {self.settings.authorization}",
            }
        
        # OAuth authentication
        if hasattr(self.settings, 'access_token'):
            return {
                "Authorization": f"Bearer {self.settings.access_token}",
            }
        
        return {}
    
    # ----- OAuth Token Refresh -----
    
    def authenticate(self, request: lib.Serializable = None) -> lib.Deserializable[dict]:
        """Authenticate and get access token.
        
        Called by settings.access_token property for OAuth flows.
        """
        response = lib.request(
            url=f"{self.settings.oauth_url}/token",
            method="POST",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data=lib.to_query_string({
                "grant_type": "client_credentials",
                "client_id": self.settings.client_id,
                "client_secret": self.settings.client_secret,
            }),
            decoder=lib.to_dict,
        )
        
        return lib.Deserializable(response)


# =============================================================================
# SETTINGS & UTILS PATTERNS
# =============================================================================

# === FILE: karrio/providers/[carrier]/utils.py ===

import base64
import datetime
import karrio.lib as lib
import karrio.core as core
import karrio.core.errors as errors


class Settings(core.Settings):
    """Carrier connection settings.
    
    Define all carrier-specific credentials and configuration here.
    The settings class is the single source of truth for connection config.
    """
    
    # ----- API Key Authentication -----
    api_key: str = None
    
    # ----- Basic Authentication -----
    username: str = None
    password: str = None
    
    # ----- OAuth Authentication -----
    client_id: str = None
    client_secret: str = None
    
    # ----- Account Information -----
    account_number: str = None
    meter_number: str = None  # Some carriers (e.g., FedEx) require this
    
    @property
    def carrier_name(self) -> str:
        """Return carrier identifier (matches the extension id)."""
        return "carrier"
    
    @property
    def server_url(self) -> str:
        """Return API base URL based on test_mode."""
        return (
            "https://api.sandbox.carrier.com"
            if self.test_mode
            else "https://api.carrier.com"
        )
    
    @property
    def oauth_url(self) -> str:
        """Return OAuth token URL."""
        return (
            "https://auth.sandbox.carrier.com"
            if self.test_mode
            else "https://auth.carrier.com"
        )
    
    @property
    def tracking_url(self) -> str:
        """Return public tracking URL template.
        
        Used to generate carrier_tracking_link in TrackingInfo.
        """
        return "https://www.carrier.com/tracking?id={}"
    
    # ----- Basic Auth Helper -----
    
    @property
    def authorization(self) -> str:
        """Generate Basic auth header value."""
        pair = f"{self.username}:{self.password}"
        return base64.b64encode(pair.encode("utf-8")).decode("ascii")
    
    # ----- OAuth Token with Caching -----
    
    @property
    def access_token(self) -> str:
        """Get valid OAuth access token with automatic refresh.
        
        Uses connection_cache for thread-safe token management.
        Tokens are refreshed 30 minutes before expiry.
        """
        cache_key = f"{self.carrier_name}|{self.client_id}|{self.client_secret}"
        
        def get_token():
            """Fetch new token from OAuth endpoint."""
            response = lib.request(
                url=f"{self.oauth_url}/token",
                method="POST",
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                data=lib.to_query_string({
                    "grant_type": "client_credentials",
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                }),
                decoder=lib.to_dict,
            )
            
            # Check for errors
            if "error" in response:
                raise errors.ShippingSDKError(
                    response.get("error_description", "OAuth authentication failed")
                )
            
            # Calculate expiry time
            expiry = datetime.datetime.now() + datetime.timedelta(
                seconds=float(response.get("expires_in", 3600))
            )
            
            return {
                **response,
                "expiry": lib.fdatetime(expiry),
            }
        
        # Use thread-safe token caching
        token = self.connection_cache.thread_safe(
            refresh_func=get_token,
            cache_key=cache_key,
            buffer_minutes=30,  # Refresh 30 min before expiry
            token_field="access_token",
        )
        
        return token.get("access_token")
    
    # ----- Connection Config -----
    
    @property
    def connection_config(self) -> lib.units.Options:
        """Parse connection configuration options.
        
        Connection config allows users to set carrier-specific options
        at the connection level (e.g., default currency, label format).
        """
        from karrio.providers.[carrier].units import ConnectionConfig
        
        return lib.to_connection_config(
            self.config or {},
            option_type=ConnectionConfig,
        )


# === FILE: karrio/mappers/[carrier]/settings.py ===

import attr
import karrio.providers.[carrier].utils as provider_utils


@attr.s(auto_attribs=True)
class Settings(provider_utils.Settings):
    """Carrier connection settings (exposed to users).
    
    This class extends the provider Settings and adds the standard
    Karrio settings fields. Users create connections using this class.
    """
    
    # Carrier-specific credentials (copy from provider_utils.Settings)
    api_key: str = None
    username: str = None
    password: str = None
    client_id: str = None
    client_secret: str = None
    account_number: str = None
    
    # Standard Karrio settings (DO NOT MODIFY)
    id: str = None
    test_mode: bool = False
    carrier_id: str = "carrier"  # Must match extension ID
    account_country_code: str = None
    metadata: dict = {}
    config: dict = {}


# =============================================================================
# UNITS PATTERNS (ConnectionConfig)
# =============================================================================

# === FILE: karrio/providers/[carrier]/units.py (ConnectionConfig section) ===

import karrio.lib as lib


class ConnectionConfig(lib.Enum):
    """Connection-level configuration options.
    
    These options can be set when creating a carrier connection
    and apply to all operations using that connection.
    """
    
    # Currency preference for rates
    currency = lib.OptionEnum("currency", str, default="USD")
    
    # Label format preference
    label_type = lib.OptionEnum("label_type", str, default="PDF")
    
    # Account-specific settings
    cost_centre_id = lib.OptionEnum("cost_centre_id", str)
    cost_centre_name = lib.OptionEnum("cost_centre_name", str)
    
    # Service filtering (for hub carriers)
    shipping_services = lib.OptionEnum("shipping_services", list)
    shipping_options = lib.OptionEnum("shipping_options", list)
    
    # Carrier-specific toggles
    use_paperless = lib.OptionEnum("use_paperless", bool, default=True)
    include_insurance = lib.OptionEnum("include_insurance", bool, default=False)


# Usage in provider functions:
"""
def rate_request(payload, settings):
    # Access connection config
    currency = settings.connection_config.currency.state or "USD"
    use_paperless = settings.connection_config.use_paperless.state
    
    # Use in request building
    request = RateRequest(
        currency=currency,
        paperless=use_paperless,
        # ...
    )
"""
