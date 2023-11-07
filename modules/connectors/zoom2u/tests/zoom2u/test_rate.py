import unittest
from unittest.mock import patch, ANY
from .fixture import gateway

import karrio
import karrio.lib as lib
import karrio.core.models as models


class TestZoom2uRating(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.RateRequest = models.RateRequest(**RatePayload)

    def test_create_rate_request(self):
        request = gateway.mapper.create_rate_request(self.RateRequest)

        self.assertEqual(request.serialize(), RateRequest)

    def test_get_rate(self):
        with patch("karrio.mappers.zoom2u.proxy.lib.request") as mock:
            mock.return_value = "{}"
            karrio.Rating.fetch(self.RateRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/api/v1/delivery/quote",
            )

    def test_parse_rate_response(self):
        with patch("karrio.mappers.zoom2u.proxy.lib.request") as mock:
            mock.return_value = RateResponse
            parsed_response = (
                karrio.Rating.fetch(self.RateRequest).from_(gateway).parse()
            )

            self.assertListEqual(lib.to_dict(parsed_response), ParsedRateResponse)


if __name__ == "__main__":
    unittest.main()


RatePayload = {
    "shipper": {
        "person_name": "John Smith",
        "email": "test@test.com",
        "phone_number": "0000 0000",
        "street_number": "123",
        "address_line1": "Main St",
        "city": "North Sydney",
        "state_code": "NSW",
        "postal_code": "2000",
        "country_code": "AU",
    },
    "recipient": {
        "person_name": "Jane Smith",
        "email": "test@test.com",
        "phone_number": "0000 0000",
        "street_number": "123",
        "address_line1": "Main St",
        "city": "North Sydney",
        "state_code": "NSW",
        "postal_code": "2000",
        "country_code": "AU",
    },
    "parcels": [
        {
            "packaging_type": "small_box",
            "description": "1 box with some cakes",
        }
    ],
    "services": ["zoom2u_VIP"],
    "options": {
        "purchase_order_number": "ABCD1234",
        "ready_datetime": "2020-12-24 10:20:00",
        "vehicle_type": "zoom2u_car",
    },
}

ParsedRateResponse = [
    [
        {
            "carrier_id": "zoom2u",
            "carrier_name": "zoom2u",
            "currency": "AUD",
            "estimated_delivery": "2020-12-25",
            "meta": {
                "earliestDropEta": "2020-12-24T11:20:00Z",
                "earliestPickupEta": "2020-12-24T11:20:00Z",
                "service_name": "Same day",
            },
            "service": "zoom2u_same_day",
            "total_charge": 68.0,
            "transit_days": 1,
        },
        {
            "carrier_id": "zoom2u",
            "carrier_name": "zoom2u",
            "currency": "AUD",
            "estimated_delivery": "2020-12-25",
            "meta": {"service_name": "Same day"},
            "service": "zoom2u_same_day",
            "total_charge": 68.0,
            "transit_days": 1,
        },
        {
            "carrier_id": "zoom2u",
            "carrier_name": "zoom2u",
            "currency": "AUD",
            "estimated_delivery": "2020-12-25",
            "meta": {"service_name": "3 hour"},
            "service": "zoom2u_3_hour",
            "total_charge": 86.0,
            "transit_days": 1,
        },
        {
            "carrier_id": "zoom2u",
            "carrier_name": "zoom2u",
            "currency": "AUD",
            "estimated_delivery": "2020-12-24",
            "meta": {"service_name": "VIP"},
            "service": "zoom2u_VIP",
            "total_charge": 159.0,
            "transit_days": 1,
        },
    ],
    [],
]


RateRequest = {
    "PurchaseOrderNumber": "ABCD1234",
    "PackageDescription": "1 box with some cakes",
    "DeliverySpeed": "VIP",
    "ReadyDateTime": "2020-12-24T10:20:00.000000Z",
    "VehicleType": "Car",
    "PackageType": "Box",
    "Pickup": {
        "ContactName": "John Smith",
        "Email": "test@test.com",
        "Phone": "0000 0000",
        "StreetNumber": "123",
        "Street": "Main St",
        "Suburb": "North Sydney",
        "State": "NSW",
        "Postcode": "2000",
        "Country": "Australia",
    },
    "Dropoff": {
        "ContactName": "Jane Smith",
        "Email": "test@test.com",
        "Phone": "0000 0000",
        "StreetNumber": "123",
        "Street": "Main St",
        "Suburb": "North Sydney",
        "State": "NSW",
        "Postcode": "2000",
        "Country": "Australia",
    },
}


RateResponse = """[
  {
    "deliverySpeed": "Same day",
    "price": 68,
    "deliveredBy": "2020-12-25T06:00:00Z",
    "earliestPickupEta": "2020-12-24T11:20:00Z",
    "earliestDropEta": "2020-12-24T11:20:00Z"
  },
  {
    "deliverySpeed": "Same day",
    "price": 68,
    "deliveredBy": "2020-12-25T09:30:00Z"
  },
  {
    "deliverySpeed": "3 hour",
    "price": 86,
    "deliveredBy": "2020-12-25T01:00:00Z"
  },
  {
    "deliverySpeed": "VIP",
    "price": 159,
    "deliveredBy": "2020-12-24T11:20:00Z"
  }
]
"""
