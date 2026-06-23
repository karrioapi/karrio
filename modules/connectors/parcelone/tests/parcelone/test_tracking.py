"""ParcelOne tracking tests."""

import unittest
from unittest.mock import patch

import karrio.core.models as models
import karrio.lib as lib
import karrio.sdk as karrio

from .fixture import gateway


class TestParcelOneTracking(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.TrackingRequest = models.TrackingRequest(**TrackingPayload)

    def test_create_tracking_request(self):
        request = gateway.mapper.create_tracking_request(self.TrackingRequest)

        self.assertListEqual(request.serialize(), TrackingRequestJSON)

    def test_get_tracking(self):
        with patch("karrio.mappers.parcelone.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Tracking.fetch(self.TrackingRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/tracklmc/shipment/4050100151016",
            )

    def test_parse_tracking_response(self):
        with patch("karrio.mappers.parcelone.proxy.lib.request") as mock:
            mock.return_value = TrackingResponseJSON
            parsed_response = karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()

            self.assertListEqual(lib.to_dict(parsed_response), ParsedTrackingResponse)

    def test_parse_tracking_no_events_response(self):
        with patch("karrio.mappers.parcelone.proxy.lib.request") as mock:
            mock.return_value = TrackingNoEventsResponseJSON
            parsed_response = karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()

            self.assertListEqual(lib.to_dict(parsed_response), ParsedTrackingNoEventsResponse)

    def test_parse_tracking_code100_maps_to_pending(self):
        """Vendor code '100' (info received) must map to 'pending', not fall through to in_transit."""
        with patch("karrio.mappers.parcelone.proxy.lib.request") as mock:
            mock.return_value = TrackingCode100ResponseJSON
            parsed_response = karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()

            result = lib.to_dict(parsed_response)
            tracker = result[0][0]
            self.assertEqual(tracker["status"], "pending")
            self.assertEqual(tracker["events"][0]["code"], "100")
            self.assertEqual(tracker["events"][0]["status"], "pending")


if __name__ == "__main__":
    unittest.main()


TrackingPayload = {
    "tracking_numbers": ["4050100151016"],
}

TrackingRequestJSON = [
    {"tracking_number": "4050100151016"},
]

ParsedTrackingResponse = [
    [
        {
            "carrier_id": "parcelone",
            "carrier_name": "parcelone",
            "delivered": False,
            "events": [
                {
                    "code": "394",
                    "date": "2021-10-20",
                    "description": "The shipment has left the P1 HUB.",
                    "location": "DE Pohlheim",
                    "status": "in_transit",
                    "time": "14:15 PM",
                    "timestamp": "2021-10-20T14:15:00.000Z",
                },
                {
                    "code": "300",
                    "date": "2021-10-20",
                    "description": "The shipment arrived the P1 HUB.",
                    "location": "DE Pohlheim",
                    "status": "in_transit",
                    "time": "07:01 AM",
                    "timestamp": "2021-10-20T07:01:00.000Z",
                },
                {
                    "code": "P101",
                    "date": "2021-10-18",
                    "description": "Handed over to a carrier.",
                    "location": "DE Fuessen",
                    "status": "in_transit",
                    "time": "07:43 AM",
                    "timestamp": "2021-10-18T07:43:18.000Z",
                },
                {
                    "code": "P100",
                    "date": "2021-10-18",
                    "description": "Prepared for transportation.",
                    "location": "DE Fuessen",
                    "status": "pending",
                    "time": "06:26 AM",
                    "timestamp": "2021-10-18T06:26:05.000Z",
                },
            ],
            "info": {
                "carrier_tracking_link": "https://tools.usps.com/go/TrackConfirmAction?tLabels=LX035843846BE",
            },
            "meta": {
                "last_mile_carrier": "USPS",
                "last_mile_carrier_slug": "correos-de-mexico",
                "last_mile_tracking_number": "LX035843846BE",
            },
            "status": "in_transit",
            "tracking_number": "4050100151016",
        }
    ],
    [],
]

ParsedTrackingNoEventsResponse = [[], []]


TrackingResponseJSON = """{
    "P1Trackno": "4050100151016",
    "TrackingEvents": [
        {
            "EventdateCET": "2021-10-18T08:26:05+02:00",
            "EventdateUTC": "2021-10-18T06:26:05+00:00",
            "Statuscode": "P100",
            "Status": "Prepared for transportation.",
            "Location": "DE Fuessen",
            "DeliveryStatus": "InfoReceived_001"
        },
        {
            "EventdateCET": "2021-10-18T09:43:18+02:00",
            "EventdateUTC": "2021-10-18T07:43:18+00:00",
            "Statuscode": "P101",
            "Status": "Handed over to a carrier.",
            "Location": "DE Fuessen",
            "DeliveryStatus": "Pending_001"
        },
        {
            "EventdateCET": "2021-10-20T09:01:00+02:00",
            "EventdateUTC": "2021-10-20T07:01:00+00:00",
            "Statuscode": "300",
            "Status": "The shipment arrived the P1 HUB.",
            "Location": "DE Pohlheim",
            "DeliveryStatus": "InTransit_003"
        },
        {
            "EventdateCET": "2021-10-20T16:15:00+02:00",
            "EventdateUTC": "2021-10-20T14:15:00+00:00",
            "Statuscode": "394",
            "Status": "The shipment has left the P1 HUB.",
            "Location": "DE Pohlheim",
            "DeliveryStatus": "InTransit_001",
            "CarrierTrackno": "LX035843846BE",
            "Carrier": "USPS",
            "CarrierSlug": "correos-de-mexico",
            "CarrierTrackURL": "https://tools.usps.com/go/TrackConfirmAction?tLabels=LX035843846BE",
            "TrackingEventsStatus": "P1TrackingEndsHere,RequestLMCCarrierTracking"
        }
    ],
    "lang": "en",
    "platform": "",
    "requestor": ""
}"""

TrackingNoEventsResponseJSON = """{
    "Error": "No shipment data found yet, try again later!"
}"""

TrackingCode100ResponseJSON = """{
    "P1Trackno": "4050100151016",
    "TrackingEvents": [
        {
            "EventdateCET": "2026-05-13T10:00:00+02:00",
            "EventdateUTC": "2026-05-13T08:00:00+00:00",
            "Statuscode": "100",
            "Status": "The shipment has been prepared for transportation by the sender.",
            "Location": "DE Berlin",
            "DeliveryStatus": "InfoReceived_001"
        }
    ],
    "lang": "en",
    "platform": "",
    "requestor": ""
}"""
