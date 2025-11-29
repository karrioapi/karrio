"""WEBHOOK TEMPLATES"""
from jinja2 import Template


WEBHOOK_REGISTER_TEMPLATE = Template("""\"\"\"Karrio {{name}} webhook registration implementation.\"\"\"

import typing
import karrio.schemas.{{id}}.webhook_request as {{id}}_req
import karrio.schemas.{{id}}.webhook_response as {{id}}_res
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.{{id}}.error as error
import karrio.providers.{{id}}.utils as provider_utils


def parse_webhook_registration_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.WebhookRegistrationDetails, typing.List[models.Message]]:
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)
    details = lib.to_object({{id}}_res.WebhookResponseType, response)

    webhook_details = lib.identity(
        models.WebhookRegistrationDetails(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            webhook_identifier=details.id,
            secret=details.secret,
            meta=lib.to_dict(details),
        )
        if details and details.id
        else None
    )

    return webhook_details, messages


def webhook_registration_request(
    payload: models.WebhookRegistrationRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    \"\"\"Create a {{name}} webhook registration request\"\"\"

    request = {{id}}_req.WebhookRequestType(
        url=payload.url,
        description=payload.description,
        enabled=True,
        enabledEvents=(payload.enabled_events if any(payload.enabled_events) else ["*"]),
    )

    return lib.Serializable(request, lib.to_dict)
""")


WEBHOOK_DEREGISTER_TEMPLATE = Template("""\"\"\"Karrio {{name}} webhook deregistration implementation.\"\"\"

import typing
import karrio.lib as lib
import karrio.core.models as models
import karrio.providers.{{id}}.error as error
import karrio.providers.{{id}}.utils as provider_utils


def parse_webhook_deregistration_response(
    _response: lib.Deserializable[dict],
    settings: provider_utils.Settings,
) -> typing.Tuple[models.ConfirmationDetails, typing.List[models.Message]]:
    response = _response.deserialize()
    messages = error.parse_error_response(response, settings)

    success = not any(messages) and (
        isinstance(response, dict) and response.get("success") is not False
        or response == ""
        or response is None
    )

    confirmation = lib.identity(
        models.ConfirmationDetails(
            carrier_id=settings.carrier_id,
            carrier_name=settings.carrier_name,
            success=success,
            operation="webhook_deregistration",
        )
        if success
        else None
    )

    return confirmation, messages


def webhook_deregistration_request(
    payload: models.WebhookDeregistrationRequest,
    settings: provider_utils.Settings,
) -> lib.Serializable:
    \"\"\"Create a {{name}} webhook deregistration request\"\"\"

    request = {"webhookId": payload.webhook_id}

    return lib.Serializable(request, lib.to_dict)
""")


WEBHOOK_INIT_TEMPLATE = Template("""from karrio.providers.{{id}}.webhook.register import (
    webhook_registration_request,
    parse_webhook_registration_response,
)
from karrio.providers.{{id}}.webhook.deregister import (
    webhook_deregistration_request,
    parse_webhook_deregistration_response,
)
""")


JSON_SCHEMA_WEBHOOK_REQUEST_TEMPLATE = Template("""{
  "url": "https://example.com/webhook",
  "description": "Tracking milestones webhook",
  "enabled": true,
  "enabledEvents": [
    "shipment.updated",
    "label.generated",
    "manifest.created"
  ],
  "metadata": {
    "shopId": "shop_123456",
    "environment": "production"
  }
}
""")


JSON_SCHEMA_WEBHOOK_RESPONSE_TEMPLATE = Template("""{
  "id": "wh_1234567890abc",
  "url": "https://example.com/webhook",
  "description": "Tracking milestones webhook",
  "enabledEvents": [
    "shipment.updated",
    "label.generated",
    "manifest.created"
  ],
  "secret": "whsec_abcdef1234567890",
  "enabled": true,
  "metadata": {
    "shopId": "shop_123456",
    "environment": "production"
  }
}
""")


TEST_WEBHOOK_TEMPLATE = Template('''"""{{name}} carrier webhook tests."""

import unittest
from unittest.mock import patch
from .fixture import gateway
import karrio.sdk as karrio
import karrio.lib as lib
import karrio.core.models as models


class Test{{compact_name}}Webhook(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.WebhookRegistrationRequest = models.WebhookRegistrationRequest(
            url="https://example.com/webhook",
            description="Test webhook",
            enabled_events=["shipment.updated", "label.generated"],
        )
        self.WebhookDeregistrationRequest = models.WebhookDeregistrationRequest(
            webhook_id="wh_1234567890abc",
        )

    def test_create_webhook_registration_request(self):
        request = gateway.mapper.create_webhook_registration_request(
            self.WebhookRegistrationRequest
        )
        self.assertEqual(lib.to_dict(request.serialize()), WebhookRegistrationRequest)

    def test_register_webhook(self):
        with patch("karrio.mappers.{{id}}.proxy.lib.request") as mock:
            mock.return_value = {% if is_xml_api %}"<r></r>"{% else %}"{}"{% endif %}
            karrio.Webhook.register(self.WebhookRegistrationRequest).from_(gateway)
            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/webhooks"
            )

    def test_deregister_webhook(self):
        with patch("karrio.mappers.{{id}}.proxy.lib.request") as mock:
            mock.return_value = {% if is_xml_api %}"<r></r>"{% else %}"{}"{% endif %}
            karrio.Webhook.deregister(self.WebhookDeregistrationRequest).from_(gateway)
            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/webhooks/wh_1234567890abc"
            )

    def test_parse_webhook_registration_response(self):
        with patch("karrio.mappers.{{id}}.proxy.lib.request") as mock:
            mock.return_value = WebhookRegistrationResponse
            parsed_response = (
                karrio.Webhook.register(self.WebhookRegistrationRequest)
                .from_(gateway)
                .parse()
            )
            self.assertListEqual(lib.to_dict(parsed_response), ParsedWebhookRegistrationResponse)

    def test_parse_webhook_deregistration_response(self):
        with patch("karrio.mappers.{{id}}.proxy.lib.request") as mock:
            mock.return_value = WebhookDeregistrationResponse
            parsed_response = (
                karrio.Webhook.deregister(self.WebhookDeregistrationRequest)
                .from_(gateway)
                .parse()
            )
            self.assertListEqual(lib.to_dict(parsed_response), ParsedWebhookDeregistrationResponse)

    def test_parse_error_response(self):
        with patch("karrio.mappers.{{id}}.proxy.lib.request") as mock:
            mock.return_value = ErrorResponse
            parsed_response = (
                karrio.Webhook.register(self.WebhookRegistrationRequest)
                .from_(gateway)
                .parse()
            )
            self.assertListEqual(lib.to_dict(parsed_response), ParsedErrorResponse)


if __name__ == "__main__":
    unittest.main()


WebhookRegistrationRequest = {
    "url": "https://example.com/webhook",
    "description": "Test webhook",
    "enabled": True,
    "enabledEvents": ["shipment.updated", "label.generated"],
}

WebhookRegistrationResponse = """{
  "id": "wh_1234567890abc",
  "url": "https://example.com/webhook",
  "description": "Test webhook",
  "enabledEvents": ["shipment.updated", "label.generated"],
  "secret": "whsec_abcdef1234567890",
  "enabled": true
}"""

WebhookDeregistrationResponse = """{
  "success": true
}"""

ErrorResponse = """{
  "error": {
    "code": "webhook_error",
    "message": "Unable to register webhook",
    "details": "Invalid URL provided"
  }
}"""

ParsedWebhookRegistrationResponse = [
    {
        "carrier_id": "{{id}}",
        "carrier_name": "{{id}}",
        "webhook_identifier": "wh_1234567890abc",
        "secret": "whsec_abcdef1234567890",
        "meta": {
            "id": "wh_1234567890abc",
            "url": "https://example.com/webhook",
            "description": "Test webhook",
            "enabledEvents": ["shipment.updated", "label.generated"],
            "secret": "whsec_abcdef1234567890",
            "enabled": True,
        },
    },
    [],
]

ParsedWebhookDeregistrationResponse = [
    {
        "carrier_id": "{{id}}",
        "carrier_name": "{{id}}",
        "success": True,
        "operation": "webhook_deregistration",
    },
    [],
]

ParsedErrorResponse = [
    None,
    [
        {
            "carrier_id": "{{id}}",
            "carrier_name": "{{id}}",
            "code": "webhook_error",
            "message": "Unable to register webhook",
            "details": {
                "details": "Invalid URL provided"
            },
        }
    ],
]
''')
