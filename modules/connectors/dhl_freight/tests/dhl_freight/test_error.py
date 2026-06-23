"""Booking validation + RFC-7807 problem+json + OAuth error parsing."""

import unittest

import karrio.providers.dhl_freight.error as error

from .fixture import gateway

SETTINGS = gateway.settings


class TestErrorParsing(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_booking_validation_errors(self):
        """Booking endpoint returns {status, validationErrors:[{errorCode,message,field}]}.

        Verified live against the sandbox (errorCode 22001/22014).
        """
        msgs = error.parse_error_response(VALIDATION_ERROR, SETTINGS)
        self.assertEqual(len(msgs), 1)
        self.assertEqual(msgs[0].code, "22014")
        self.assertEqual(msgs[0].message, "Accountnumber 62085855350106 not valid for party Consignor")
        self.assertEqual(msgs[0].details["field"], "Parties[0].Id")

    def test_multiple_booking_validation_errors(self):
        msgs = error.parse_error_response(MULTI_VALIDATION_ERROR, SETTINGS)
        self.assertEqual([m.code for m in msgs], ["22001", "22002"])

    def test_problem_json_400(self):
        msgs = error.parse_error_response(PROBLEM_JSON_400, SETTINGS)
        self.assertEqual(len(msgs), 1)
        self.assertEqual(msgs[0].code, "400")
        self.assertEqual(msgs[0].message, "Missing required field: totalWeight")
        self.assertEqual(msgs[0].carrier_name, "dhl_freight")

    def test_problem_json_includes_invalid_params_in_details(self):
        msgs = error.parse_error_response(PROBLEM_JSON_400, SETTINGS)
        self.assertEqual(
            msgs[0].details["invalidParams"],
            [{"name": "totalWeight", "reason": "must be > 0"}],
        )

    def test_oauth_error_response(self):
        """Token endpoint returns ``error`` + ``error_description`` (not problem+json)."""
        msgs = error.parse_error_response(OAUTH_ERROR, SETTINGS)
        self.assertEqual(len(msgs), 1)
        self.assertEqual(msgs[0].code, "invalid_client")
        self.assertIn("Client", msgs[0].message)

    def test_rate_limit_429(self):
        msgs = error.parse_error_response(RATE_LIMIT_429, SETTINGS)
        self.assertEqual(msgs[0].code, "429")

    def test_success_response_yields_no_messages(self):
        msgs = error.parse_error_response(SUCCESS_RESPONSE, SETTINGS)
        self.assertEqual(msgs, [])

    def test_list_of_responses(self):
        """parse_error_response accepts a list, flattens errors across them."""
        msgs = error.parse_error_response([SUCCESS_RESPONSE, PROBLEM_JSON_400], SETTINGS)
        self.assertEqual(len(msgs), 1)
        self.assertEqual(msgs[0].code, "400")


if __name__ == "__main__":
    unittest.main()


# Fixtures ---------------------------------------------------------------------

VALIDATION_ERROR = {
    "status": "Error",
    "validationErrors": [
        {
            "errorCode": 22014,
            "message": "Accountnumber 62085855350106 not valid for party Consignor",
            "field": "Parties[0].Id",
        }
    ],
}

MULTI_VALIDATION_ERROR = {
    "status": "Error",
    "validationErrors": [
        {"errorCode": 22001, "message": "Missing Id in Consignor", "field": "Parties[0].Id"},
        {"errorCode": 22002, "message": "Missing name in Consignee", "field": "Parties[1].Name"},
    ],
}

PROBLEM_JSON_400 = {
    "type": "https://api.dhl.com/freight/problem",
    "title": "Bad Request",
    "statusCode": 400,
    "detail": "Missing required field: totalWeight",
    "instance": "/freight/shipping/orders/v1/sendtransportinstruction",
    "invalidParams": [{"name": "totalWeight", "reason": "must be > 0"}],
}

OAUTH_ERROR = {
    "error": "invalid_client",
    "error_description": "Client authentication failed",
}

RATE_LIMIT_429 = {
    "title": "Too Many Requests",
    "statusCode": 429,
    "detail": "Daily rate limit exceeded",
}

SUCCESS_RESPONSE = {
    "shipmentId": "DHLF-2026-000001",
    "status": "BOOKED",
}
