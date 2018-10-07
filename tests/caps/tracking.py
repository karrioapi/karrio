import unittest
from unittest.mock import patch
from gds_helpers import to_xml, jsonify, export
from purplship.domain.entities import Tracking
from tests.caps.fixture import proxy
from tests.utils import strip


class TestCanadaPostTracking(unittest.TestCase):
    def setUp(self):
        self.tracking_numbers = ["1Z12345E6205277936"]

    def test_create_tracking_request(self):
        payload = Tracking.create(tracking_numbers=self.tracking_numbers)

        tracking_pins = proxy.mapper.create_tracking_request(payload)

        self.assertEqual(tracking_pins, self.tracking_numbers)

    @patch("purplship.mappers.caps.caps_proxy.http", return_value='<a></a>')
    def test_get_trackings(self, http_mock):
        proxy.get_trackings(self.tracking_numbers)

        reqUrl = http_mock.call_args[1]['url']
        self.assertEqual(reqUrl, TrackingRequestURL)

    def test_tracking_auth_error_parsing(self):
        parsed_response = proxy.mapper.parse_error_response(to_xml(AuthError))
        self.assertEqual(jsonify(parsed_response), jsonify(ParsedAuthError))

    def test_parse_tracking_response(self):
        parsed_response = proxy.mapper.parse_tracking_response(
            to_xml(TrackingResponseXml))
        self.assertEqual(jsonify(parsed_response),
                         jsonify(ParsedTrackingResponse))

    def test_tracking_unknown_response_parsing(self):
        parsed_response = proxy.mapper.parse_tracking_response(
            to_xml(UnknownTrackingNumberResponse))
        self.assertEqual(jsonify(parsed_response),
                         jsonify(ParsedUnknownTrackingNumberResponse))


if __name__ == '__main__':
    unittest.main()


ParsedAuthError = [
  {
    'carrier': 'CanadaPost', 
    'code': 'E002', 
    'message': 'AAA Authentication Failure'
  }
]

ParsedTrackingResponse = [
  [
    {
      'carrier': 'CanadaPost', 
      'events': [
        {
          'code': 'INDUCTION', 
          'date': '20110404:133457', 
          'description': 'Order information received by Canada Post', 
          'location': '', 
          'signatory': '', 
          'time': None
        }
      ], 
      'shipment_date': '2011-04-04', 
      'tracking_number': '7023210039414604'
    }
  ], 
  []
]

ParsedUnknownTrackingNumberResponse = [
  [], 
  [
    {
      'carrier': 'CanadaPost', 
      'code': '004', 
      'message': 'No Pin History'
    }
  ]
]


AuthError = """<wrapper>
    <messages xmlns="http://www.canadapost.ca/ws/messages">
        <message>
            <code>E002</code>
            <description>AAA Authentication Failure</description>
        </message>
    </messages>
</wrapper>
"""

TrackingRequestURL = """https://ct.soa-gw.canadapost.ca/vis/track/pin/1Z12345E6205277936/summary"""

TrackingResponseXml = """<wrapper>
    <tracking-summary>
        <pin-summary>
            <pin>7023210039414604</pin>
            <origin-postal-id>K1G</origin-postal-id>
            <destination-postal-id>K0J</destination-postal-id>
            <destination-province>ON</destination-province>
            <service-name>Expedited Parcels</service-name>
            <mailed-on-date>2011-04-04</mailed-on-date>
            <expected-delivery-date>2011-04-05</expected-delivery-date>
            <actual-delivery-date />
            <delivery-option-completed-ind>2</delivery-option-completed-ind>
            <event-date-time>20110404:133457</event-date-time>
            <event-description>Order information received by Canada Post</event-description>
            <attempted-date />
            <customer-ref-1>APRIL1REF1A</customer-ref-1>
            <customer-ref-2>APRIL1REF1C</customer-ref-2>
            <return-pin />
            <event-type>INDUCTION</event-type>
            <event-location />
            <signatory-name />
        </pin-summary>
    </tracking-summary>
</wrapper>
"""

UnknownTrackingNumberResponse = """<wrapper>
    <messages xmlns="http://www.canadapost.ca/ws/track">
        <message>
            <code>004</code>
            <description>No Pin History</description>
        </message>
    </messages>
</wrapper>
"""
