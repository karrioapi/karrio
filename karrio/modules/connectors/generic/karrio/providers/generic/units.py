import karrio.lib as lib
import karrio.core.models as models


class ConnectionConfig(lib.Enum):
    text_color = lib.OptionEnum("text_color")
    brand_color = lib.OptionEnum("brand_color")


class Service(lib.Enum):
    standard_service = "standard"


class Option(lib.Enum):
    tracking_number_reference = lib.OptionEnum("tracking_number")


DEFAULT_SERVICES = [
    models.ServiceLevel(
        service_name="Standard Service",
        service_code="standard_service",
        currency="USD",
        transit_days=1,
        zones=[models.ServiceZone(label="Zone 1", rate=0.0)],
    ),
]

SAMPLE_SHIPMENT_REQUEST = {
    "service": "carrier_premium",
    "label_type": "ZPL",
    "shipper": {
        "company_name": "CGI",
        "address_line1": "502 MAIN ST N",
        "city": "MONTREAL",
        "postal_code": "H2B1A0",
        "country_code": "CA",
        "person_name": "Bob",
        "phone_number": "1 (450) 823-8432",
        "state_code": "QC",
    },
    "recipient": {
        "company_name": "CGI",
        "address_line1": "23 jardin private",
        "city": "Ottawa",
        "postal_code": "K1K4T3",
        "country_code": "CA",
        "person_name": "Jain",
        "state_code": "ON",
    },
    "parcels": [
        {
            "height": 3.0,
            "length": 5.0,
            "width": 3.0,
            "weight": 4.0,
            "dimension_unit": "IN",
            "weight_unit": "LB",
            "reference_number": "2975565",
            "items": [
                {
                    "weight": 1.0,
                    "weight_unit": "LB",
                    "quantity": 1,
                    "title": "Item 1",
                    "sku": "SKU-1",
                    "metadata": {
                        "RFF_CN": "037-2332855",
                        "BGM": "040000000000016256",
                        "RFF_ON": "5424560",
                        "DEPT": "DBR128",
                        "CTL": "11253678",
                        "XXNC": "138039C01",
                        "NAD_UD": "570162",
                        "RFF_AJY": "907",
                        "RFF_AEM": "3901L",
                    },
                },
            ],
        }
    ],
}
