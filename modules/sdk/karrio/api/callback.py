"""Karrio Callback abstract class definition module."""

import abc
import attr
import typing
import functools
import karrio.lib as lib
import karrio.core.models as models
import karrio.core.errors as errors
import karrio.core.settings as settings


@attr.s(auto_attribs=True)
class Callback(abc.ABC):
    """Unified Shipping API Callback (Interface)"""

    settings: typing.Optional[settings.Settings] = None

    def trace(self, *args, **kwargs):
        if self.settings:
            return self.settings.trace(*args, **kwargs)

        return lib.Tracer().trace(*args, **kwargs)

    def trace_as(self, format: str):
        return functools.partial(self.trace, format=format)

    def process_webhook_event(
        self, response: lib.Deserializable
    ) -> typing.Tuple[models.WebhookEventDetails, typing.List[models.Message]]:
        """Process a webhook event from a carrier webservice

        Args:
            response (Deserializable): a deserializable webhook event response (xml, json, text...)

        Returns:
            Tuple[WebhookEventDetails, List[Message]]: the webhook event details
                as well as errors and messages returned

        Raises:
            MethodNotSupportedError: Is raised when the carrier integration does not implement this method
        """
        raise errors.MethodNotSupportedError(
            self.__class__.process_webhook_event.__name__,
            self.settings.carrier_name,
        )

    def process_oauth_callback(
        self, response: lib.Deserializable
    ) -> typing.Tuple[typing.List[typing.Dict], typing.List[models.Message]]:
        """Process a OAuth callback from a carrier webservice

        Args:
            response (Deserializable): a deserializable OAuth response (xml, json, text...)
        """
        raise errors.MethodNotSupportedError(
            self.__class__.process_oauth_callback.__name__,
            self.settings.carrier_name,
        )
