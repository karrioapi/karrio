import unittest
from unittest.mock import patch
from karrio.core.utils import DP
from karrio.core.models import ShipmentRequest, ShipmentCancelRequest
from karrio import Shipment
from .fixture import gateway


class TestEasyPostShipment(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.ShipmentRequest = ShipmentRequest(**SHIPMENT_PAYLOAD)
        self.ShipmentCancelRequest = ShipmentCancelRequest(**CANCEL_SHIPMENT_PAYLOAD)

    def test_create_shipment_request(self):
        request = gateway.mapper.create_shipment_request(self.ShipmentRequest)

        self.assertEqual(request.serialize(), ShipmentRequestJSON)

    def test_create_cancel_shipment_request(self):
        request = gateway.mapper.create_cancel_shipment_request(
            self.ShipmentCancelRequest
        )
        self.assertEqual(request.serialize(), CancelShipmentRequestJSON)

    def test_create_shipment(self):
        with patch("karrio.mappers.easypost.proxy.http") as mocks:
            mocks.side_effect = [ShipmentResponseJSON, BuyShipmentResponseJSON]
            Shipment.create(self.ShipmentRequest).from_(gateway)

            create_call, buy_call = mocks.call_args_list

            self.assertEqual(
                create_call[1]["url"],
                f"{gateway.settings.server_url}/shipments",
            )
            self.assertEqual(
                buy_call[1]["url"],
                f"{gateway.settings.server_url}/shipments/shp_.../buy",
            )

    def test_create_cancel_shipment(self):
        with patch("karrio.mappers.easypost.proxy.http") as mock:
            mock.return_value = "{}"
            Shipment.cancel(self.ShipmentCancelRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/shipments/{self.ShipmentCancelRequest.shipment_identifier}/refund",
            )

    def test_parse_shipment_response(self):
        with patch("karrio.mappers.easypost.proxy.http") as mocks:
            mocks.side_effect = [ShipmentResponseJSON, BuyShipmentResponseJSON]
            response = Shipment.create(self.ShipmentRequest).from_(gateway)

            with patch("karrio.providers.easypost.utils.request") as mock:
                mock.return_value = ""
                parsed_response = response.parse()

                self.assertListEqual(
                    DP.to_dict(parsed_response), ParsedShipmentResponse
                )

    def test_parse_cancel_shipment_response(self):
        with patch("karrio.mappers.easypost.proxy.http") as mock:
            mock.return_value = CancelShipmentResponseJSON
            parsed_response = (
                Shipment.cancel(self.ShipmentCancelRequest).from_(gateway).parse()
            )

            self.assertListEqual(
                DP.to_dict(parsed_response), ParsedCancelShipmentResponse
            )


if __name__ == "__main__":
    unittest.main()


SHIPMENT_PAYLOAD = {
    "service": "easypost_ups_next_day_air",
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
    "options": {"insurance": 249.99},
}

CANCEL_SHIPMENT_PAYLOAD = {
    "shipment_identifier": "shipment_id",
    "options": {"shipment_identifiers": ["shipment_id"]},
}

ParsedShipmentResponse = [
    {
        "carrier_id": "easypost",
        "carrier_name": "easypost",
        "docs": {},
        "label_type": "PNG",
        "meta": {
            "label_url": "https://amazonaws.com/.../a1b2c3.png",
            "rate_provider": "UPS",
            "service_name": "NextDayAir",
        },
        "shipment_identifier": "shp_...",
        "tracking_number": "1ZE6A4850190733810",
    },
    [],
]

ParsedCancelShipmentResponse = [
    {
        "carrier_id": "easypost",
        "carrier_name": "easypost",
        "operation": "cancel shipment",
        "success": True,
    },
    [],
]


ShipmentRequestJSON = {
    "insurance": 249.99,
    "service": "NextDayAir",
    "data": {
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
            "options": {
                "label_format": "PDF",
                "payment": {"postal_code": "10451", "type": "SENDER"},
            },
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
    },
}

CancelShipmentRequestJSON = "shipment_id"

ShipmentResponseJSON = """{
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
      "carrier": "UPS",
      "created_at": "2013-11-08T15:50:02Z",
      "currency": "USD",
      "id": "rate_...",
      "object": "Rate",
      "rate": "30.44",
      "service": "NextDayAir",
      "shipment_id": "shp_...",
      "updated_at": "2013-11-08T15:50:02Z"
    }, {
      "carrier": "UPS",
      "created_at": "2013-11-08T15:50:02Z",
      "currency": "USD",
      "id": "rate_...",
      "object": "Rate",
      "rate": "60.28",
      "service": "NextDayAirEarlyAM",
      "shipment_id": "shp_...",
      "updated_at": "2013-11-08T15:50:02Z"
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

BuyShipmentResponseJSON = """{
  "batch_message": null,
  "batch_status": null,
  "created_at": "2013-11-08T15:50:00Z",
  "customs_info": null,
  "from_address": {
    "city": "San Francisco",
    "company": null,
    "country": "US",
    "created_at": "2013-11-08T15:49:59Z",
    "email": null,
    "id": "adr_...",
    "mode": "test",
    "name": "EasyPost",
    "object": "Address",
    "phone": "415-379-7678",
    "state": "CA",
    "street1": "417 Montgomery Street",
    "street2": "5th Floor",
    "updated_at": "2013-11-08T15:49:59Z",
    "zip": "94104"
  },
  "id": "shp_...",
  "insurance": 249.99,
  "is_return": false,
  "mode": "test",
  "object": "Shipment",
  "parcel": {
    "created_at": "2013-11-08T15:49:59Z",
    "height": null,
    "id": "prcl_...",
    "length": null,
    "mode": "test",
    "object": "Parcel",
    "predefined_package": "UPSLetter",
    "updated_at": "2013-11-08T15:49:59Z",
    "weight": 3.0,
    "width": null
  },
  "postage_label": {
    "created_at": "2013-11-08T20:57:32Z",
    "id": "pl_...",
    "integrated_form": "none",
    "label_date": "2013-11-08T20:57:32Z",
    "label_epl2_url": null,
    "label_file_type": "image/png",
    "label_pdf_url": "https://amazonaws.com/.../a1b2c3.pdf",
    "label_resolution": 200,
    "label_size": "4x7",
    "label_type": "default",
    "label_url": "https://amazonaws.com/.../a1b2c3.png",
    "label_zpl_url": null,
    "object": "PostageLabel",
    "updated_at": "2013-11-08T21:11:14Z"
  },
  "rates": [
    {
      "carrier": "UPS",
      "created_at": "2013-11-08T15:50:02Z",
      "currency": "USD",
      "id": "rate_...",
      "object": "Rate",
      "rate": "30.44",
      "service": "NextDayAir",
      "shipment_id": "shp_...",
      "updated_at": "2013-11-08T15:50:02Z"
    }, {
      "carrier": "UPS",
      "created_at": "2013-11-08T15:50:02Z",
      "currency": "USD",
      "id": "rate_...",
      "object": "Rate",
      "rate": "60.28",
      "service": "NextDayAirEarlyAM",
      "shipment_id": "shp_...",
      "updated_at": "2013-11-08T15:50:02Z"
    }
  ],
  "reference": null,
  "refund_status": null,
  "scan_form": null,
  "selected_rate": {
    "carrier": "UPS",
    "created_at": "2013-11-08T15:50:02Z",
    "currency": "USD",
    "id": "rate_...",
    "object": "Rate",
    "rate": "30.44",
    "service": "NextDayAir",
    "shipment_id": "shp_...",
    "updated_at": "2013-11-08T15:50:02Z"
  },
  "status": "unknown",
  "to_address": {
    "city": "Redondo Beach",
    "company": null,
    "country": "US",
    "created_at": "2013-11-08T15:49:58Z",
    "email": "dr_steve_brule@gmail.com",
    "id": "adr_...",
    "mode": "test",
    "name": "Dr. Steve Brule",
    "object": "Address",
    "phone": null,
    "state": "CA",
    "street1": "179 N Harbor Dr",
    "street2": null,
    "updated_at": "2013-11-08T15:49:58Z",
    "zip": "90277"
  },
  "tracker": {
    "created_at": "2013-11-08T20:57:32Z",
    "id": "trk_...",
    "mode": "test",
    "object": "Tracker",
    "shipment_id": "shp_...",
    "status": "unknown",
    "tracking_code": "1ZE6A4850190733810",
    "tracking_details": [ ],
    "updated_at": "2013-11-08T20:58:26Z",
    "public_url": "https://track.easypost.com/djE7..."
  },
  "tracking_code": "1ZE6A4850190733810",
  "updated_at": "2013-11-08T20:58:26Z"
}
"""

CancelShipmentResponseJSON = """{
  "batch_message": null,
  "batch_status": null,
  "created_at": "2013-11-08T15:50:00Z",
  "customs_info": null,
  "from_address": {
    "city": "San Francisco",
    "company": null,
    "country": "US",
    "created_at": "2013-11-08T15:49:59Z",
    "email": null,
    "id": "adr_...",
    "mode": "test",
    "name": "EasyPost",
    "object": "Address",
    "phone": "415-379-7678",
    "state": "CA",
    "street1": "417 Montgomery Street",
    "street2": "5th Floor",
    "updated_at": "2013-11-08T15:49:59Z",
    "zip": "94104"
  },
  "id": "shp_...",
  "insurance": null,
  "is_return": false,
  "mode": "test",
  "object": "Shipment",
  "parcel": {
    "created_at": "2013-11-08T15:49:59Z",
    "height": null,
    "id": "prcl_...",
    "length": null,
    "mode": "test",
    "object": "Parcel",
    "predefined_package": "UPSLetter",
    "updated_at": "2013-11-08T15:49:59Z",
    "weight": 3.0,
    "width": null
  },
  "postage_label": {
    "created_at": "2013-11-08T20:57:32Z",
    "id": "pl_...",
    "integrated_form": "none",
    "label_date": "2013-11-08T20:57:32Z",
    "label_epl2_url": null,
    "label_file_type": "image/png",
    "label_pdf_url": "https://amazonaws.com/.../a1b2c3.pdf",
    "label_resolution": 200,
    "label_size": "4x7",
    "label_type": "default",
    "label_url": "https://amazonaws.com/.../a1b2c3.png",
    "label_zpl_url": "https://amazonaws.com/.../a1b2c3.zpl",
    "object": "PostageLabel",
    "updated_at": "2013-11-08T21:11:14Z"
  },
  "rates": [
    {
      "carrier": "UPS",
      "created_at": "2013-11-08T15:50:02Z",
      "currency": "USD",
      "id": "rate_...",
      "object": "Rate",
      "rate": "30.44",
      "service": "NextDayAir",
      "shipment_id": "shp_...",
      "updated_at": "2013-11-08T15:50:02Z"
    }, {
      "carrier": "UPS",
      "created_at": "2013-11-08T15:50:02Z",
      "currency": "USD",
      "id": "rate_...",
      "object": "Rate",
      "rate": "60.28",
      "service": "NextDayAirEarlyAM",
      "shipment_id": "shp_...",
      "updated_at": "2013-11-08T15:50:02Z"
    }
  ],
  "reference": null,
  "refund_status": "submitted",
  "scan_form": null,
  "selected_rate": {
    "carrier": "UPS",
    "created_at": "2013-11-08T15:50:02Z",
    "currency": "USD",
    "id": "rate_...",
    "object": "Rate",
    "rate": "30.44",
    "service": "NextDayAir",
    "shipment_id": "shp_...",
    "updated_at": "2013-11-08T15:50:02Z"
  },
  "status": "unknown",
  "to_address": {
    "city": "Redondo Beach",
    "company": null,
    "country": "US",
    "created_at": "2013-11-08T15:49:58Z",
    "email": "dr_steve_brule@gmail.com",
    "id": "adr_...",
    "mode": "test",
    "name": "Dr. Steve Brule",
    "object": "Address",
    "phone": null,
    "state": "CA",
    "street1": "179 N Harbor Dr",
    "street2": null,
    "updated_at": "2013-11-08T15:49:58Z",
    "zip": "90277"
  },
  "tracker": {
    "created_at": "2013-11-08T20:57:32Z",
    "id": "trk_...",
    "mode": "test",
    "object": "Tracker",
    "shipment_id": "shp_...",
    "status": "unknown",
    "tracking_code": "1ZE6A4850190733810",
    "tracking_details": [ ],
    "updated_at": "2013-11-08T20:58:26Z",
    "public_url": "https://track.easypost.com/djE7..."
  },
  "tracking_code": "1ZE6A4850190733810",
  "updated_at": "2013-11-08T20:58:26Z"
}
"""
