import unittest
from unittest.mock import patch
from gds_helpers import to_xml, jsonify, export
from openship.domain.entities import Tracking
from tests.ups.fixture import proxy
from tests.utils import strip


class TestUPSTracking(unittest.TestCase):

    @patch("openship.mappers.ups.ups_proxy.http", return_value='<a></a>')
    def test_create_tracking_request(self, http_mock):
        payload = Tracking.create(tracking_numbers=["8346088391"])
        tracking_req_xml_obj = proxy.mapper.create_tracking_request(payload)

        proxy.get_trackings(tracking_req_xml_obj)

        xmlStr = http_mock.call_args[1]['data'].decode("utf-8")
        self.assertEqual(strip(xmlStr), strip(TrackingRequestXml))

    def test_tracking_auth_error_parsing(self):
        parsed_response = proxy.mapper.parse_error_response(to_xml(AuthError))
        self.assertEqual(jsonify(parsed_response), jsonify(ParsedAuthError))

    def test_parse_tracking_response(self):
        parsed_response = proxy.mapper.parse_tracking_response(
            to_xml(TrackingResponseXml))
        self.assertEqual(jsonify(parsed_response),
                         jsonify(ParsedTrackingResponse))

    def test_tracking_single_not_found_parsing(self):
        parsed_response = proxy.mapper.parse_tracking_response(
            to_xml(TrackingSingleNotFound))
        self.assertEqual(jsonify(parsed_response),
                         jsonify(ParsedTrackingSingNotFound))

    def test_tracking_unknown_response_parsing(self):
        parsed_response = proxy.mapper.parse_tracking_response(
            to_xml(UnknownTrackResponse))
        self.assertEqual(jsonify(parsed_response),
                         jsonify(ParsedUnknownTrackResponse))


if __name__ == '__main__':
    unittest.main()


ParsedAuthError = [
]

ParsedTrackingSingNotFound = [
]

ParsedTrackingResponse = [
]

ParsedUnknownTrackResponse = [
]



AuthError = '''
'''

TrackingSingleNotFound = """
"""

TrackingRequestXml = '''
'''

TrackingResponseXml = '''
'''

UnknownTrackResponse = """
"""
