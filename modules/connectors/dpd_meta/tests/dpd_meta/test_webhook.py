"""DPD Meta Tracking Push (webhook) tests."""

import unittest

import karrio.core.models as models
import karrio.lib as lib
from karrio.providers.dpd_meta.hooks import on_webhook_event

from .fixture import gateway


def parse(query: dict) -> models.WebhookEventDetails:
    details, _ = on_webhook_event(models.RequestPayload(url="", query=query), gateway.settings)
    return details


class TestDPDMetaWebhook(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_parse_push_event(self):
        self.assertDictEqual(lib.to_dict(parse(DeliveredPush)), ParsedDeliveredPush)

    def test_status_mapping(self):
        # Known codes map to their unified status; an unknown code yields None so
        # update_tracker leaves the stored status untouched (no downgrade).
        statuses = {
            code: parse(dict(pushid="1", pnr="01234567890123", status=code)).tracking.status for code in STATUS_MAP
        }
        self.assertDictEqual(statuses, STATUS_MAP)

    def test_unmatched_parcel_is_acknowledged(self):
        # No parcel number -> nothing to update, but DPD still gets its receipt.
        details = parse(dict(pushid="999", status="start_order"))
        self.assertIsNone(details.tracking)
        self.assertEqual(details.response, "<push><pushid>999</pushid><status>OK</status></push>")

    def test_malformed_statusdate_is_ignored(self):
        # A bad statusdate must not raise (that would 500 and skip the ack).
        details = parse(dict(pushid="1", pnr="01234567890123", status="delivery_customer", statusdate="bad"))
        self.assertIsNone(details.tracking.events[0].date)
        self.assertEqual(details.response, "<push><pushid>1</pushid><status>OK</status></push>")


DeliveredPush = {
    "pushid": "335298",
    "ref": "ORDER-4711",
    "pnr": "01234567890123",
    "depot": "0163",
    "status": "delivery_customer",
    "statusdate": "04122025071600",
    "receiver": "Mustermann",
    "services": "101_DE_97350_NC_EXPA",
    "pod": "POD123",
}

ParsedDeliveredPush = {
    "carrier_id": "dpd_meta",
    "carrier_name": "dpd_meta",
    "response": "<push><pushid>335298</pushid><status>OK</status></push>",
    "response_format": "xml",
    "tracking_number": "01234567890123",
    "tracking": {
        "carrier_id": "dpd_meta",
        "carrier_name": "dpd_meta",
        "delivered": True,
        "status": "delivered",
        "tracking_number": "01234567890123",
        "events": [
            {
                "code": "delivery_customer",
                "date": "2025-12-04",
                "description": "Delivered to customer",
                "location": "0163",
                "time": "07:16 AM",
            }
        ],
        "info": {
            "carrier_tracking_link": "https://www.dpdgroup.com/tracking?parcelNumber=01234567890123",
            "shipment_service": "101_DE_97350_NC_EXPA",
            "signed_by": "Mustermann",
        },
        "meta": {
            "depot": "0163",
            "pod": "POD123",
            "pushid": "335298",
            "reference": "ORDER-4711",
            "services": "101_DE_97350_NC_EXPA",
        },
    },
}

STATUS_MAP = {
    "start_order": "pending",
    "pickup_driver": "picked_up",
    "pickup_depot": "in_transit",
    "delivery_depot": "in_transit",
    "delivery_nab": "in_transit",
    "delivery_carload": "out_for_delivery",
    "delivery_notification": "on_hold",
    "delivery_customer": "delivered",
    "delivery_shop": "ready_for_pickup",
    "error_pickup": "delivery_failed",
    "error_return": "return_to_sender",
    "pickup_by_consignee": "delivered",
    "no_pickup_by_consignee": "return_to_sender",
    "unrecognised_code": None,
}


if __name__ == "__main__":
    unittest.main()
