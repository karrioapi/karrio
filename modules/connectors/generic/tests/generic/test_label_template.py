import base64
import unittest
import jinja2
import karrio.sdk as karrio
import karrio.addons.label as label
from unittest.mock import patch

from karrio.providers.generic.units import SAMPLE_SHIPMENT_REQUEST
from karrio.core.models import ShipmentRequest


def _gateway(template: str):
    """A custom carrier connection whose owner supplied `template`."""
    return karrio.gateway["generic"].create(
        {
            "carrier_id": "custom-carrier",
            "custom_carrier_name": "custom_carrier",
            "display_name": "Custom Carrier",
            "label_template": {"slug": "custom", "template": template, "template_type": "SVG"},
            "services": [
                dict(
                    service_name="Standard Service",
                    service_code="standard_service",
                    currency="USD",
                    zones=[dict(rate=100.00)],
                )
            ],
        }
    )


def _buy_label(template: str):
    """Buy a label on the connection; PNG keeps the rendered text as is."""
    request = ShipmentRequest(**{**SAMPLE_SHIPMENT_REQUEST, "label_type": "PNG"})
    shipment, messages = karrio.Shipment.create(request).from_(_gateway(template)).parse()
    label_text = base64.b64decode(shipment.docs.label).decode("utf-8") if shipment else None

    return label_text, [m.message for m in messages]


def _rendered_label(template: str) -> str:
    label_text, messages = _buy_label(template)
    assert label_text is not None, messages
    return label_text


class TestGenericLabelTemplateSandbox(unittest.TestCase):
    """Anyone who can create a custom carrier connection chooses its label
    template, and it is rendered on the server when a label is bought."""

    def setUp(self):
        self.maxDiff = None

    def test_the_template_cannot_reach_python_internals(self):
        """Asserted on attribute access only: nothing is executed."""
        probes = [
            "{{ ''.__class__.__mro__ }}",
            "{{ cycler.__init__.__globals__ }}",
            "{{ shipment.__class__.__mro__ }}",
        ]
        for body in probes:
            with self.subTest(body):
                label_text, messages = _buy_label(body)

                self.assertIsNone(label_text)
                self.assertIn("is unsafe", " ".join(messages))

    def test_a_custom_template_still_renders_shipment_data(self):
        body = (
            "{{ tracking_number|length > 0 }}|{{ service_name }}|"
            "{{ shipment.recipient.city }}|{{ package_index }}/{{ total_packages }}|"
            "{% set seen = [] %}{% set _ = seen.append(1) %}{{ seen|length }}"
        )

        self.assertEqual(_rendered_label(body), "True|carrier_premium|Ottawa|1/1|1")

    def test_the_default_label_renders_byte_identical(self):
        contexts = []
        render = label.SANDBOXED_ENV.from_string

        def capture(template):
            compiled = render(template)
            real = compiled.render
            compiled.render = lambda **ctx: contexts.append(ctx) or real(**ctx)
            return compiled

        request = ShipmentRequest(**{**SAMPLE_SHIPMENT_REQUEST, "label_type": "PNG"})
        gateway = karrio.gateway["generic"].create(
            {
                "carrier_id": "custom-carrier",
                "custom_carrier_name": "custom_carrier",
                "display_name": "Custom Carrier",
            }
        )
        with patch.object(label.SANDBOXED_ENV, "from_string", side_effect=capture):
            shipment, _ = karrio.Shipment.create(request).from_(gateway).parse()

        sandboxed = base64.b64decode(shipment.docs.label).decode("utf-8")
        unsandboxed = jinja2.Template(label.DEFAULT_SVG_LABEL_TEMPLATE).render(**contexts[0])
        self.assertEqual(sandboxed, unsandboxed)


if __name__ == "__main__":
    unittest.main()
