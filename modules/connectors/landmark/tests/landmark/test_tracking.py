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

    def test_parse_in_transit_response(self):
        with patch("karrio.mappers.landmark.proxy.lib.request") as mock:
            mock.return_value = IN_TRANSIT_TRACKING_RESPONSE_XML
            parsed_response = (
                karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )
            self.assertListEqual(
                lib.to_dict(parsed_response), PARSED_IN_TRANSIT_RESPONSE
            )

    def test_parse_out_for_delivery_response(self):
        with patch("karrio.mappers.landmark.proxy.lib.request") as mock:
            mock.return_value = OUT_FOR_DELIVERY_TRACKING_RESPONSE_XML
            parsed_response = (
                karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )
            self.assertListEqual(
                lib.to_dict(parsed_response), PARSED_OUT_FOR_DELIVERY_RESPONSE
            )

    def test_parse_delivered_response(self):
        with patch("karrio.mappers.landmark.proxy.lib.request") as mock:
            mock.return_value = DELIVERED_TRACKING_RESPONSE_XML
            parsed_response = (
                karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )
            self.assertListEqual(
                lib.to_dict(parsed_response), PARSED_DELIVERED_RESPONSE
            )

    def test_parse_delivery_failed_response(self):
        with patch("karrio.mappers.landmark.proxy.lib.request") as mock:
            mock.return_value = DELIVERY_FAILED_TRACKING_RESPONSE_XML
            parsed_response = (
                karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )
            self.assertListEqual(
                lib.to_dict(parsed_response), PARSED_DELIVERY_FAILED_RESPONSE
            )

    def test_parse_midnight_time_sorting_response(self):
        """Test that events with midnight times (12:35 AM, 01:35 AM) are sorted correctly"""
        with patch("karrio.mappers.landmark.proxy.lib.request") as mock:
            mock.return_value = MIDNIGHT_TIME_SORTING_RESPONSE_XML
            parsed_response = (
                karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )
            self.assertListEqual(
                lib.to_dict(parsed_response), PARSED_MIDNIGHT_TIME_SORTING_RESPONSE
            )

    def test_parse_to_be_routed_response(self):
        """Test that 'To Be Routed' EndDeliveryCarrier excludes last_mile_carrier from meta"""
        with patch("karrio.mappers.landmark.proxy.lib.request") as mock:
            mock.return_value = TO_BE_ROUTED_TRACKING_RESPONSE_XML
            parsed_response = (
                karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )
            self.assertListEqual(
                lib.to_dict(parsed_response), PARSED_TO_BE_ROUTED_RESPONSE
            )


if __name__ == "__main__":
    unittest.main()

TRACKING_REQUEST_PAYLOAD = ["LTN123121"]


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
                    "status": "in_transit",
                    "time": "03:02 PM",
                    "timestamp": "2025-10-01T15:02:00.000Z",
                },
                {
                    "code": "200",
                    "date": "2025-09-30",
                    "description": "US in Transit",
                    "location": "Columbus, OH",
                    "status": "in_transit",
                    "time": "11:45 AM",
                    "timestamp": "2025-09-30T11:45:00.000Z",
                },
            ],
            "info": {
                "carrier_tracking_link": "https://track.landmarkglobal.com/?search=LTN38570269N1"
            },
            "meta": {
                "last_mile_tracking_number": "LTN123121",
                "last_mile_carrier": "Sample Carrier",
            },
            "status": "in_transit",
            "tracking_number": "LTN38570269N1",
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

PARSED_IN_TRANSIT_RESPONSE = [
    [
        {
            "carrier_id": "landmark",
            "carrier_name": "landmark",
            "delivered": False,
            "events": [
                {
                    "code": "275",
                    "date": "2025-10-01",
                    "description": "Item in transit with carrier",
                    "location": "Toronto, ON, CA",
                    "status": "in_transit",
                    "time": "05:45 PM",
                    "timestamp": "2025-10-01T17:45:00.000Z",
                },
                {
                    "code": "250",
                    "date": "2025-09-30",
                    "description": "Customs Clearance in Progress",
                    "location": "Chicago, IL, US",
                    "status": "in_transit",
                    "time": "01:00 PM",
                    "timestamp": "2025-09-30T13:00:00.000Z",
                },
                {
                    "code": "75",
                    "date": "2025-09-29",
                    "description": "Shipment Processed",
                    "location": "Los Angeles, CA, US",
                    "status": "in_transit",
                    "time": "09:00 AM",
                    "timestamp": "2025-09-29T09:00:00.000Z",
                },
                {
                    "code": "50",
                    "date": "2025-09-28",
                    "description": "Shipment Data Uploaded",
                    "location": "Los Angeles, CA, US",
                    "status": "pending",
                    "time": "08:12 AM",
                    "timestamp": "2025-09-28T08:12:00.000Z",
                },
            ],
            "info": {
                "carrier_tracking_link": "https://track.landmarkglobal.com/?search=LTN48392101N1"
            },
            "meta": {
                "last_mile_tracking_number": "1Z999AA10123456784",
                "last_mile_carrier": "Canada Post",
            },
            "status": "in_transit",
            "tracking_number": "LTN48392101N1",
        }
    ],
    [],
]

PARSED_OUT_FOR_DELIVERY_RESPONSE = [
    [
        {
            "carrier_id": "landmark",
            "carrier_name": "landmark",
            "delivered": False,
            "events": [
                {
                    "code": "300",
                    "date": "2025-10-02",
                    "description": "Item out for delivery",
                    "location": "Lyon, FR",
                    "status": "out_for_delivery",
                    "time": "08:15 AM",
                    "timestamp": "2025-10-02T08:15:00.000Z",
                },
                {
                    "code": "275",
                    "date": "2025-10-01",
                    "description": "Item in transit with carrier",
                    "location": "Lyon, FR",
                    "status": "in_transit",
                    "time": "09:30 AM",
                    "timestamp": "2025-10-01T09:30:00.000Z",
                },
                {
                    "code": "225",
                    "date": "2025-09-30",
                    "description": "Item grouped at Landmark facility",
                    "location": "Paris, FR",
                    "status": "in_transit",
                    "time": "03:00 PM",
                    "timestamp": "2025-09-30T15:00:00.000Z",
                },
                {
                    "code": "200",
                    "date": "2025-09-30",
                    "description": "Item scanned at postal facility",
                    "location": "Paris, FR",
                    "status": "in_transit",
                    "time": "08:45 AM",
                    "timestamp": "2025-09-30T08:45:00.000Z",
                },
                {
                    "code": "50",
                    "date": "2025-09-29",
                    "description": "Shipment Data Uploaded",
                    "location": "London, UK",
                    "status": "pending",
                    "time": "06:20 AM",
                    "timestamp": "2025-09-29T06:20:00.000Z",
                },
            ],
            "info": {
                "carrier_tracking_link": "https://track.landmarkglobal.com/?search=LTN49831232N2"
            },
            "meta": {
                "last_mile_tracking_number": "1Z999BB20234567895",
                "last_mile_carrier": "La Poste",
            },
            "status": "out_for_delivery",
            "tracking_number": "LTN49831232N2",
        }
    ],
    [],
]

PARSED_DELIVERED_RESPONSE = [
    [
        {
            "carrier_id": "landmark",
            "carrier_name": "landmark",
            "delivered": True,
            "events": [
                {
                    "code": "500",
                    "date": "2025-09-27",
                    "description": "Item successfully delivered",
                    "location": "Quebec City, QC, CA",
                    "status": "delivered",
                    "time": "02:05 PM",
                    "timestamp": "2025-09-27T14:05:00.000Z",
                },
                {
                    "code": "300",
                    "date": "2025-09-27",
                    "description": "Item out for delivery",
                    "location": "Quebec City, QC, CA",
                    "status": "out_for_delivery",
                    "time": "09:15 AM",
                    "timestamp": "2025-09-27T09:15:00.000Z",
                },
                {
                    "code": "275",
                    "date": "2025-09-27",
                    "description": "Item in transit with carrier",
                    "location": "Quebec City, QC, CA",
                    "status": "in_transit",
                    "time": "08:30 AM",
                    "timestamp": "2025-09-27T08:30:00.000Z",
                },
                {
                    "code": "125",
                    "date": "2025-09-26",
                    "description": "Customs Cleared",
                    "location": "Montreal, QC, CA",
                    "status": "in_transit",
                    "time": "11:40 AM",
                    "timestamp": "2025-09-26T11:40:00.000Z",
                },
                {
                    "code": "50",
                    "date": "2025-09-25",
                    "description": "Shipment Data Uploaded",
                    "location": "New York, NY, US",
                    "status": "pending",
                    "time": "09:10 AM",
                    "timestamp": "2025-09-25T09:10:00.000Z",
                },
            ],
            "info": {
                "carrier_tracking_link": "https://track.landmarkglobal.com/?search=LTN49100231N3"
            },
            "meta": {
                "last_mile_tracking_number": "1Z999CC30345678906",
                "last_mile_carrier": "Canada Post",
            },
            "status": "delivered",
            "tracking_number": "LTN49100231N3",
        }
    ],
    [],
]

PARSED_DELIVERY_FAILED_RESPONSE = [
    [
        {
            "carrier_id": "landmark",
            "carrier_name": "landmark",
            "delivered": False,
            "events": [
                {
                    "code": "900",
                    "date": "2025-10-03",
                    "description": "Delivery failed",
                    "location": "Rotterdam, NL",
                    "reason": "consignee_refused",
                    "status": "delivery_failed",
                    "time": "06:00 PM",
                    "timestamp": "2025-10-03T18:00:00.000Z",
                },
                {
                    "code": "400",
                    "date": "2025-10-02",
                    "description": "Attempted delivery",
                    "location": "Rotterdam, NL",
                    "reason": "consignee_not_available",
                    "status": "delivery_delayed",
                    "time": "09:30 AM",
                    "timestamp": "2025-10-02T09:30:00.000Z",
                },
                {
                    "code": "275",
                    "date": "2025-10-01",
                    "description": "Item in transit with carrier",
                    "location": "Rotterdam, NL",
                    "status": "in_transit",
                    "time": "02:00 PM",
                    "timestamp": "2025-10-01T14:00:00.000Z",
                },
                {
                    "code": "225",
                    "date": "2025-09-30",
                    "description": "Item grouped at Landmark facility",
                    "location": "Amsterdam, NL",
                    "status": "in_transit",
                    "time": "10:30 AM",
                    "timestamp": "2025-09-30T10:30:00.000Z",
                },
                {
                    "code": "50",
                    "date": "2025-09-29",
                    "description": "Shipment Data Uploaded",
                    "location": "Berlin, DE",
                    "status": "pending",
                    "time": "07:00 AM",
                    "timestamp": "2025-09-29T07:00:00.000Z",
                },
            ],
            "info": {
                "carrier_tracking_link": "https://track.landmarkglobal.com/?search=LTN49678120N4"
            },
            "meta": {
                "last_mile_carrier": "DHL",
                "last_mile_tracking_number": "1Z999DD40456789017",
            },
            "status": "delivery_failed",
            "tracking_number": "LTN49678120N4",
        }
    ],
    [],
]


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

IN_TRANSIT_TRACKING_RESPONSE_XML = """
<TrackResponse>
  <Test>true</Test>
  <Result>
    <Success>true</Success>
    <ShipmentDetails>
      <EndDeliveryCarrier>Canada Post</EndDeliveryCarrier>
    </ShipmentDetails>
    <Packages>
      <Package>
        <TrackingNumber>1Z999AA10123456784</TrackingNumber>
        <LandmarkTrackingNumber>LTN48392101N1</LandmarkTrackingNumber>
        <PackageReference>ORDER-1001</PackageReference>
        <Events>
          <Event>
            <Status>Shipment Data Uploaded</Status>
            <DateTime>09/28/2025 08:12 AM</DateTime>
            <Location>Los Angeles, CA, US</Location>
            <EventCode>50</EventCode>
          </Event>
          <Event>
            <Status>Shipment Processed</Status>
            <DateTime>09/29/2025 09:00 AM</DateTime>
            <Location>Los Angeles, CA, US</Location>
            <EventCode>75</EventCode>
          </Event>
          <Event>
            <Status>Customs Clearance in Progress</Status>
            <DateTime>09/30/2025 01:00 PM</DateTime>
            <Location>Chicago, IL, US</Location>
            <EventCode>250</EventCode>
          </Event>
          <Event>
            <Status>Item in transit with carrier</Status>
            <DateTime>10/01/2025 05:45 PM</DateTime>
            <Location>Toronto, ON, CA</Location>
            <EventCode>275</EventCode>
          </Event>
        </Events>
      </Package>
    </Packages>
  </Result>
</TrackResponse>
"""

OUT_FOR_DELIVERY_TRACKING_RESPONSE_XML = """
<TrackResponse>
  <Test>true</Test>
  <Result>
    <Success>true</Success>
    <ShipmentDetails>
      <EndDeliveryCarrier>La Poste</EndDeliveryCarrier>
    </ShipmentDetails>
    <Packages>
      <Package>
        <TrackingNumber>1Z999BB20234567895</TrackingNumber>
        <LandmarkTrackingNumber>LTN49831232N2</LandmarkTrackingNumber>
        <PackageReference>ORDER-2002</PackageReference>
        <Events>
          <Event>
            <Status>Shipment Data Uploaded</Status>
            <DateTime>2025-09-29 06:20:00</DateTime>
            <Location>London, UK</Location>
            <EventCode>50</EventCode>
          </Event>
          <Event>
            <Status>Item scanned at postal facility</Status>
            <DateTime>2025-09-30 08:45:00</DateTime>
            <Location>Paris, FR</Location>
            <EventCode>200</EventCode>
          </Event>
          <Event>
            <Status>Item grouped at Landmark facility</Status>
            <DateTime>2025-09-30 15:00:00</DateTime>
            <Location>Paris, FR</Location>
            <EventCode>225</EventCode>
          </Event>
          <Event>
            <Status>Item in transit with carrier</Status>
            <DateTime>2025-10-01 09:30:00</DateTime>
            <Location>Lyon, FR</Location>
            <EventCode>275</EventCode>
          </Event>
          <Event>
            <Status>Item out for delivery</Status>
            <DateTime>2025-10-02 08:15:00</DateTime>
            <Location>Lyon, FR</Location>
            <EventCode>300</EventCode>
          </Event>
        </Events>
      </Package>
    </Packages>
  </Result>
</TrackResponse>
"""

DELIVERED_TRACKING_RESPONSE_XML = """
<TrackResponse>
  <Test>true</Test>
  <Result>
    <Success>true</Success>
    <ShipmentDetails>
      <EndDeliveryCarrier>Canada Post</EndDeliveryCarrier>
    </ShipmentDetails>
    <Packages>
      <Package>
        <TrackingNumber>1Z999CC30345678906</TrackingNumber>
        <LandmarkTrackingNumber>LTN49100231N3</LandmarkTrackingNumber>
        <PackageReference>ORDER-3003</PackageReference>
        <Events>
          <Event>
            <Status>Shipment Data Uploaded</Status>
            <DateTime>09/25/2025 09:10 AM</DateTime>
            <Location>New York, NY, US</Location>
            <EventCode>50</EventCode>
          </Event>
          <Event>
            <Status>Customs Cleared</Status>
            <DateTime>09/26/2025 11:40 AM</DateTime>
            <Location>Montreal, QC, CA</Location>
            <EventCode>125</EventCode>
          </Event>
          <Event>
            <Status>Item in transit with carrier</Status>
            <DateTime>09/27/2025 08:30 AM</DateTime>
            <Location>Quebec City, QC, CA</Location>
            <EventCode>275</EventCode>
          </Event>
          <Event>
            <Status>Item out for delivery</Status>
            <DateTime>09/27/2025 09:15 AM</DateTime>
            <Location>Quebec City, QC, CA</Location>
            <EventCode>300</EventCode>
          </Event>
          <Event>
            <Status>Item successfully delivered</Status>
            <DateTime>09/27/2025 02:05 PM</DateTime>
            <Location>Quebec City, QC, CA</Location>
            <EventCode>500</EventCode>
          </Event>
        </Events>
      </Package>
    </Packages>
  </Result>
</TrackResponse>
"""

DELIVERY_FAILED_TRACKING_RESPONSE_XML = """
<TrackResponse>
  <Test>true</Test>
  <Result>
    <Success>true</Success>
    <ShipmentDetails>
      <EndDeliveryCarrier>DHL</EndDeliveryCarrier>
    </ShipmentDetails>
    <Packages>
      <Package>
        <TrackingNumber>1Z999DD40456789017</TrackingNumber>
        <LandmarkTrackingNumber>LTN49678120N4</LandmarkTrackingNumber>
        <PackageReference>ORDER-4004</PackageReference>
        <Events>
          <Event>
            <Status>Shipment Data Uploaded</Status>
            <DateTime>09/29/2025 07:00 AM</DateTime>
            <Location>Berlin, DE</Location>
            <EventCode>50</EventCode>
          </Event>
          <Event>
            <Status>Item grouped at Landmark facility</Status>
            <DateTime>09/30/2025 10:30 AM</DateTime>
            <Location>Amsterdam, NL</Location>
            <EventCode>225</EventCode>
          </Event>
          <Event>
            <Status>Item in transit with carrier</Status>
            <DateTime>10/01/2025 02:00 PM</DateTime>
            <Location>Rotterdam, NL</Location>
            <EventCode>275</EventCode>
          </Event>
          <Event>
            <Status>Attempted delivery</Status>
            <DateTime>10/02/2025 09:30 AM</DateTime>
            <Location>Rotterdam, NL</Location>
            <EventCode>400</EventCode>
          </Event>
          <Event>
            <Status>Delivery failed</Status>
            <DateTime>10/03/2025 06:00 PM</DateTime>
            <Location>Rotterdam, NL</Location>
            <EventCode>900</EventCode>
          </Event>
        </Events>
      </Package>
    </Packages>
  </Result>
</TrackResponse>
"""

MIDNIGHT_TIME_SORTING_RESPONSE_XML = """<?xml version="1.0"?>
<TrackResponse>
    <Result>
        <Success>true</Success>
        <ShipmentDetails>
            <EndDeliveryCarrier>BPost International</EndDeliveryCarrier>
        </ShipmentDetails>
        <Packages>
            <Package>
                <TrackingNumber>LE223553042BE</TrackingNumber>
                <LandmarkTrackingNumber>LTN408798880N1</LandmarkTrackingNumber>
                <PackageReference>ZS034809548GB</PackageReference>
                <Events>
                    <Event>
                        <Status>Shipment Data Uploaded</Status>
                        <DateTime>2025-10-27 05:48:01</DateTime>
                        <Location>North Shields</Location>
                        <EventCode>50</EventCode>
                    </Event>
                    <Event>
                        <Status>Package scanned at carrier facility</Status>
                        <DateTime>2025-10-28 08:41:59</DateTime>
                        <Location>Feltham, SRY</Location>
                        <EventCode>225</EventCode>
                    </Event>
                    <Event>
                        <Status>Processed</Status>
                        <DateTime>2025-10-28 08:42:00</DateTime>
                        <Location>Feltham, SRY</Location>
                        <EventCode>75</EventCode>
                    </Event>
                    <Event>
                        <Status>Grouped when pallet scanned to crossing (INTAKE DDP #17)</Status>
                        <DateTime>2025-10-29 09:34:00</DateTime>
                        <Location>Feltham, SRY</Location>
                        <EventCode>225</EventCode>
                    </Event>
                    <Event>
                        <Status>Crossing border and in transit to carrier hub</Status>
                        <DateTime>2025-10-29 10:15:43</DateTime>
                        <Location>Feltham, SRY</Location>
                        <EventCode>150</EventCode>
                    </Event>
                    <Event>
                        <Status>Outgoing scan at facility</Status>
                        <DateTime>2025-10-29 11:10:19</DateTime>
                        <Location>Feltham, SRY</Location>
                        <EventCode>225</EventCode>
                    </Event>
                    <Event>
                        <Status>Incoming scan at facility</Status>
                        <DateTime>2025-10-30 06:13:13</DateTime>
                        <Location>Machelen</Location>
                        <EventCode>225</EventCode>
                    </Event>
                    <Event>
                        <Status>Outgoing scan at facility</Status>
                        <DateTime>2025-10-30 08:52:51</DateTime>
                        <Location>Machelen</Location>
                        <EventCode>225</EventCode>
                    </Event>
                    <Event>
                        <Status>Received at international processing center</Status>
                        <DateTime>2025-10-30 10:34:22</DateTime>
                        <Location></Location>
                        <EventCode>155</EventCode>
                    </Event>
                    <Event>
                        <Status>Departure to country of destination</Status>
                        <DateTime>2025-10-30 13:33:00</DateTime>
                        <Location></Location>
                        <EventCode>200</EventCode>
                    </Event>
                    <Event>
                        <Status>Customs cleared</Status>
                        <DateTime>2025-10-30 13:54:02</DateTime>
                        <Location>Machelen</Location>
                        <EventCode>125</EventCode>
                    </Event>
                    <Event>
                        <Status>Arrival from abroad</Status>
                        <DateTime>2025-10-31 08:24:00</DateTime>
                        <Location></Location>
                        <EventCode>275</EventCode>
                    </Event>
                    <Event>
                        <Status>Departure to distribution network</Status>
                        <DateTime>2025-11-02 13:35:00</DateTime>
                        <Location></Location>
                        <EventCode>275</EventCode>
                    </Event>
                    <Event>
                        <Status>Arrival distribution office</Status>
                        <DateTime>2025-11-03 00:35:00</DateTime>
                        <Location></Location>
                        <EventCode>275</EventCode>
                    </Event>
                    <Event>
                        <Status>Your shipment has arrived at the postal operator of the country of
                            destination and will be delivered in the coming days.</Status>
                        <DateTime>2025-11-03 01:35:00</DateTime>
                        <Location></Location>
                        <EventCode>275</EventCode>
                    </Event>
                    <Event>
                        <Status>Item delivered</Status>
                        <DateTime>2025-11-03 07:14:00</DateTime>
                        <Location>Endingen Am Kaiserstuhl</Location>
                        <EventCode>500</EventCode>
                    </Event>
                </Events>
            </Package>
        </Packages>
    </Result>
</TrackResponse>
"""

PARSED_MIDNIGHT_TIME_SORTING_RESPONSE = [
    [
        {
            "carrier_id": "landmark",
            "carrier_name": "landmark",
            "delivered": True,
            "events": [
                {
                    "code": "500",
                    "date": "2025-11-03",
                    "description": "Item delivered",
                    "location": "Endingen Am Kaiserstuhl",
                    "status": "delivered",
                    "time": "07:14 AM",
                    "timestamp": "2025-11-03T07:14:00.000Z",
                },
                {
                    "code": "275",
                    "date": "2025-11-03",
                    "description": "Your shipment has arrived at the postal operator of the country of\n                            destination and will be delivered in the coming days.",
                    "status": "in_transit",
                    "time": "01:35 AM",
                    "timestamp": "2025-11-03T01:35:00.000Z",
                },
                {
                    "code": "275",
                    "date": "2025-11-03",
                    "description": "Arrival distribution office",
                    "status": "in_transit",
                    "time": "12:35 AM",
                    "timestamp": "2025-11-03T00:35:00.000Z",
                },
                {
                    "code": "275",
                    "date": "2025-11-02",
                    "description": "Departure to distribution network",
                    "status": "in_transit",
                    "time": "01:35 PM",
                    "timestamp": "2025-11-02T13:35:00.000Z",
                },
                {
                    "code": "275",
                    "date": "2025-10-31",
                    "description": "Arrival from abroad",
                    "status": "in_transit",
                    "time": "08:24 AM",
                    "timestamp": "2025-10-31T08:24:00.000Z",
                },
                {
                    "code": "125",
                    "date": "2025-10-30",
                    "description": "Customs cleared",
                    "location": "Machelen",
                    "status": "in_transit",
                    "time": "01:54 PM",
                    "timestamp": "2025-10-30T13:54:02.000Z",
                },
                {
                    "code": "200",
                    "date": "2025-10-30",
                    "description": "Departure to country of destination",
                    "status": "in_transit",
                    "time": "01:33 PM",
                    "timestamp": "2025-10-30T13:33:00.000Z",
                },
                {
                    "code": "155",
                    "date": "2025-10-30",
                    "description": "Received at international processing center",
                    "status": "in_transit",
                    "time": "10:34 AM",
                    "timestamp": "2025-10-30T10:34:22.000Z",
                },
                {
                    "code": "225",
                    "date": "2025-10-30",
                    "description": "Outgoing scan at facility",
                    "location": "Machelen",
                    "status": "in_transit",
                    "time": "08:52 AM",
                    "timestamp": "2025-10-30T08:52:51.000Z",
                },
                {
                    "code": "225",
                    "date": "2025-10-30",
                    "description": "Incoming scan at facility",
                    "location": "Machelen",
                    "status": "in_transit",
                    "time": "06:13 AM",
                    "timestamp": "2025-10-30T06:13:13.000Z",
                },
                {
                    "code": "225",
                    "date": "2025-10-29",
                    "description": "Outgoing scan at facility",
                    "location": "Feltham, SRY",
                    "status": "in_transit",
                    "time": "11:10 AM",
                    "timestamp": "2025-10-29T11:10:19.000Z",
                },
                {
                    "code": "150",
                    "date": "2025-10-29",
                    "description": "Crossing border and in transit to carrier hub",
                    "location": "Feltham, SRY",
                    "status": "in_transit",
                    "time": "10:15 AM",
                    "timestamp": "2025-10-29T10:15:43.000Z",
                },
                {
                    "code": "225",
                    "date": "2025-10-29",
                    "description": "Grouped when pallet scanned to crossing (INTAKE DDP #17)",
                    "location": "Feltham, SRY",
                    "status": "in_transit",
                    "time": "09:34 AM",
                    "timestamp": "2025-10-29T09:34:00.000Z",
                },
                {
                    "code": "75",
                    "date": "2025-10-28",
                    "description": "Processed",
                    "location": "Feltham, SRY",
                    "status": "in_transit",
                    "time": "08:42 AM",
                    "timestamp": "2025-10-28T08:42:00.000Z",
                },
                {
                    "code": "225",
                    "date": "2025-10-28",
                    "description": "Package scanned at carrier facility",
                    "location": "Feltham, SRY",
                    "status": "in_transit",
                    "time": "08:41 AM",
                    "timestamp": "2025-10-28T08:41:59.000Z",
                },
                {
                    "code": "50",
                    "date": "2025-10-27",
                    "description": "Shipment Data Uploaded",
                    "location": "North Shields",
                    "status": "pending",
                    "time": "05:48 AM",
                    "timestamp": "2025-10-27T05:48:01.000Z",
                },
            ],
            "info": {
                "carrier_tracking_link": "https://track.landmarkglobal.com/?search=LTN408798880N1"
            },
            "meta": {
                "last_mile_carrier": "BPost International",
                "last_mile_tracking_number": "LE223553042BE",
            },
            "status": "delivered",
            "tracking_number": "LTN408798880N1",
        }
    ],
    [],
]

TO_BE_ROUTED_TRACKING_RESPONSE_XML = """<?xml version="1.0"?>
<TrackResponse>
  <Result>
    <Success>true</Success>
    <ShipmentDetails>
      <EndDeliveryCarrier>To Be Routed</EndDeliveryCarrier>
    </ShipmentDetails>
    <Packages>
      <Package>
        <TrackingNumber>H00TCC0028567558</TrackingNumber>
        <LandmarkTrackingNumber>LTN433006705N1</LandmarkTrackingNumber>
        <PackageReference>ZS204724186GB</PackageReference>
        <Events>
          <Event>
            <Status>Shipment Data Uploaded</Status>
            <DateTime>2026-01-28 03:40:52</DateTime>
            <Location>North Shields</Location>
            <EventCode>50</EventCode>
          </Event>
        </Events>
      </Package>
    </Packages>
  </Result>
</TrackResponse>
"""

PARSED_TO_BE_ROUTED_RESPONSE = [
    [
        {
            "carrier_id": "landmark",
            "carrier_name": "landmark",
            "delivered": False,
            "events": [
                {
                    "code": "50",
                    "date": "2026-01-28",
                    "description": "Shipment Data Uploaded",
                    "location": "North Shields",
                    "status": "pending",
                    "time": "03:40 AM",
                    "timestamp": "2026-01-28T03:40:52.000Z",
                },
            ],
            "info": {
                "carrier_tracking_link": "https://track.landmarkglobal.com/?search=LTN433006705N1"
            },
            "meta": {
                "last_mile_tracking_number": "H00TCC0028567558",
            },
            "status": "pending",
            "tracking_number": "LTN433006705N1",
        }
    ],
    [],
]
