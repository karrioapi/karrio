import unittest
from unittest.mock import patch
from .fixture import gateway
from karrio.core.utils import DP
from karrio.core.models import TrackingRequest
from karrio import Tracking


class TestTNTTracking(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.TrackingRequest = TrackingRequest(tracking_numbers=TRACKING_PAYLOAD)

    def test_create_tracking_request(self):
        request = gateway.mapper.create_tracking_request(self.TrackingRequest)
        self.assertEqual(request.serialize(), TRACKING_REQUEST)

    def test_parse_tracking_response(self):
        with patch("karrio.mappers.tnt.proxy.lib.request") as mock:
            mock.return_value = TRACKING_RESPONSE
            parsed_response = (
                Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )

            self.assertEqual(
                DP.to_dict(parsed_response), DP.to_dict(PARSED_TRACKING_RESPONSE)
            )

    def test_tracking_auth_error_parsing(self):
        with patch("karrio.mappers.tnt.proxy.lib.request") as mock:
            mock.return_value = TRACKING_ERROR_RESPONSE
            parsed_response = (
                Tracking.fetch(self.TrackingRequest).from_(gateway).parse()
            )
            self.assertListEqual(
                DP.to_dict(parsed_response),
                PARSED_TRACKING_ERROR,
            )


if __name__ == "__main__":
    unittest.main()


TRACKING_PAYLOAD = ["22222222", "123456782"]

PARSED_TRACKING_RESPONSE = [
    [
        {
            "carrier_id": "tnt",
            "carrier_name": "tnt",
            "delivered": True,
            "events": [
                {
                    "code": "OK",
                    "date": "2021-02-18",
                    "description": "\n        Shipment Delivered In Good Condition.\n      ",
                    "location": "PNA-\n        Pamplona\n      ",
                    "time": "10:20 AM",
                }
            ],
            "tracking_number": "123456782",
        },
        {
            "carrier_id": "tnt",
            "carrier_name": "tnt",
            "delivered": True,
            "events": [
                {
                    "code": "OK",
                    "date": "2021-02-04",
                    "description": "\n        Shipment Delivered In Good Condition.\n      ",
                    "location": "BA4-\n        Bradford\n      ",
                    "time": "08:41 AM",
                },
                {
                    "code": "OD",
                    "date": "2021-02-04",
                    "description": "\n        Out For Delivery.\n      ",
                    "location": "BA4-\n        Bradford\n      ",
                    "time": "07:47 AM",
                },
                {
                    "code": "IR",
                    "date": "2021-02-04",
                    "description": "\n        Shipment Received At Tnt Location\n      ",
                    "location": "BA4-\n        Bradford\n      ",
                    "time": "05:09 AM",
                },
                {
                    "code": "IR",
                    "date": "2021-02-04",
                    "description": "\n        Shipment Received At Tnt Location\n      ",
                    "location": "BA4-\n        Bradford\n      ",
                    "time": "03:55 AM",
                },
                {
                    "code": "TR",
                    "date": "2021-02-03",
                    "description": "\n        Shipment In Transit.\n      ",
                    "location": "DZ5-\n        DZ5\n      ",
                    "time": "16:51 PM",
                },
                {
                    "code": "IS",
                    "date": "2021-02-03",
                    "description": "\n        Shipment Received At Tnt Location\n      ",
                    "location": "DZ5-\n        DZ5\n      ",
                    "time": "16:13 PM",
                },
                {
                    "code": "NR",
                    "date": "2021-02-03",
                    "description": "\n        Shipment Delayed In Transit Recovery Actions Underway\n      ",
                    "location": "BA4-\n        Bradford\n      ",
                    "time": "14:12 PM",
                },
                {
                    "code": "NR",
                    "date": "2021-02-03",
                    "description": "\n        Shipment Delayed In Transit Recovery Actions Underway\n      ",
                    "location": "BA4-\n        Bradford\n      ",
                    "time": "10:52 AM",
                },
                {
                    "code": "MLA",
                    "date": "2021-02-02",
                    "description": "\n        Connection Delay. Recovery Actions Underway.\n      ",
                    "location": "DZ5-\n        DZ5\n      ",
                    "time": "21:45 PM",
                },
                {
                    "code": "IS",
                    "date": "2021-02-02",
                    "description": "\n        Shipment Received At Tnt Location\n      ",
                    "location": "QAR-\n        Arnhem Hub\n      ",
                    "time": "09:44 AM",
                },
                {
                    "code": "AS",
                    "date": "2021-02-02",
                    "description": "\n        Shipment Received At Transit Point.\n      ",
                    "location": "QAR-\n        Arnhem Hub\n      ",
                    "time": "09:24 AM",
                },
                {
                    "code": "IS",
                    "date": "2021-02-02",
                    "description": "\n        Shipment Received At Tnt Location\n      ",
                    "location": "QAR-\n        Arnhem Hub\n      ",
                    "time": "08:50 AM",
                },
                {
                    "code": "TR",
                    "date": "2021-02-01",
                    "description": "\n        Shipment In Transit.\n      ",
                    "location": "DNG-\n        Nuernberg Hub\n      ",
                    "time": "18:51 PM",
                },
                {
                    "code": "IS",
                    "date": "2021-02-01",
                    "description": "\n        Shipment Received At Tnt Location\n      ",
                    "location": "DNG-\n        Nuernberg Hub\n      ",
                    "time": "18:46 PM",
                },
                {
                    "code": "CI",
                    "date": "2021-02-01",
                    "description": "\n        Shipment Received At Origin Depot.\n      ",
                    "location": "NBE-\n        Nuernberg\n      ",
                    "time": "18:42 PM",
                },
            ],
            "tracking_number": "123456782",
        },
        {
            "carrier_id": "tnt",
            "carrier_name": "tnt",
            "delivered": False,
            "tracking_number": "22222222",
        },
    ],
    [],
]

PARSED_TRACKING_ERROR = [
    [],
    [
        {
            "carrier_id": "tnt",
            "carrier_name": "tnt",
            "code": "9000",
            "message": "Unauthorized Access",
        }
    ],
]


TRACKING_REQUEST = f"""<TrackRequest locale="en_US" version="3.1">
    <SearchCriteria marketType="INTERNATIONAL" originCountry="US">
        <ConsignmentNumber>22222222</ConsignmentNumber>
        <ConsignmentNumber>123456782</ConsignmentNumber>
    </SearchCriteria>
    <LevelOfDetail>
        <Complete originAddress="true" destinationAddress="true"/>
    </LevelOfDetail>
</TrackRequest>
"""

TRACKING_RESPONSE = """<?xml version="1.0" encoding="utf-8"?>
<TrackResponse>
  <Consignment access="public">
    <ConsignmentNumber>123456782</ConsignmentNumber>
    <OriginDepot>FDX</OriginDepot>
    <OriginDepotName>
      <![CDATA[FDX]]>
    </OriginDepotName>
    <CustomerReference>
      <![CDATA[783350930039]]>
    </CustomerReference>
    <CollectionDate format="YYYYMMDD">20210203</CollectionDate>
    <DeliveryTown>
      <![CDATA[ROWVILLE]]>
    </DeliveryTown>
    <DeliveryDate format="YYYYMMDD">20210218</DeliveryDate>
    <DeliveryTime format="HHMM">1020</DeliveryTime>
    <Signatory>
      <![CDATA[sesar chevines]]>
    </Signatory>
    <SummaryCode>DEL</SummaryCode>
    <DestinationCountry>
      <CountryCode>AU</CountryCode>
      <CountryName>
        <![CDATA[Australia]]>
      </CountryName>
    </DestinationCountry>
    <OriginCountry>
      <CountryCode>US</CountryCode>
      <CountryName>
        <![CDATA[United States]]>
      </CountryName>
    </OriginCountry>
    <PieceQuantity>1</PieceQuantity>
    <StatusData>
      <StatusCode>OK</StatusCode>
      <StatusDescription>
        <![CDATA[Shipment Delivered In Good Condition.]]>
      </StatusDescription>
      <LocalEventDate format="YYYYMMDD">20210218</LocalEventDate>
      <LocalEventTime format="HHMM">1020</LocalEventTime>
      <Depot>PNA</Depot>
      <DepotName>
        <![CDATA[Pamplona]]>
      </DepotName>
    </StatusData>
  </Consignment>
  <Consignment access="public">
    <ConsignmentNumber>123456782</ConsignmentNumber>
    <OriginDepot>NBE</OriginDepot>
    <OriginDepotName>
      <![CDATA[Nuernberg]]>
    </OriginDepotName>
    <CustomerReference>
      <![CDATA[SIPG50447739705]]>
    </CustomerReference>
    <CollectionDate format="YYYYMMDD">20210201</CollectionDate>
    <DeliveryTown>
      <![CDATA[MENSTON]]>
    </DeliveryTown>
    <DeliveryDate format="YYYYMMDD">20210204</DeliveryDate>
    <DeliveryTime format="HHMM">0841</DeliveryTime>
    <Signatory>
      <![CDATA[umbridge]]>
    </Signatory>
    <SummaryCode>DEL</SummaryCode>
    <DestinationCountry>
      <CountryCode>GB</CountryCode>
      <CountryName>
        <![CDATA[United Kingdom]]>
      </CountryName>
    </DestinationCountry>
    <OriginCountry>
      <CountryCode>DE</CountryCode>
      <CountryName>
        <![CDATA[Germany]]>
      </CountryName>
    </OriginCountry>
    <PieceQuantity>2</PieceQuantity>
    <StatusData>
      <StatusCode>OK</StatusCode>
      <StatusDescription>
        <![CDATA[Shipment Delivered In Good Condition.]]>
      </StatusDescription>
      <LocalEventDate format="YYYYMMDD">20210204</LocalEventDate>
      <LocalEventTime format="HHMM">0841</LocalEventTime>
      <Depot>BA4</Depot>
      <DepotName>
        <![CDATA[Bradford]]>
      </DepotName>
    </StatusData>
    <StatusData>
      <StatusCode>OD</StatusCode>
      <StatusDescription>
        <![CDATA[Out For Delivery.]]>
      </StatusDescription>
      <LocalEventDate format="YYYYMMDD">20210204</LocalEventDate>
      <LocalEventTime format="HHMM">0747</LocalEventTime>
      <Depot>BA4</Depot>
      <DepotName>
        <![CDATA[Bradford]]>
      </DepotName>
    </StatusData>
    <StatusData>
      <StatusCode>IR</StatusCode>
      <StatusDescription>
        <![CDATA[Shipment Received At Tnt Location]]>
      </StatusDescription>
      <LocalEventDate format="YYYYMMDD">20210204</LocalEventDate>
      <LocalEventTime format="HHMM">0509</LocalEventTime>
      <Depot>BA4</Depot>
      <DepotName>
        <![CDATA[Bradford]]>
      </DepotName>
    </StatusData>
    <StatusData>
      <StatusCode>IR</StatusCode>
      <StatusDescription>
        <![CDATA[Shipment Received At Tnt Location]]>
      </StatusDescription>
      <LocalEventDate format="YYYYMMDD">20210204</LocalEventDate>
      <LocalEventTime format="HHMM">0355</LocalEventTime>
      <Depot>BA4</Depot>
      <DepotName>
        <![CDATA[Bradford]]>
      </DepotName>
    </StatusData>
    <StatusData>
      <StatusCode>TR</StatusCode>
      <StatusDescription>
        <![CDATA[Shipment In Transit.]]>
      </StatusDescription>
      <LocalEventDate format="YYYYMMDD">20210203</LocalEventDate>
      <LocalEventTime format="HHMM">1651</LocalEventTime>
      <Depot>DZ5</Depot>
      <DepotName>
        <![CDATA[DZ5]]>
      </DepotName>
    </StatusData>
    <StatusData>
      <StatusCode>IS</StatusCode>
      <StatusDescription>
        <![CDATA[Shipment Received At Tnt Location]]>
      </StatusDescription>
      <LocalEventDate format="YYYYMMDD">20210203</LocalEventDate>
      <LocalEventTime format="HHMM">1613</LocalEventTime>
      <Depot>DZ5</Depot>
      <DepotName>
        <![CDATA[DZ5]]>
      </DepotName>
    </StatusData>
    <StatusData>
      <StatusCode>NR</StatusCode>
      <StatusDescription>
        <![CDATA[Shipment Delayed In Transit Recovery Actions Underway]]>
      </StatusDescription>
      <LocalEventDate format="YYYYMMDD">20210203</LocalEventDate>
      <LocalEventTime format="HHMM">1412</LocalEventTime>
      <Depot>BA4</Depot>
      <DepotName>
        <![CDATA[Bradford]]>
      </DepotName>
    </StatusData>
    <StatusData>
      <StatusCode>NR</StatusCode>
      <StatusDescription>
        <![CDATA[Shipment Delayed In Transit Recovery Actions Underway]]>
      </StatusDescription>
      <LocalEventDate format="YYYYMMDD">20210203</LocalEventDate>
      <LocalEventTime format="HHMM">1052</LocalEventTime>
      <Depot>BA4</Depot>
      <DepotName>
        <![CDATA[Bradford]]>
      </DepotName>
    </StatusData>
    <StatusData>
      <StatusCode>MLA</StatusCode>
      <StatusDescription>
        <![CDATA[Connection Delay. Recovery Actions Underway.]]>
      </StatusDescription>
      <LocalEventDate format="YYYYMMDD">20210202</LocalEventDate>
      <LocalEventTime format="HHMM">2145</LocalEventTime>
      <Depot>DZ5</Depot>
      <DepotName>
        <![CDATA[DZ5]]>
      </DepotName>
    </StatusData>
    <StatusData>
      <StatusCode>IS</StatusCode>
      <StatusDescription>
        <![CDATA[Shipment Received At Tnt Location]]>
      </StatusDescription>
      <LocalEventDate format="YYYYMMDD">20210202</LocalEventDate>
      <LocalEventTime format="HHMM">0944</LocalEventTime>
      <Depot>QAR</Depot>
      <DepotName>
        <![CDATA[Arnhem Hub]]>
      </DepotName>
    </StatusData>
    <StatusData>
      <StatusCode>AS</StatusCode>
      <StatusDescription>
        <![CDATA[Shipment Received At Transit Point.]]>
      </StatusDescription>
      <LocalEventDate format="YYYYMMDD">20210202</LocalEventDate>
      <LocalEventTime format="HHMM">0924</LocalEventTime>
      <Depot>QAR</Depot>
      <DepotName>
        <![CDATA[Arnhem Hub]]>
      </DepotName>
    </StatusData>
    <StatusData>
      <StatusCode>IS</StatusCode>
      <StatusDescription>
        <![CDATA[Shipment Received At Tnt Location]]>
      </StatusDescription>
      <LocalEventDate format="YYYYMMDD">20210202</LocalEventDate>
      <LocalEventTime format="HHMM">0850</LocalEventTime>
      <Depot>QAR</Depot>
      <DepotName>
        <![CDATA[Arnhem Hub]]>
      </DepotName>
    </StatusData>
    <StatusData>
      <StatusCode>TR</StatusCode>
      <StatusDescription>
        <![CDATA[Shipment In Transit.]]>
      </StatusDescription>
      <LocalEventDate format="YYYYMMDD">20210201</LocalEventDate>
      <LocalEventTime format="HHMM">1851</LocalEventTime>
      <Depot>DNG</Depot>
      <DepotName>
        <![CDATA[Nuernberg Hub]]>
      </DepotName>
    </StatusData>
    <StatusData>
      <StatusCode>IS</StatusCode>
      <StatusDescription>
        <![CDATA[Shipment Received At Tnt Location]]>
      </StatusDescription>
      <LocalEventDate format="YYYYMMDD">20210201</LocalEventDate>
      <LocalEventTime format="HHMM">1846</LocalEventTime>
      <Depot>DNG</Depot>
      <DepotName>
        <![CDATA[Nuernberg Hub]]>
      </DepotName>
    </StatusData>
    <StatusData>
      <StatusCode>CI</StatusCode>
      <StatusDescription>
        <![CDATA[Shipment Received At Origin Depot.]]>
      </StatusDescription>
      <LocalEventDate format="YYYYMMDD">20210201</LocalEventDate>
      <LocalEventTime format="HHMM">1842</LocalEventTime>
      <Depot>NBE</Depot>
      <DepotName>
        <![CDATA[Nuernberg]]>
      </DepotName>
    </StatusData>
  </Consignment>
  <Consignment access="public">
    <ConsignmentNumber>22222222</ConsignmentNumber>
    <SummaryCode>CNF</SummaryCode>
  </Consignment>
</TrackResponse>
"""

TRACKING_ERROR_RESPONSE = """<?xml version="1.0" encoding="UTF-8"?>
<TrackResponse>
    <Error>
        <Code>9000</Code>
        <Message><![CDATA[Unauthorized Access]]></Message>
    </Error>
</TrackResponse>
"""
