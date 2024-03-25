import unittest
from unittest.mock import patch, ANY
from karrio.core.utils import DP
from karrio.core.models import RateRequest
from karrio import Rating
from .fixture import gateway


class TestEasyPostRating(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.RateRequest = RateRequest(**PAYLOAD)

    def test_create_rate_request(self):
        request = gateway.mapper.create_rate_request(self.RateRequest)

        self.assertEqual(request.serialize(), RateRequestJSON)

    def test_get_rate(self):
        with patch("karrio.mappers.easypost.proxy.lib.request") as mock:
            mock.return_value = "{}"
            Rating.fetch(self.RateRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/shipments",
            )

    def test_parse_rate_response(self):
        with patch("karrio.mappers.easypost.proxy.lib.request") as mock:
            mock.return_value = RateResponseJSON
            parsed_response = Rating.fetch(self.RateRequest).from_(gateway).parse()

            self.assertListEqual(DP.to_dict(parsed_response), ParsedRateResponse)

    def test_parse_error_response(self):
        with patch("karrio.mappers.easypost.proxy.lib.request") as mock:
            mock.return_value = ErrorResponseJSON
            parsed_response = Rating.fetch(self.RateRequest).from_(gateway).parse()

            self.assertListEqual(DP.to_dict(parsed_response), ParsedErrorResponse)


if __name__ == "__main__":
    unittest.main()


PAYLOAD = {
    "reference": "order #1111",
    "recipient": {
        "company_name": "EasyPost",
        "address_line1": "417 Montgomery Street",
        "address_line2": "5th Floor",
        "city": "San Francisco",
        "state_code": "CA",
        "postal_code": "94104",
        "phone_number": "415-528-7555",
    },
    "shipper": {
        "person_name": "George Costanza",
        "company_name": "Vandelay Industries",
        "address_line1": "1 E 161st St.",
        "city": "Bronx",
        "state_code": "NY",
        "postal_code": "10451",
    },
    "parcels": [{"length": 9.0, "width": 6.0, "height": 2.0, "weight": 10.0}],
}

ParsedRateResponse = [
    [
        {
            "carrier_id": "easypost",
            "carrier_name": "easypost",
            "meta": {
                "rate_provider": "usps",
                "service_name": "usps_first_class_package_international_service",
            },
            "service": "easypost_usps_first_class_package_international_service",
            "total_charge": 9.5,
            "transit_days": 4,
        },
        {
            "carrier_id": "easypost",
            "carrier_name": "easypost",
            "meta": {
                "rate_provider": "usps",
                "service_name": "usps_priority_mail_international",
            },
            "service": "easypost_usps_priority_mail_international",
            "total_charge": 27.4,
            "transit_days": 2,
        },
        {
            "carrier_id": "easypost",
            "carrier_name": "easypost",
            "meta": {
                "rate_provider": "usps",
                "service_name": "usps_express_mail_international",
            },
            "service": "easypost_usps_express_mail_international",
            "total_charge": 35.48,
            "transit_days": 1,
        },
    ],
    [],
]

ParsedErrorResponse = [
    [],
    [
        {
            "carrier_id": "easypost",
            "carrier_name": "easypost",
            "code": "SHIPMENT.INVALID_PARAMS",
            "details": {
                "errors": [
                    {"to_address": "Required and missing."},
                    {"from_address": "Required and missing."},
                ]
            },
            "message": "Unable to create shipment, one or more parameters were invalid.",
        }
    ],
]


RateRequestJSON = {
    "shipment": {
        "from_address": {
            "city": "Bronx",
            "company": "Vandelay Industries",
            "name": "George Costanza",
            "residential": False,
            "state": "NY",
            "street1": "1 E 161st St.",
            "zip": "10451",
        },
        "options": {},
        "parcel": {"height": 2.0, "length": 9.0, "weight": 160.0, "width": 6.0},
        "reference": "order #1111",
        "to_address": {
            "city": "San Francisco",
            "company": "EasyPost",
            "phone": "415-528-7555",
            "residential": False,
            "state": "CA",
            "street1": "417 Montgomery Street",
            "street2": "5th Floor",
            "zip": "94104",
        },
    }
}

RateResponseJSON = """{
  "id": "shp_...",
  "object": "Shipment",
  "mode": "test",
  "to_address": {
    "id": "adr_...",
    "object": "Address",
    "name": "Dr. Steve Brule",
    "company": null,
    "street1": "179 N Harbor Dr",
    "street2": null,
    "city": "Redondo Beach",
    "state": "CA",
    "zip": "90277",
    "country": "US",
    "phone": "4153334444",
    "mode": "test",
    "carrier_facility": null,
    "residential": null,
    "email": "dr_steve_brule@gmail.com",
    "created_at": "2013-04-22T05:39:56Z",
    "updated_at": "2013-04-22T05:39:56Z"
  },
  "from_address": {
    "id": "adr_...",
    "object": "Address",
    "name": "EasyPost",
    "company": null,
    "street1": "417 Montgomery Street",
    "street2": "5th Floor",
    "city": "San Francisco",
    "state": "CA",
    "zip": "94104",
    "country": "US",
    "phone": "4153334444",
    "email": "support@easypost.com",
    "mode": "test",
    "carrier_facility": null,
    "residential": null,
    "created_at": "2013-04-22T05:39:57Z",
    "updated_at": "2013-04-22T05:39:57Z"
  },
  "parcel": {
    "id": "prcl_...",
    "object": "Parcel",
    "length": 20.2,
    "width": 10.9,
    "height": 5.0,
    "predefined_package": null,
    "weight": 140.8,
    "created_at": "2013-04-22T05:39:57Z",
    "updated_at": "2013-04-22T05:39:57Z"
  },
  "customs_info": {
    "id": "cstinfo_...",
    "object": "CustomsInfo",
    "created_at": "2013-04-22T05:39:57Z",
    "updated_at": "2013-04-22T05:39:57Z",
    "contents_explanation": null,
    "contents_type": "merchandise",
    "customs_certify": false,
    "customs_signer": null,
    "eel_pfc": null,
    "non_delivery_option": "return",
    "restriction_comments": null,
    "restriction_type": "none",
    "customs_items": [
      {
        "id": "cstitem_...",
        "object": "CustomsItem",
        "description": "Many, many EasyPost stickers.",
        "hs_tariff_number": "123456",
        "origin_country": "US",
        "quantity": 1,
        "value": 879,
        "weight": 140,
        "created_at": "2013-04-22T05:39:57Z",
        "updated_at": "2013-04-22T05:39:57Z"
      }
    ]
  },
  "rates": [
    {
      "id": "rate_...",
      "object": "Rate",
      "carrier_account_id": "ca_...",
      "service": "FirstClassPackageInternationalService",
      "rate": "9.50",
      "carrier": "USPS",
      "shipment_id": "shp_...",
      "delivery_days": 4,
      "delivery_date": "2013-04-26T05:40:57Z",
      "delivery_date_guaranteed": false,
      "created_at": "2013-04-22T05:40:57Z",
      "updated_at": "2013-04-22T05:40:57Z"
    },
    {
      "id": "rate_...",
      "object": "Rate",
      "carrier_account_id": "ca_...",
      "service": "PriorityMailInternational",
      "rate": "27.40",
      "carrier": "USPS",
      "shipment_id": "shp_...",
      "delivery_days": 2,
      "delivery_date": "2013-04-24T05:40:57Z",
      "delivery_date_guaranteed": false,
      "created_at": "2013-04-22T05:40:57Z",
      "updated_at": "2013-04-22T05:40:57Z"
    },
    {
      "id": "rate_...",
      "object": "Rate",
      "carrier_account_id": "ca_...",
      "service": "ExpressMailInternational",
      "rate": "35.48",
      "carrier": "USPS",
      "shipment_id": "shp_...",
      "delivery_days": 1,
      "delivery_date": "2013-04-23T05:40:57Z",
      "delivery_date_guaranteed": true,
      "created_at": "2013-04-22T05:40:57Z",
      "updated_at": "2013-04-22T05:40:57Z"
    }
  ],
  "scan_form": null,
  "selected_rate": null,
  "postage_label": null,
  "tracking_code": null,
  "refund_status": null,
  "insurance": null,
  "created_at": "2013-04-22T05:40:57Z",
  "updated_at": "2013-04-22T05:40:57Z"
}
"""

ErrorResponseJSON = """{
	"error": {
		"code": "SHIPMENT.INVALID_PARAMS",
		"message": "Unable to create shipment, one or more parameters were invalid.",
		"errors": [
			{
				"to_address": "Required and missing."
			},
			{
				"from_address": "Required and missing."
			}
		]
	}
}
"""
