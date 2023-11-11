import unittest
from unittest.mock import patch, ANY
from .fixture import gateway

import karrio
import karrio.lib as lib
import karrio.core.models as models


class TestBelgianPostTracking(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.TrackingRequest = models.TrackingRequest(**TrackingPayload)

    def test_create_tracking_request(self):
        request = gateway.mapper.create_tracking_request(self.TrackingRequest)

        self.assertEqual(request.serialize(), TrackingRequest)

    def test_get_tracking(self):
        with patch("karrio.mappers.bpost.proxy.lib.request") as mock:
            mock.return_value = "<a></a>"
            karrio.Tracking.fetch(self.TrackingRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                "https://api.parcel.bpost.cloud/services/trackedmail/item/323212345659900040669030/trackingInfo",
            )

    def test_parse_tracking_response(self):
        with patch("karrio.mappers.bpost.proxy.lib.request") as mock:
            mock.return_value = TrackingResponse
            parsed_response = (
                karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedTrackingResponse)

    def test_parse_error_response(self):
        with patch("karrio.mappers.bpost.proxy.lib.request") as mock:
            mock.return_value = ErrorResponse
            parsed_response = (
                karrio.Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedErrorResponse)


if __name__ == "__main__":
    unittest.main()


TrackingPayload = {
    "tracking_numbers": ["323212345659900040669030"],
}

ParsedTrackingResponse = [
    [
        {
            "carrier_id": "bpost",
            "carrier_name": "bpost",
            "delivered": False,
            "estimated_delivery": "2012-11-23",
            "events": [
                {
                    "code": "T00",
                    "date": "2012-11-22",
                    "description": "Sorted - sorted_out",
                    "time": "23:19",
                },
                {
                    "code": "L00",
                    "date": "2012-11-23",
                    "description": "BoundToRound - out_for_distribution",
                    "time": "07:11",
                },
                {
                    "code": "U01",
                    "date": "2012-11-23",
                    "description": "DistributedNormally - regular",
                    "time": "09:31",
                },
            ],
            "info": {
                "carrier_tracking_link": "https://track.bpost.cloud/btr/web/#/search?itemCode=323212345659900040669030&lang=EN",
                "customer_name": "BARCODE TEAM BPACK",
                "expected_delivery": "2012-11-23",
                "package_weight": 0.38,
                "package_weight_unit": "KG",
                "shipment_destination_country": "BE",
                "shipment_destination_postal_code": "1000",
                "shipment_origin_country": "BE",
                "shipment_origin_postal_code": "1000",
            },
            "meta": {
                "pickup_point": "66 RUE WASHINGTON / WASHINGTONSTRAAT 1050 IXELLES / ELSENE",
                "reference": "TEST AUTOMATIC SORTER",
                "trackingId": "gqwxvsyt",
            },
            "status": "in_transit",
            "tracking_number": "323212345659900040669030",
        }
    ],
    [],
]

ParsedErrorResponse = [
    [],
    [
        {
            "carrier_id": "bpost",
            "carrier_name": "bpost",
            "code": "500",
            "details": {"tracking_number": "323212345659900040669030"},
            "message": "An unexpected error occurred while executing the request!\n"
            "        Please try again in a few moments.\n"
            "        If the problem persist, please contact our support and "
            "provide the following token\n"
            "        information f35c0f13-538f-41ae-99aa-932bc3141109",
        }
    ],
]


TrackingRequest = ["323212345659900040669030"]

TrackingResponse = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<itemTracking xmlns="http://schema.post.be/tracking/v1/"
    xmlns:ns2="http://schema.post.be/announcement/common/v1/">
    <itemCode>323212345659900040669030</itemCode>
    <sender>
        <ns2:name>TEST COMPANY NAME</ns2:name>
        <ns2:address>
            <ns2:streetName>WETSTRAAT</ns2:streetName>
            <ns2:houseNumber>1</ns2:houseNumber>
            <ns2:postalCode>1000</ns2:postalCode>
            <ns2:city>BRUSSELS</ns2:city>
            <ns2:countryCode>BE</ns2:countryCode>
        </ns2:address>
    </sender>
    <addressee>
        <ns2:name>BARCODE TEAM BPACK</ns2:name>
        <ns2:address>
            <ns2:streetName>MUNTCENTRUM</ns2:streetName>
            <ns2:postalCode>1000</ns2:postalCode>
            <ns2:city>BRUSSELS</ns2:city>
            <ns2:countryCode>BE</ns2:countryCode>
        </ns2:address>
        <ns2:contactDetail>
            <ns2:emailAddress>BARCODESPARCELS@POST.BE</ns2:emailAddress>
        </ns2:contactDetail>
    </addressee>
    <cityOrCountryOfdeparture>BRUSSELS</cityOrCountryOfdeparture>
    <cityOrCountryOfDestination>BRUSSELS</cityOrCountryOfDestination>
    <nameOfDestination>BARCODE TEAM BPACK</nameOfDestination>
    <deliveryTime>2012-11-23T09:31:07+01:00</deliveryTime>
    <customerReference>TEST AUTOMATIC SORTER</customerReference>
    <itemDetail>
        <weightInGrams>380</weightInGrams>
        <type>01</type>
        <options />
    </itemDetail>
    <stateInfo>
        <time>2012-11-22T23:19:29+01:00</time>
        <stateCode>T00</stateCode>
        <stateDescription>Sorted - sorted_out</stateDescription>
    </stateInfo>
    <stateInfo>
        <time>2012-11-23T07:11:18.923+01:00</time>
        <stateCode>L00</stateCode>
        <stateDescription>BoundToRound - out_for_distribution</stateDescription>
    </stateInfo>
    <stateInfo>
        <time>2012-11-23T09:31:07.427+01:00</time>
        <stateCode>U01</stateCode>
        <stateDescription>DistributedNormally - regular</stateDescription>
    </stateInfo>
    <trackingId>gqwxvsyt</trackingId>
    <pickupPoint>
        <id>805140</id>
        <name>LIBRAIRIE WILSON</name>
        <streetName>RUE WASHINGTON / WASHINGTONSTRAAT</streetName>
        <houseNumber>66</houseNumber>
        <postalCode>1050</postalCode>
        <city>IXELLES / ELSENE</city>
    </pickupPoint>
</itemTracking>
"""

ErrorResponse = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<systemException xmlns="http://schema.post.be/api/shm/common/v2/"
    xmlns:ns2="http://schema.post.be/common/exception/v1/">
    <ns2:message>An unexpected error occurred while executing the request!
        Please try again in a few moments.
        If the problem persist, please contact our support and provide the following token
        information f35c0f13-538f-41ae-99aa-932bc3141109</ns2:message>
    <ns2:timestamp>2011-04-29+02:00</ns2:timestamp>
</systemException>
"""
