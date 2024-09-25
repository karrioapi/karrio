import unittest
from unittest.mock import patch, ANY
from .fixture import gateway
from tests import logger

import karrio
import karrio.lib as lib
import karrio.core.models as models


class TestTNTConnectItalyTracking(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.TrackingRequest = models.TrackingRequest(**TrackingPayload)

    def test_create_tracking_request(self):
        request = gateway.mapper.create_tracking_request(self.TrackingRequest)

        self.assertEqual(request.serialize(), TrackingRequest)

    def test_get_tracking(self):
        with patch("karrio.mappers.tnt_it.proxy.lib.request") as mock:
            mock.return_value = "<a></a>"
            karrio.Tracking.fetch(self.TrackingRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}",
            )

    def test_parse_tracking_response(self):
        with patch("karrio.mappers.tnt_it.proxy.lib.request") as mock:
            mock.return_value = TrackingResponse
            parsed_response = (
                karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedTrackingResponse)

    def test_parse_error_response(self):
        with patch("karrio.mappers.tnt_it.proxy.lib.request") as mock:
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

ParsedTrackingResponse = []

ParsedErrorResponse = []


TrackingRequest = """<Document xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
  <Application>MYTRA</Application>
  <Version>3.0</Version>
  <Login>
    <Customer>XXXXXX</Customer>
    <User>EXPRESSLABEL</User>
    <Password>XXXXXXXX</Password>
    <LangID>IT</LangID>
  </Login>
  <SearchCriteria>
    <ConNo>Lettera di vettura</ConNo>
	<RTLSearch>N</RTLSearch>
    <AccountNo>Codice Cliente</AccountNo>
    <StartDate>01-01-0001</StartDate>
    <EndDate>31-12-9999</EndDate>
  </SearchCriteria>
  <SearchParameters>
    <SearchType>Detail</SearchType>
    <SearchOption>ConsignmentTracking</SearchOption>
    <SearchKeyValue />
    <SearchMethod />
  </SearchParameters>
  <ExtraDetails>ConsignmentDetail</ExtraDetails>
</Document>
"""

TrackingResponse = """<a></a>
"""

ErrorResponse = """<a></a>
"""
