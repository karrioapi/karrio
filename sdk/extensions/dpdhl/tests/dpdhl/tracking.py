import unittest
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

        self.assertEqual(request.serialize(), TrackingRequest)

    def test_get_tracking(self):
        with patch("karrio.mappers.dpdhl.proxy.lib.request") as mock:
            mock.return_value = "<a></a>"
            karrio.Tracking.fetch(self.TrackingRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}",
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
    "tracking_numbers": ["89108749065090"],
}

ParsedTrackingResponse = [[], []]

ParsedErrorResponse = [{}, []]


TrackingRequest = """<data appname="Benutzerkennung" password="Passwort" request="d-get-piece-detail" language-code="iso-sprachcode" piece-code="Sendungsnummer" from-date="2012-03-01" to-date="2012-04-20">
</data>
"""

TrackingResponse = """<?xml version="1.0" encoding="UTF-8" ?>
<data name="pieceshipmentlist" request-id="379d9788-5a8e-49dd-9f7e-d30e17746c2a" code="0">
    <data name="pieceshipment" error-status="0" piece-id="3b048653-aaa9-485b-b0dd-d16e068230e9" shipment-code="" piece-identifier="26633445" identifier-type="1" piece-code="266334453" event-location="" event-country="DE" status-liste="" status-timestamp="16.03.2012 15:29" status="Die Sendung wurde erfolgreich zugestellt." short-status="Zustellung erfolgreich" recipient-name="TestMustermann" recipient-street="Am Musterhaus 5" recipient-city="23221 Testmannsdorf" pan-recipient-name="TestMustermann" pan-recipient-street="Am Musterhaus 5" pan-recipient-city="23221 Testmannsdorf" pan-recipient-address="Am Musterhaus 5 23221 Testmannsdorf" shipper-name="VersandhausHeileWelt" shipper-street="Testerstraße 111" shipper-city="53113 Meindorf" shipper-address="Testerstraße 111 53113 Meindorf" product-code="00" product-key="" product-name="DHLPAKET" delivery-event-flag="1" recipient-id="2" recipient-id-text="Ehegatte" upu="" shipment-length="0.0" shipment-width="0.0" shipment-height="0.0" shipment-weight="0.2" international-flag="0" division="DPEED" ice="DLVRD" ric="ACCPT" standard-event-code="ZU" dest-country="DE" origin-country="DE" searched-piece-code="26633445" searched-ref-nr="" piece-customer-reference="034234" shipment-customer-reference="111234" leitcode="" />
    <data name="pieceeventlist" piece-identifier="2343265" _build-time="2012-10-06 18:18:10.000607" piece-id="3b048653-aaa9-485b-b0dd-d16e068230e9" leitcode="34634543453">
        <data name="pieceevent" event-timestamp="14.03.2012 00:00" event-status="Die Sendung wurde im Start-Paketzentrum bearbeitet." event-text="Die Sendung wurde im Start-Paketzentrum bearbeitet." ice="LDTMV" ric="MVMTV" event-location="Saulheim" event-country="Deutschland" standard-event-code="AA"/>
        <data name="pieceevent" event-timestamp="16.03.2012 15:29" event-status="Die Sendung wurde erfolgreich zugestellt." event-text=" Die Sendung wurde erfolgreich zugestellt." ice="DLVRD" ric="ACCPT" event-location="Bonn" event-country="Deutschland" standard-event-code="ZU"/>
    </data>
</data>
"""

ErrorResponse = """<a></a>
"""
