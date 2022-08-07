import unittest
import urllib.parse
from unittest.mock import patch
from tests.dpdhl.fixture import gateway

import karrio
import karrio.lib as lib
import karrio.core.models as models


class TestDPDHLTracking(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.TrackingRequest = models.TrackingRequest(**TrackingPayload)

    def test_create_tracking_request(self):
        request = gateway.mapper.create_tracking_request(self.TrackingRequest)

        self.assertEqual(request.serialize(), [TrackingRequest])

    def test_get_tracking(self):
        with patch("karrio.mappers.dpdhl.proxy.lib.request") as mock:
            mock.return_value = "<a></a>"
            karrio.Tracking.fetch(self.TrackingRequest).from_(gateway)
            query = urllib.parse.urlencode(dict(xml=TrackingRequest))

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/rest/sendungsverfolgung?{query}",
            )

    def test_parse_tracking_response(self):
        with patch("karrio.mappers.dpdhl.proxy.lib.request") as mock:
            mock.return_value = TrackingResponse
            parsed_response = (
                karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedTrackingResponse)

    def test_parse_error_response(self):
        with patch("karrio.mappers.dpdhl.proxy.lib.request") as mock:
            mock.return_value = ErrorResponse
            parsed_response = (
                karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedErrorResponse)


if __name__ == "__main__":
    unittest.main()


TrackingPayload = {
    "tracking_numbers": ["00340434161094042557"],
}

ParsedTrackingResponse = [
    [
        {
            "carrier_id": "dpdhl",
            "carrier_name": "dpdhl",
            "delivered": True,
            "events": [
                {
                    "code": "SHRCU",
                    "date": "2016-03-17",
                    "description": "The shipment has been posted by the sender at the PACKSTATION",
                    "location": "Bremen, Germany",
                    "time": "2016-03-17",
                },
                {
                    "code": "LDTMV",
                    "date": "2016-03-17",
                    "description": "The shipment has been taken from the PACKSTATION for onward transportation",
                    "location": "Bremen, Germany",
                    "time": "2016-03-17",
                },
                {
                    "code": "PCKDU",
                    "date": "2016-03-17",
                    "description": "The shipment has been picked up",
                    "location": "Germany",
                    "time": "2016-03-17",
                },
                {
                    "code": "LDTMV",
                    "date": "2016-03-17",
                    "description": "The shipment has been processed in the parcel center of origin",
                    "location": "Bremen, Germany",
                    "time": "2016-03-17",
                },
                {
                    "code": "ULFMV",
                    "date": "2016-03-18",
                    "description": "The shipment has been processed in the destination parcel center",
                    "location": "Neuwied, Germany",
                    "time": "2016-03-18",
                },
                {
                    "code": "SRTED",
                    "date": "2016-03-18",
                    "description": "The shipment has been loaded onto the delivery vehicle",
                    "time": "2016-03-18",
                },
                {
                    "code": "DLVRD",
                    "date": "2016-03-18",
                    "description": "The shipment has been successfully delivered",
                    "location": "Bonn, Germany",
                    "time": "2016-03-18",
                },
            ],
            "tracking_number": 340434161094042557,
        }
    ],
    [],
]

ParsedErrorResponse = [
    [],
    [
        {
            "carrier_id": "dpdhl",
            "carrier_name": "dpdhl",
            "code": "5",
            "message": "Log-in failed",
        }
    ],
]


TrackingRequest = """<data appname="2222222222_01" password="pass" request="d-get-piece-detail" language-code="en" piece-code="00340434161094042557"/>
"""

TrackingResponse = """<?xml version="1.0" encoding="UTF-8"?>
<data name="piece-shipment-list" code="0" request-id="89786828-031c-4855-a149-90f7921106a0">
    <data name="piece-shipment" error-status="0" piece-id="fc23a3ec-cca6-483e-8fd5-c927ab0e2b1b" shipment-code="" piece-identifier="340434161094042557" identifier-type="2" piece-code="00340434161094042557" event-location="" event-country="DE" status-liste="0" status-timestamp="18.03.2016 10:02" status="The shipment has been successfully delivered" short-status="Delivery successful" recipient-name="Kraemer" recipient-street="Heinrich-Brüning-Str. 7" recipient-city="53113 Bonn" pan-recipient-name="Deutsche Post DHL" pan-recipient-street="Heinrich-Brüning-Str. 7" pan-recipient-city="53113 Bonn" pan-recipient-address="Heinrich-Brüning-Str. 7 53113 Bonn" pan-recipient-postalcode="53113" shipper-name="No sender data has been transferred to DHL." shipper-street="" shipper-city="" shipper-address="" product-code="00" product-key="" product-name="DHL PAKET (parcel)" delivery-event-flag="1" recipient-id="5" recipient-id-text="different person present" upu="" shipment-length="0.0" shipment-width="0.0" shipment-height="0.0" shipment-weight="0.0" international-flag="0" division="DPEED" ice="DLVRD" ric="OTHER" standard-event-code="ZU" dest-country="DE" origin-country="DE" searched-piece-code="00340434161094042557" searched-ref-no="" piece-customer-reference="" shipment-customer-reference="" leitcode="" routing-code-ean="" matchcode="" domestic-id="" airway-bill-number="" ruecksendung="false" pslz-nr="5066847896" order-preferred-delivery-day="false">
        <data name="piece-event-list" piece-identifier="340434161094042557" _build-time="2017-01-14 19:56:41.000512" piece-id="fc23a3ec-cca6-483e-8fd5-c927ab0e2b1b" leitcode="5311304400700" routing-code-ean="" ruecksendung="false" pslz-nr="5066847896" order-preferred-delivery-day="false">
            <data name="piece-event" event-timestamp="17.03.2016 11:21" event-status="The shipment has been posted by the sender at the PACKSTATION" event-text="The shipment has been posted by the sender at the PACKSTATION" event-short-status="Posting at PACKSTATION" ice="SHRCU" ric="PCKST" event-location="Bremen" event-country="Germany" standard-event-code="ES" ruecksendung="false" />
            <data name="piece-event" event-timestamp="17.03.2016 13:23" event-status="The shipment has been taken from the PACKSTATION for onward transportation" event-text="The shipment has been taken from the PACKSTATION for onward transportation" event-short-status="Transportation to parcel center of origin" ice="LDTMV" ric="MVMTV" event-location="Bremen" event-country="Germany" standard-event-code="AA" ruecksendung="false" />
            <data name="piece-event" event-timestamp="17.03.2016 16:18" event-status="The shipment has been picked up" event-text="The shipment has been picked up" event-short-status="Pick-up successful" ice="PCKDU" ric="PUBCR" event-location="" event-country="Germany" standard-event-code="AE" ruecksendung="false" />
            <data name="piece-event" event-timestamp="17.03.2016 18:12" event-status="The shipment has been processed in the parcel center of origin" event-text="The shipment has been processed in the parcel center of origin" event-short-status="Parcel center of origin" ice="LDTMV" ric="MVMTV" event-location="Bremen" event-country="Germany" standard-event-code="AA" ruecksendung="false" />
            <data name="piece-event" event-timestamp="18.03.2016 03:24" event-status="The shipment has been processed in the destination parcel center" event-text="The shipment has been processed in the destination parcel center" event-short-status="Destination parcel center" ice="ULFMV" ric="UNLDD" event-location="Neuwied" event-country="Germany" standard-event-code="EE" ruecksendung="false" />
            <data name="piece-event" event-timestamp="18.03.2016 09:02" event-status="The shipment has been loaded onto the delivery vehicle" event-text="The shipment has been loaded onto the delivery vehicle" event-short-status="In delivery" ice="SRTED" ric="NRQRD" event-location="" event-country="" standard-event-code="PO" ruecksendung="false" />
            <data name="piece-event" event-timestamp="18.03.2016 10:02" event-status="The shipment has been successfully delivered" event-text="The shipment has been successfully delivered" event-short-status="Delivery successful" ice="DLVRD" ric="OTHER" event-location="Bonn" event-country="Germany" standard-event-code="ZU" ruecksendung="false" />
        </data>
    </data>
</data>
"""

ErrorResponse = """<?xml version="1.0" encoding="UTF-8"?>
<data name="piece-shipment-list" code="5" request-id="3f214081-0712-442c-9e83-163ddd9d9fb8" error="Log-in failed">
    <data name="piece-shipment" searched-piece-code="00340434161094032954" piece-code="00340434161094032954" international-flag="0" piece-status="5" piece-status-desc="Log-in failed"/>
</data>
"""
