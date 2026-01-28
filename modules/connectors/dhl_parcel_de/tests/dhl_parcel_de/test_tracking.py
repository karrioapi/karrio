import unittest
from unittest.mock import patch
from karrio.core.utils import DP
from karrio.sdk import Tracking
from karrio.core.models import TrackingRequest
from .fixture import gateway


class TestCarrierTracking(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.TrackingRequest = TrackingRequest(tracking_numbers=TRACKING_PAYLOAD)

    def test_create_tracking_request(self):
        request = gateway.mapper.create_tracking_request(self.TrackingRequest)
        serialized = request.serialize()

        # Request should be a list of XML strings
        self.assertEqual(len(serialized), 1)
        # Check that the request contains expected XML elements
        self.assertIn('<?xml version="1.0" encoding="UTF-8" standalone="no"?>', serialized[0])
        self.assertIn('appname="zt12345"', serialized[0])
        self.assertIn('password="geheim"', serialized[0])
        self.assertIn('request="d-get-piece-detail"', serialized[0])
        self.assertIn('language-code="en"', serialized[0])
        self.assertIn('piece-code="00340434161094015902"', serialized[0])

    def test_get_tracking(self):
        with patch("karrio.mappers.dhl_parcel_de.proxy.lib.request") as mock:
            mock.return_value = TrackingResponseXML
            Tracking.fetch(self.TrackingRequest).from_(gateway)

            # Check URL contains the tracking server and xml parameter
            call_url = mock.call_args[1]["url"]
            self.assertIn(gateway.settings.tracking_server_url, call_url)
            self.assertIn("xml=", call_url)

            # Check HTTP Basic Auth header is present
            headers = mock.call_args[1]["headers"]
            self.assertIn("Authorization", headers)
            self.assertTrue(headers["Authorization"].startswith("Basic "))

    def test_parse_tracking_response(self):
        with patch("karrio.mappers.dhl_parcel_de.proxy.lib.request") as mock:
            mock.return_value = TrackingResponseXML
            parsed_response = (
                Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )
            print(parsed_response)
            self.assertListEqual(DP.to_dict(parsed_response), ParsedTrackingResponse)

    def test_parse_tracking_error_response(self):
        with patch("karrio.mappers.dhl_parcel_de.proxy.lib.request") as mock:
            mock.return_value = TrackingErrorResponseXML
            parsed_response = (
                Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )
            print(parsed_response)
            self.assertListEqual(
                DP.to_dict(parsed_response), ParsedTrackingErrorResponse
            )


if __name__ == "__main__":
    unittest.main()

TRACKING_PAYLOAD = ["00340434161094015902"]

ParsedTrackingResponse = [
    [
        {
            "carrier_id": "dhl_parcel_de",
            "carrier_name": "dhl_parcel_de",
            "delivered": True,
            "events": [
                {
                    "code": "ZU",
                    "date": "2016-03-18",
                    "description": "The shipment has been successfully delivered",
                    "location": "Bonn, Germany",
                    "status": "delivered",
                    "time": "10:02 AM",
                    "timestamp": "2016-03-18T10:02:00.000Z",
                },
                {
                    "code": "PO",
                    "date": "2016-03-18",
                    "description": "The shipment has been loaded onto the delivery vehicle",
                    "status": "in_transit",
                    "time": "09:02 AM",
                    "timestamp": "2016-03-18T09:02:00.000Z",
                },
                {
                    "code": "EE",
                    "date": "2016-03-18",
                    "description": "The shipment has been processed in the destination parcel center",
                    "location": "Neuwied, Germany",
                    "status": "in_transit",
                    "time": "03:32 AM",
                    "timestamp": "2016-03-18T03:32:00.000Z",
                },
                {
                    "code": "AA",
                    "date": "2016-03-17",
                    "description": "The shipment has been processed in the parcel center of origin",
                    "location": "Bremen, Germany",
                    "status": "in_transit",
                    "time": "15:51 PM",
                    "timestamp": "2016-03-17T15:51:00.000Z",
                },
                {
                    "code": "AE",
                    "date": "2016-03-17",
                    "description": "The shipment has been picked up",
                    "location": "Germany",
                    "status": "in_transit",
                    "time": "13:55 PM",
                    "timestamp": "2016-03-17T13:55:00.000Z",
                },
                {
                    "code": "AA",
                    "date": "2016-03-17",
                    "description": "The shipment has been taken from the PACKSTATION for onward transportation",
                    "location": "Bremen, Germany",
                    "status": "in_transit",
                    "time": "13:54 PM",
                    "timestamp": "2016-03-17T13:54:00.000Z",
                },
                {
                    "code": "ES",
                    "date": "2016-03-17",
                    "description": "The shipment has been posted by the sender at the PACKSTATION",
                    "location": "Bremen, Germany",
                    "status": "in_transit",
                    "time": "11:44 AM",
                    "timestamp": "2016-03-17T11:44:00.000Z",
                },
            ],
            "info": {
                "carrier_tracking_link": "https://www.dhl.com/de-en/home/tracking/tracking-parcel.html?submit=1&tracking-id=00340434161094015902",
                "customer_name": "Kraemer",
                "package_weight": 0.0,
                "package_weight_unit": "KG",
                "shipment_destination_country": "DE",
                "shipment_destination_postal_code": "53113",
                "shipment_origin_country": "DE",
                "shipment_service": "DHL PAKET (parcel)",
                "signed_by": "different person present",
            },
            "meta": {
                "piece_id": "a5aed21b-d9f4-4396-a322-f6f5f00f8039",
                "product_code": "00",
            },
            "status": "delivered",
            "tracking_number": "00340434161094015902",
        }
    ],
    [],
]

ParsedTrackingErrorResponse = [
    [],
    [
        {
            "carrier_id": "dhl_parcel_de",
            "carrier_name": "dhl_parcel_de",
            "code": "100",
            "details": {
                "request_id": "test-request-id-12345",
                "response_name": "piece-shipment-list",
            },
            "message": "No data found",
        }
    ],
]


# XML Response samples (based on actual DHL Parcel DE Tracking API responses)

TrackingResponseXML = """<?xml version="1.0" encoding="UTF-8"?>
<data name="piece-shipment-list" code="0" request-id="test-request-12345">
  <data name="piece-shipment"
    error-status="0"
    piece-id="a5aed21b-d9f4-4396-a322-f6f5f00f8039"
    shipment-code=""
    piece-identifier="340434161094015902"
    identifier-type="2"
    piece-code="00340434161094015902"
    event-location=""
    event-country="DE"
    status-liste="0"
    status-timestamp="18.03.2016 10:02"
    status="The shipment has been successfully delivered"
    short-status="Delivery successful"
    recipient-name="Kraemer"
    recipient-street="Heinrich-Brüning-Str. 7"
    recipient-city="53113 Bonn"
    pan-recipient-name="Deutsche Post DHL"
    pan-recipient-street="Heinrich-Brüning-Str. 7"
    pan-recipient-city="53113 Bonn"
    pan-recipient-address="Heinrich-Brüning-Str. 7 53113 Bonn"
    pan-recipient-postalcode="53113"
    shipper-name="No sender data has been transferred to DHL."
    shipper-street=""
    shipper-city=""
    shipper-address=""
    product-code="00"
    product-key=""
    product-name="DHL PAKET (parcel)"
    delivery-event-flag="1"
    recipient-id="5"
    recipient-id-text="different person present"
    upu=""
    shipment-length="0.0"
    shipment-width="0.0"
    shipment-height="0.0"
    shipment-weight="0.0"
    international-flag="0"
    division="DPEED"
    ice="DLVRD"
    ric="OTHER"
    standard-event-code="ZU"
    dest-country="DE"
    origin-country="DE"
    searched-piece-code="00340434161094015902"
    searched-ref-no=""
    piece-customer-reference=""
    shipment-customer-reference=""
    leitcode=""
    routing-code-ean=""
    matchcode=""
    domestic-id=""
    airway-bill-number=""
    ruecksendung="false"
    pslz-nr="5066935271"
    order-preferred-delivery-day="false"
  >
    <data name="piece-event-list"
      piece-identifier="340434161094015902"
      piece-id="a5aed21b-d9f4-4396-a322-f6f5f00f8039"
      leitcode="5311304400700"
      routing-code-ean=""
      ruecksendung="false"
      pslz-nr="5066935271"
      order-preferred-delivery-day="false"
    >
      <data name="piece-event"
        event-timestamp="17.03.2016 11:44"
        event-status="The shipment has been posted by the sender at the PACKSTATION"
        event-text="The shipment has been posted by the sender at the PACKSTATION"
        event-short-status="Posting at PACKSTATION"
        ice="SHRCU"
        ric="PCKST"
        event-location="Bremen"
        event-country="Germany"
        standard-event-code="ES"
        ruecksendung="false"
      />
      <data name="piece-event"
        event-timestamp="17.03.2016 13:54"
        event-status="The shipment has been taken from the PACKSTATION for onward transportation"
        event-text="The shipment has been taken from the PACKSTATION for onward transportation"
        event-short-status="Transportation to parcel center of origin"
        ice="LDTMV"
        ric="MVMTV"
        event-location="Bremen"
        event-country="Germany"
        standard-event-code="AA"
        ruecksendung="false"
      />
      <data name="piece-event"
        event-timestamp="17.03.2016 13:55"
        event-status="The shipment has been picked up"
        event-text="The shipment has been picked up"
        event-short-status="Pick-up successful"
        ice="PCKDU"
        ric="PUBCR"
        event-location=""
        event-country="Germany"
        standard-event-code="AE"
        ruecksendung="false"
      />
      <data name="piece-event"
        event-timestamp="17.03.2016 15:51"
        event-status="The shipment has been processed in the parcel center of origin"
        event-text="The shipment has been processed in the parcel center of origin"
        event-short-status="Parcel center of origin"
        ice="LDTMV"
        ric="MVMTV"
        event-location="Bremen"
        event-country="Germany"
        standard-event-code="AA"
        ruecksendung="false"
      />
      <data name="piece-event"
        event-timestamp="18.03.2016 03:32"
        event-status="The shipment has been processed in the destination parcel center"
        event-text="The shipment has been processed in the destination parcel center"
        event-short-status="Destination parcel center"
        ice="ULFMV"
        ric="UNLDD"
        event-location="Neuwied"
        event-country="Germany"
        standard-event-code="EE"
        ruecksendung="false"
      />
      <data name="piece-event"
        event-timestamp="18.03.2016 09:02"
        event-status="The shipment has been loaded onto the delivery vehicle"
        event-text="The shipment has been loaded onto the delivery vehicle"
        event-short-status="In delivery"
        ice="SRTED"
        ric="NRQRD"
        event-location=""
        event-country=""
        standard-event-code="PO"
        ruecksendung="false"
      />
      <data name="piece-event"
        event-timestamp="18.03.2016 10:02"
        event-status="The shipment has been successfully delivered"
        event-text="The shipment has been successfully delivered"
        event-short-status="Delivery successful"
        ice="DLVRD"
        ric="OTHER"
        event-location="Bonn"
        event-country="Germany"
        standard-event-code="ZU"
        ruecksendung="false"
      />
    </data>
  </data>
</data>
"""

TrackingErrorResponseXML = """<?xml version="1.0" encoding="UTF-8"?>
<data name="piece-shipment-list" code="100" error="No data found" request-id="test-request-id-12345"/>
"""
