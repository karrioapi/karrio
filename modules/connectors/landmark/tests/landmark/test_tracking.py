"""Landmark Global carrier tracking tests."""

import unittest
from unittest.mock import patch, ANY
from .fixture import gateway

import karrio.sdk as karrio
import karrio.lib as lib
import karrio.core.models as models


class TestLandmarkGlobalTracking(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.TrackingRequest = models.TrackingRequest(
            tracking_numbers=TRACKING_REQUEST_PAYLOAD
        )

    def test_create_tracking_request(self):
        request = gateway.mapper.create_tracking_request(self.TrackingRequest)

        self.assertEqual(request.serialize()[0].request, TRACKING_REQUEST_XML)

    def test_get_tracking(self):
        with patch("karrio.mappers.landmark.proxy.lib.request") as mock:
            mock.return_value = "<a></a>"
            karrio.Tracking.fetch(self.TrackingRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"], f"{gateway.settings.server_url}/Track.php"
            )

    def test_parse_tracking_response(self):
        with patch("karrio.mappers.landmark.proxy.lib.request") as mock:
            mock.return_value = TRACKING_RESPONSE_XML
            parsed_response = (
                karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), PARSED_TRACKING_RESPONSE)

    def test_parse_error_response(self):
        with patch("karrio.mappers.landmark.proxy.lib.request") as mock:
            mock.return_value = ERROR_RESPONSE_XML
            parsed_response = (
                karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )
            self.assertListEqual(lib.to_dict(parsed_response), PARSED_ERROR_RESPONSE)


if __name__ == "__main__":
    unittest.main()

TRACKING_REQUEST_PAYLOAD = ["LTN123121"]

TRACKING_REQUEST_XML = """<TrackRequest>
    <Login>
        <Username>test_username</Username>
        <Password>test_password</Password>
    </Login>
    <Test>true</Test>
    <ClientID>2437</ClientID>
    <TrackingNumber>LTN123121</TrackingNumber>
    <RetrievalType>Historical</RetrievalType>
</TrackRequest>
"""

TRACKING_RESPONSE_XML = """<?xml version="1.0"?>
<TrackResponse>
	<Test>true</Test>
	<Result>
		<Success>true</Success>
		<ShipmentDetails>
			<EndDeliveryCarrier>Sample Carrier</EndDeliveryCarrier>
		</ShipmentDetails>
		<Packages>
			<Package>
				<TrackingNumber>LTN123121</TrackingNumber>
				<LandmarkTrackingNumber>LTN38570269N1</LandmarkTrackingNumber>
				<PackageReference></PackageReference>
				<Events>
					<Event>
						<Status>Customs Clearance in Progress</Status>
						<DateTime>10/01/2025 03:02 PM</DateTime>
						<Location>Anytown, US</Location>
						<EventCode>250</EventCode>
					</Event>
					<Event>
						<Status>US in Transit</Status>
						<DateTime>09/30/2025 11:45 AM</DateTime>
						<Location>Columbus, OH</Location>
						<EventCode>200</EventCode>
					</Event>
				</Events>
			</Package>
		</Packages>
	</Result>
</TrackResponse>"""

ERROR_RESPONSE_XML = """<?xml version="1.0"?>
<TrackResponse>
	<Result>
		<Success>false</Success>
		<ResultMessage>See Errors element for error details</ResultMessage>
	</Result>
	<Errors>
		<Error>
			<ErrorCode>Login</ErrorCode>
			<ErrorMessage>The username/password combination provided is invalid.</ErrorMessage>
		</Error>
	</Errors>
</TrackResponse>"""

PARSED_TRACKING_RESPONSE = [
    [
        {
            "carrier_id": "landmark",
            "carrier_name": "landmark",
            "delivered": False,
            "events": [
                {
                    "code": "250",
                    "date": "2025-10-01",
                    "description": "Customs Clearance in Progress",
                    "location": "Anytown, US",
                    "time": "15:02 PM",
                },
                {
                    "code": "200",
                    "date": "2025-09-30",
                    "description": "US in Transit",
                    "location": "Columbus, OH",
                    "time": "11:45 AM",
                },
            ],
            "info": {
                "carrier_tracking_link": "https://track.landmarkglobal.com/?search=LTN38570269N1"
            },
            "meta": {"carrier": "Sample Carrier"},
            "status": "in_transit",
            "tracking_number": "LTN123121",
        }
    ],
    [],
]

PARSED_ERROR_RESPONSE = [
    [],
    [
        {
            "carrier_id": "landmark",
            "carrier_name": "landmark",
            "code": "Login",
            "details": {"tracking_number": "LTN123121"},
            "message": "The username/password combination provided is invalid.",
        }
    ],
]
