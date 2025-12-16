
import base64
import datetime
import karrio.lib as lib
import karrio.core as core
import karrio.core.errors as errors


class Settings(core.Settings):
    """DPD Group connection settings."""

    # DPD META-API authentication properties
    # Required
    bucode: str  # Business Unit code (X-DPD-BUCODE)

    # Authentication method 1: Username/Password
    username: str = None  # X-DPD-LOGIN
    password: str = None  # X-DPD-PASSWORD

    # Authentication method 2: Client credentials
    client_id: str = None  # X-DPD-CLIENTID
    client_secret: str = None  # X-DPD-CLIENTSECRET

    # Optional account information
    account_number: str = None
    customer_account_number: str = None

    @property
    def carrier_name(self):
        return "dpd_group"

    @property
    def server_url(self):
        return (
            "https://api-preprod.dpsin.dpdgroup.com:8443/shipping/v1"
            if self.test_mode
            else "https://api.dpdgroup.com/shipping/v1"
        )

    @property
    def tracking_url(self):
        return "https://www.dpdgroup.com/tracking?parcelNumber={}"

    @property
    def connection_config(self) -> lib.units.Options:
        from karrio.providers.dpd_group.units import ConnectionConfig

        return lib.to_connection_config(
            self.config or {},
            option_type=ConnectionConfig,
        )


def login(settings: Settings):
    """Login to DPD META-API and get access token from response headers."""
    import karrio.providers.dpd_group.error as error
    import json

    url = f"{settings.server_url}/login"

    # Defensive normalization: avoid invisible whitespace causing LOGIN_8.
    bucode = (settings.bucode or "").strip()
    username = (settings.username or "").strip()
    password = (settings.password or "").strip()
    client_id = (settings.client_id or "").strip()
    client_secret = (settings.client_secret or "").strip()
    
    # DPD META-API login uses custom headers for authentication.
    # Depending on account setup, credentials can be provided either as:
    # - X-DPD-LOGIN + X-DPD-PASSWORD + X-DPD-BUCODE
    # - X-DPD-CLIENTID + X-DPD-CLIENTSECRET + X-DPD-BUCODE
    if not any(bucode):
        raise errors.ShippingSDKError("DPD login failed: missing BUCODE (X-DPD-BUCODE)")

    has_user_pass = any([username, password])
    has_client_creds = any([client_id, client_secret])

    if has_user_pass and has_client_creds:
        # Avoid ambiguous configuration.
        raise errors.ShippingSDKError(
            "DPD login failed: provide either (username/password) OR (client_id/client_secret), not both."
        )

    if not has_user_pass and not has_client_creds:
        raise errors.ShippingSDKError(
            "DPD login failed: missing credentials. Provide username/password or client_id/client_secret."
        )

    headers = {"X-DPD-BUCODE": bucode}
    if has_client_creds:
        if not all([client_id, client_secret]):
            raise errors.ShippingSDKError(
                "DPD login failed: both client_id and client_secret are required."
            )
        headers.update(
            {
                "X-DPD-CLIENTID": client_id,
                "X-DPD-CLIENTSECRET": client_secret,
            }
        )
    else:
        if not all([username, password]):
            raise errors.ShippingSDKError(
                "DPD login failed: both username and password are required."
            )
        headers.update(
            {
                "X-DPD-LOGIN": username,
                "X-DPD-PASSWORD": password,
            }
        )
    
    # Use lib.request but capture the full response to access headers
    # We'll need to use urllib directly since lib.request doesn't expose headers
    import urllib.request
    import urllib.error
    
    # Create request with POST method but no body data
    # Not passing 'data' parameter means no Content-Length header is set
    request = urllib.request.Request(url, headers=headers, method="POST")
    
    try:
        with urllib.request.urlopen(request) as response:
            # Extract token from response headers
            token = response.headers.get("X-DPD-TOKEN") or response.headers.get("x-dpd-token")
            
            if not token:
                # Log the actual response for debugging
                body = response.read().decode('utf-8')
                raise errors.ShippingSDKError(
                    f"DPD login succeeded but no token in headers. "
                    f"Response headers: {dict(response.headers)}. "
                    f"Body: {body}"
                )
            
            # Token is valid for 24 hours according to DPD docs
            expiry = datetime.datetime.now() + datetime.timedelta(hours=24)
            
            return {
                "access_token": token,
                "token_type": "Bearer",
                "expires_in": 86400,  # 24 hours in seconds
                "expiry": lib.fdatetime(expiry),
            }
            
    except urllib.error.HTTPError as e:
        # Parse DPD error response
        body = e.read().decode('utf-8')

        # Use Karrio's Loguru logger so it shows in server logs.
        from karrio.core.utils.logger import logger

        # Never log secrets (password). Username/bucode are generally ok but keep it minimal.
        logger.error(
            "DPD login failed: HTTP {code} {reason} | url={url} | bucode={bucode}",
            code=e.code,
            reason=e.reason,
            url=url,
            bucode=bucode,
        )
        if any(body or ""):
            logger.error("DPD login error body: {body}", body=body)

        try:
            error_data = json.loads(body) if body else {}
            messages = error.parse_error_response(error_data, settings)
            if any(messages):
                details = "; ".join(
                    f"{m.code}: {m.message} ({m.details})" for m in messages
                )
                # IMPORTANT: raise a ShippingSDKError with details in the message.
                # ThreadSafeTokenManager will wrap `str(e)`; ParsedMessagesError would
                # always show "Invalid request payload" and hide the real DPD error.
                raise errors.ShippingSDKError(
                    f"DPD login failed: {details} (HTTP {e.code} {e.reason}) | url={url}"
                )
        except (json.JSONDecodeError, ValueError):
            # Fall back to raw body below.
            pass

        # Fallback: expose raw body in the exception message (truncate to avoid huge logs).
        raw = (body or "").strip()
        if len(raw) > 1000:
            raw = raw[:1000] + "…(truncated)"

        raise errors.ShippingSDKError(
            f"DPD login failed: HTTP {e.code} {e.reason} | url={url} | body={raw}"
        )
