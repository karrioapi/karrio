import unittest
from unittest.mock import patch
from karrio.core.utils import DP
from karrio import Tracking
from karrio.core.models import TrackingRequest
from .fixture import gateway


class TestCarrierTracking(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.TrackingRequest = TrackingRequest(tracking_numbers=TRACKING_PAYLOAD)

    def test_create_tracking_request(self):
        request = gateway.mapper.create_tracking_request(self.TrackingRequest)

        self.assertEqual(request.serialize(), TrackingRequestJSON)

    def test_get_tracking(self):
        with patch("karrio.mappers.dhl_universal.proxy.http") as mock:
            mock.return_value = "{}"
            Tracking.fetch(self.TrackingRequest).from_(gateway)

            self.assertEqual(
                mock.call_args[1]["url"],
                f"{gateway.settings.server_url}/track/shipments?language=en&trackingNumber=00340434292135100124",
            )

    def test_parse_tracking_response(self):
        with patch("karrio.mappers.dhl_universal.proxy.http") as mock:
            mock.return_value = TrackingResponseJSON
            parsed_response = (
                Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )
            self.assertListEqual(DP.to_dict(parsed_response), ParsedTrackingResponse)

    def test_parse_tracking_error_response(self):
        with patch("karrio.mappers.dhl_universal.proxy.http") as mock:
            mock.return_value = TrackingErrorResponseJSON
            parsed_response = (
                Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )

            self.assertListEqual(
                DP.to_dict(parsed_response), ParsedTrackingErrorResponse
            )


if __name__ == "__main__":
    unittest.main()

TRACKING_PAYLOAD = ["00340434292135100124"]

ParsedTrackingResponse = [
    [
        {
            "carrier_id": "dhl_universal",
            "carrier_name": "dhl_universal",
            "delivered": False,
            "estimated_delivery": "2018-08-03",
            "events": [
                {
                    "code": "pre-transit",
                    "date": "2018-03-02",
                    "description": "JESSICA",
                    "location": "Oderweg 2, AMSTERDAM",
                    "time": "07:53 AM",
                }
            ],
            "info": {
                "carrier_tracking_link": "https://www.dhl.com/de-en/home/tracking/tracking-parcel.html?submit=1&tracking-id=7777777770",
                "customer_name": "John Doe",
                "package_weight": 253.5,
                "package_weight_unit": "kg",
                "shipment_destination_country": "NL",
                "shipment_destination_postal_code": "1043 AG",
                "shipment_origin_country": "NL",
                "shipment_origin_postal_code": "1043 AG",
                "shipment_service": "UNKNOWN - Product unknown",
                "signed_by": "John Doe",
            },
            "meta": {"reference": "YZ3892406173"},
            "status": "in_transit",
            "tracking_number": "7777777770",
        }
    ],
    [],
]

ParsedTrackingErrorResponse = [
    [],
    [
        {
            "carrier_id": "dhl_universal",
            "carrier_name": "dhl_universal",
            "code": "404",
            "details": {"instance": "/shipment/8264715546", "title": "No result found"},
            "message": "No shipment with given tracking number found.",
        }
    ],
]


# Serialized output samples

TrackingRequestJSON = [{"language": "en", "trackingNumber": "00340434292135100124"}]

TrackingResponseJSON = """{
    "url": "/shipments?trackingNumber=7777777770?offset=0&limit=5",
    "prevUrl": "/shipments?trackingNumber=7777777770?offset=0&limit=5",
    "nextUrl": "/shipments?trackingNumber=7777777770?offset=5&limit=5",
    "firstUrl": "/shipments?trackingNumber=7777777770?offset=0&limit=5",
    "lastUrl": "/shipments?trackingNumber=7777777770?offset=10&limit=5",
    "shipments": [
      {
        "id": 7777777770,
        "service": "express",
        "origin": {
          "address": {
            "countryCode": "NL",
            "postalCode": "1043 AG",
            "addressLocality": "Oderweg 2, AMSTERDAM"
          }
        },
        "destination": {
          "address": {
            "countryCode": "NL",
            "postalCode": "1043 AG",
            "addressLocality": "Oderweg 2, AMSTERDAM"
          }
        },
        "status": {
          "timestamp": "2018-03-02T07:53:47Z",
          "location": {
            "address": {
              "countryCode": "NL",
              "postalCode": "1043 AG",
              "addressLocality": "Oderweg 2, AMSTERDAM"
            }
          },
          "statusCode": "pre-transit",
          "status": "DELIVERED",
          "description": "JESSICA",
          "remark": "The shipment is pending completion of customs inspection.",
          "nextSteps": "The status will be updated following customs inspection."
        },
        "estimatedTimeOfDelivery": "2018-08-03T00:00:00Z",
        "estimatedDeliveryTimeFrame": {
          "estimatedFrom": "2018-08-03T00:00:00Z",
          "estimatedThrough": "2018-08-03T22:00:00Z"
        },
        "estimatedTimeOfDeliveryRemark": "By End of Day",
        "serviceUrl": "http://www.dhl.de/de/privatkunden.html?piececode=7777777770",
        "rerouteUrl": "https://www.dhl.de/de/privatkunden.html?piececode=7777777770&verfuegen_selected_tab=FIRST",
        "details": {
          "carrier": {
            "@type": "Organization",
            "organizationName": "EXPRESS"
          },
          "product": {
            "productName": "UNKNOWN - Product unknown"
          },
          "receiver": {
            "@type": "Person",
            "organizationName": "EXPRESS",
            "familyName": "Doe",
            "givenName": "John",
            "name": "John"
          },
          "sender": {
            "@type": "Person",
            "organizationName": "EXPRESS",
            "familyName": "Doe",
            "givenName": "John",
            "name": "John"
          },
          "proofOfDelivery": {
            "timestamp": "2018-09-05T16:33:00Z",
            "signatureUrl": "string",
            "documentUrl": "https://webpod.dhl.com/webPOD/DHLePODRequest",
            "signed": {
              "@type": "Person",
              "familyName": "Doe",
              "givenName": "John",
              "name": "John"
            }
          },
          "totalNumberOfPieces": 8,
          "pieceIds": [
            "JD014600006281230704",
            "JD014600002708681600",
            "JD014600006615052259",
            "JD014600006615052264",
            "JD014600006615052265",
            "JD014600006615052268",
            "JD014600006615052307",
            "JD014600002266382340",
            "JD014600002659593446",
            "JD014600006101653481",
            "JD014600006614884499"
          ],
          "weight": {
            "value": 253.5,
            "unitText": "kg"
          },
          "volume": {
            "value": 12600
          },
          "loadingMeters": 1.5,
          "dimensions": {
            "width": {
              "value": 20,
              "unitText": "cm"
            },
            "height": {
              "value": 18,
              "unitText": "cm"
            },
            "length": {
              "value": 35,
              "unitText": "cm"
            }
          },
          "references": {
            "number": "YZ3892406173",
            "type": "customer-reference"
          }
        },
        "events": [
          {
            "timestamp": "2018-03-02T07:53:47",
            "location": {
              "address": {
                "countryCode": "NL",
                "postalCode": "1043 AG",
                "addressLocality": "Oderweg 2, AMSTERDAM"
              }
            },
            "statusCode": "pre-transit",
            "status": "DELIVERED",
            "description": "JESSICA",
            "remark": "The shipment is pending completion of customs inspection.",
            "nextSteps": "The status will be updated following customs inspection."
          }
        ]
      }
    ],
    "possibleAdditionalShipmentsUrl": [
      "/shipments?trackingNumber=7777777770&service=parcel-de",
      "/shipments?trackingNumber=7777777770&service=parcel-nl"
    ]
}
"""

TrackingErrorResponseJSON = """
{
    "title": "No result found",
    "detail": "No shipment with given tracking number found.",
    "status": 404,
    "instance": "/shipment/8264715546"
}
"""
