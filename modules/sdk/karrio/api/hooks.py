"""Karrio Hooks abstract class definition module."""

import abc
import attr
import typing
import karrio.core.models as models
import karrio.core.errors as errors
import karrio.core.settings as core_settings


@attr.s(auto_attribs=True)
class Hooks(abc.ABC):
    """Unified Shipping API Hooks (Interface)"""

    settings: core_settings.Settings

    def on_webhook_event(
        self, payload: models.RequestPayload
    ) -> typing.Tuple[models.WebhookEventDetails, typing.List[models.Message]]:
        """Process a webhook event from a carrier webservice

        Args:
            payload (RequestPayload): a request payload (xml, json, text...)

        Returns:
            Tuple[WebhookEventDetails, List[Message]]: the webhook event details
                as well as errors and messages returned

        Raises:
            MethodNotSupportedError: Is raised when the carrier integration does not implement this method
        """
        raise errors.MethodNotSupportedError(
            self.__class__.on_webhook_event.__name__,
            self.settings.carrier_name,
        )

    def on_oauth_authorize(
        self, payload: models.OAuthAuthorizePayload
    ) -> typing.Tuple[models.OAuthAuthorizeRequest, typing.List[models.Message]]:
        """Create a OAuth authorize request for a carrier OAuth flow

        Args:
            payload (OAuthAuthorizePayload): a OAuth authorize request payload

        Returns:
            Tuple[OAuthAuthorizeResponse, List[Message]]: the OAuth authorize response details
                as well as errors and messages returned

        Raises:
            MethodNotSupportedError: Is raised when the carrier integration does not implement this method
        """
        raise errors.MethodNotSupportedError(
            self.__class__.on_oauth_authorize.__name__,
            self.settings.carrier_name,
        )

    def on_oauth_callback(
        self, payload: models.RequestPayload
    ) -> typing.Tuple[typing.Optional[typing.Dict], typing.List[models.Message]]:
        """Process a OAuth callback from a carrier webservice

        Args:
            payload (RequestPayload): a request payload (xml, json, text...)
        """
        raise errors.MethodNotSupportedError(
            self.__class__.on_oauth_callback.__name__,
            self.settings.carrier_name,
        )
