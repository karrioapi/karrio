"""Karrio Teleship OAuth processing implementation."""

import typing
import urllib.parse
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.teleship.error as error
import karrio.providers.teleship.utils as provider_utils


def on_oauth_authorize(
    payload: models.OAuthAuthorizePayload,
    settings: provider_utils.Settings,
) -> typing.Tuple[models.OAuthAuthorizeRequest, typing.List[models.Message]]:
    """Create OAuth authorize request for Teleship.

    Generates the authorization URL and parameters needed to initiate
    the OAuth flow with Teleship.
    """
    messages: typing.List[models.Message] = []

    # Get OAuth credentials from system config
    scope = payload.options.get("scope", "read_accounts write_shipments")

    if not settings.oauth_client_id:
        messages.append(
            models.Message(
                carrier_id=settings.carrier_id,
                carrier_name=settings.carrier_name,
                code="OAUTH_CONFIG_ERROR",
                message="TELESHIP_OAUTH_CLIENT_ID is not configured in system settings",
            )
        )

    # Build authorization URL parameters
    auth_params = dict(
        redirectUri=payload.redirect_uri,
        state=payload.state,
        responseType="code",
        clientId=settings.oauth_client_id,
        scope=scope,
    )

    authorization_url = lib.identity(
        f"{settings.server_url}/oauth/authorize?{urllib.parse.urlencode(auth_params)}"
    )

    return (
        models.OAuthAuthorizeRequest(
            carrier_name=settings.carrier_name,
            authorization_url=authorization_url,
            meta=dict(scope=scope),
        ),
        messages,
    )


def on_oauth_callback(
    payload: models.RequestPayload,
    settings: provider_utils.Settings,
) -> typing.Tuple[typing.Optional[typing.Dict], typing.List[models.Message]]:
    """Process OAuth authorization callback.

    Extracts the authorization code and user credentials from the callback.
    Teleship returns account_client_id and account_client_secret in the callback
    query parameters which are the user's credentials for API access.
    """
    query = payload.query or {}
    messages = error.parse_error_response(payload.body, settings)

    code = query.get("code")
    account_client_id = query.get("account_client_id")
    account_client_secret = query.get("account_client_secret")

    if not code:
        messages.append(
            models.Message(
                carrier_id=settings.carrier_id,
                carrier_name=settings.carrier_name,
                code="OAUTH_CALLBACK_ERROR",
                message="No authorization code received in callback",
            )
        )
        return None, messages

    if not account_client_id or not account_client_secret:
        messages.append(
            models.Message(
                carrier_id=settings.carrier_id,
                carrier_name=settings.carrier_name,
                code="OAUTH_CALLBACK_ERROR",
                message="Missing account credentials in callback",
            )
        )
        return None, messages

    # Return credentials that map to the Teleship connection settings
    credentials = dict(
        client_id=account_client_id,
        client_secret=account_client_secret,
    )

    return credentials, messages
