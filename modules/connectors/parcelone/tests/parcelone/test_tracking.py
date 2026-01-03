"""ParcelOne tracking tests."""

import unittest
from unittest.mock import patch
from .fixture import gateway

import karrio.sdk as karrio
import karrio.lib as lib
import karrio.core.models as models


class TestParcelOneTracking(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.TrackingRequest = models.TrackingRequest(**TrackingPayload)

    def test_create_tracking_request(self):
        request = gateway.mapper.create_tracking_request(self.TrackingRequest)

        self.assertEqual(request.serialize(), TrackingRequest)

    def test_get_tracking(self):
        with patch("karrio.mappers.parcelone.proxy.lib.request") as mock:
            mock.return_value = "<a></a>"
            karrio.Tracking.fetch(self.TrackingRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}",
            )

    def test_parse_tracking_response(self):
        with patch("karrio.mappers.parcelone.proxy.lib.request") as mock:
            mock.return_value = TrackingResponse
            parsed_response = (
                karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )
            print(parsed_response)
            self.assertListEqual(lib.to_dict(parsed_response), ParsedTrackingResponse)

    def test_parse_tracking_no_events_response(self):
        with patch("karrio.mappers.parcelone.proxy.lib.request") as mock:
            mock.return_value = TrackingNoEventsResponse
            parsed_response = (
                karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )
            print(parsed_response)
            self.assertListEqual(
                lib.to_dict(parsed_response), ParsedTrackingNoEventsResponse
            )


if __name__ == "__main__":
    unittest.main()


TrackingPayload = {
    "tracking_numbers": ["123456789012", "987654321098"],
}

ParsedTrackingResponse = [
    [
        {
            "carrier_id": "parcelone",
            "carrier_name": "parcelone",
            "delivered": True,
            "events": [
                {
                    "code": "DELIVERED",
                    "date": "2024-01-15",
                    "description": "Package delivered",
                    "location": "Munich, Germany",
                    "status": "delivered",
                    "time": "14:30 PM",
                    "timestamp": "2024-01-15T14:30:00.000Z",
                },
                {
                    "code": "OUT_FOR_DELIVERY",
                    "date": "2024-01-15",
                    "description": "Out for delivery",
                    "location": "Munich, Germany",
                    "status": "out_for_delivery",
                    "time": "08:00 AM",
                    "timestamp": "2024-01-15T08:00:00.000Z",
                },
                {
                    "code": "ARRIVED",
                    "date": "2024-01-14",
                    "description": "Arrived at destination facility",
                    "location": "Munich Hub",
                    "status": "in_transit",
                    "time": "22:00 PM",
                    "timestamp": "2024-01-14T22:00:00.000Z",
                },
                {
                    "code": "IN_TRANSIT",
                    "date": "2024-01-14",
                    "description": "Shipment in transit",
                    "location": "Berlin Hub",
                    "status": "in_transit",
                    "time": "10:00 AM",
                    "timestamp": "2024-01-14T10:00:00.000Z",
                },
                {
                    "code": "REGISTERED",
                    "date": "2024-01-13",
                    "description": "Shipment picked up",
                    "location": "Berlin",
                    "status": "pending",
                    "time": "16:00 PM",
                    "timestamp": "2024-01-13T16:00:00.000Z",
                },
            ],
            "info": {
                "carrier_tracking_link": "https://tracking.parcel.one/?trackingNumber=123456789012"
            },
            "status": "delivered",
            "tracking_number": "123456789012",
        }
    ],
    [],
]

ParsedTrackingNoEventsResponse = [[], []]


TrackingRequest = """<?xml version="1.0" encoding="utf-8"?>
<soapenv:Envelope
    xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
    xmlns:tns="http://tempuri.org/"
    xmlns:wcf="http://schemas.datacontract.org/2004/07/ShippingWCF"
    xmlns:arr="http://schemas.microsoft.com/2003/10/Serialization/Arrays">
    <soapenv:Header>
        <wsse:Security xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd">
            <wsse:UsernameToken>
                <wsse:Username>test_user</wsse:Username>
                <wsse:Password Type="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0#PasswordText">test_password</wsse:Password>
            </wsse:UsernameToken>
        </wsse:Security>
    </soapenv:Header>
    <soapenv:Body>
        <tns:getTrackings>
            <tns:ShippingData>
                <wcf:identifyShipment xmlns:wcf="http://schemas.datacontract.org/2004/07/ShippingWCF">
    <ShipmentRefField>TrackingID</ShipmentRefField>
    <ShipmentRefValue>123456789012</ShipmentRefValue>
</wcf:identifyShipment>
<wcf:identifyShipment xmlns:wcf="http://schemas.datacontract.org/2004/07/ShippingWCF">
    <ShipmentRefField>TrackingID</ShipmentRefField>
    <ShipmentRefValue>987654321098</ShipmentRefValue>
</wcf:identifyShipment>

            </tns:ShippingData>
        </tns:getTrackings>
    </soapenv:Body>
</soapenv:Envelope>"""


TrackingResponse = """<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
    xmlns:wcf="http://schemas.datacontract.org/2004/07/ShippingWCF">
    <soap:Body>
        <getTrackingsResponse xmlns="http://tempuri.org/">
            <getTrackingsResult>
                <wcf:ShipmentTrackingResult>
                    <wcf:ActionResult>
                        <wcf:Success>1</wcf:Success>
                        <wcf:TrackingID>123456789012</wcf:TrackingID>
                    </wcf:ActionResult>
                    <wcf:Trackings>
                        <wcf:TrackingResult>
                            <wcf:TrackingDateTime>2024-01-15T14:30:00</wcf:TrackingDateTime>
                            <wcf:TrackingLocation>Munich, Germany</wcf:TrackingLocation>
                            <wcf:TrackingStatus>Package delivered</wcf:TrackingStatus>
                            <wcf:TrackingStatusCode>DELIVERED</wcf:TrackingStatusCode>
                        </wcf:TrackingResult>
                        <wcf:TrackingResult>
                            <wcf:TrackingDateTime>2024-01-15T08:00:00</wcf:TrackingDateTime>
                            <wcf:TrackingLocation>Munich, Germany</wcf:TrackingLocation>
                            <wcf:TrackingStatus>Out for delivery</wcf:TrackingStatus>
                            <wcf:TrackingStatusCode>OUT_FOR_DELIVERY</wcf:TrackingStatusCode>
                        </wcf:TrackingResult>
                        <wcf:TrackingResult>
                            <wcf:TrackingDateTime>2024-01-14T22:00:00</wcf:TrackingDateTime>
                            <wcf:TrackingLocation>Munich Hub</wcf:TrackingLocation>
                            <wcf:TrackingStatus>Arrived at destination facility</wcf:TrackingStatus>
                            <wcf:TrackingStatusCode>ARRIVED</wcf:TrackingStatusCode>
                        </wcf:TrackingResult>
                        <wcf:TrackingResult>
                            <wcf:TrackingDateTime>2024-01-14T10:00:00</wcf:TrackingDateTime>
                            <wcf:TrackingLocation>Berlin Hub</wcf:TrackingLocation>
                            <wcf:TrackingStatus>Shipment in transit</wcf:TrackingStatus>
                            <wcf:TrackingStatusCode>IN_TRANSIT</wcf:TrackingStatusCode>
                        </wcf:TrackingResult>
                        <wcf:TrackingResult>
                            <wcf:TrackingDateTime>2024-01-13T16:00:00</wcf:TrackingDateTime>
                            <wcf:TrackingLocation>Berlin</wcf:TrackingLocation>
                            <wcf:TrackingStatus>Shipment picked up</wcf:TrackingStatus>
                            <wcf:TrackingStatusCode>REGISTERED</wcf:TrackingStatusCode>
                        </wcf:TrackingResult>
                    </wcf:Trackings>
                </wcf:ShipmentTrackingResult>
            </getTrackingsResult>
        </getTrackingsResponse>
    </soap:Body>
</soap:Envelope>"""


TrackingNoEventsResponse = """<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
    xmlns:wcf="http://schemas.datacontract.org/2004/07/ShippingWCF">
    <soap:Body>
        <getTrackingsResponse xmlns="http://tempuri.org/">
            <getTrackingsResult>
                <wcf:ShipmentTrackingResult>
                    <wcf:ActionResult>
                        <wcf:Success>1</wcf:Success>
                        <wcf:TrackingID>999999999999</wcf:TrackingID>
                    </wcf:ActionResult>
                    <wcf:Trackings/>
                </wcf:ShipmentTrackingResult>
            </getTrackingsResult>
        </getTrackingsResponse>
    </soap:Body>
</soap:Envelope>"""
