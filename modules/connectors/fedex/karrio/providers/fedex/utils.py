import gzip
import jstruct
import datetime
import urllib.parse
import karrio.lib as lib
import karrio.core as core
import karrio.core.errors as errors


class Settings(core.Settings):
    """FedEx connection settings."""

    api_key: str = None
    secret_key: str = None
    account_number: str = None
    track_api_key: str = None
    track_secret_key: str = None

    account_country_code: str = None
    metadata: dict = {}
    config: dict = {}
    id: str = None

    @property
    def carrier_name(self):
        return "fedex"

    @property
    def server_url(self):
        return (
            "https://apis-sandbox.fedex.com"
            if self.test_mode
            else "https://apis.fedex.com"
        )

    @property
    def tracking_url(self):
        return "https://www.fedex.com/fedextrack/?trknbr={}"

    @property
    def connection_config(self) -> lib.units.Options:
        from karrio.providers.fedex.units import ConnectionConfig

        return lib.to_connection_config(
            self.config or {},
            option_type=ConnectionConfig,
        )

    @property
    def access_token(self):
        """Retrieve the access_token using the api_key|secret_key pair
        or collect it from the cache if an unexpired access_token exist.
        """
        if not all([self.api_key, self.secret_key, self.account_number]):
            raise Exception(
                "The api_key, secret_key and account_number are required for Rate, Ship and Other API requests."
            )

        cache_key = f"{self.carrier_name}|{self.api_key}|{self.secret_key}"
        now = datetime.datetime.now() + datetime.timedelta(minutes=30)

        auth = self.connection_cache.get(cache_key) or {}
        token = auth.get("access_token")
        expiry = lib.to_date(auth.get("expiry"), current_format="%Y-%m-%d %H:%M:%S")

        if token is not None and expiry is not None and expiry > now:
            return token

        self.connection_cache.set(
            cache_key,
            lambda: login(
                self,
                client_id=self.api_key,
                client_secret=self.secret_key,
            ),
        )
        new_auth = self.connection_cache.get(cache_key)

        return new_auth["access_token"]

    @property
    def track_access_token(self):
        """Retrieve the access_token using the track_api_key|track_secret_key pair
        or collect it from the cache if an unexpired access_token exist.
        """
        if not all([self.track_api_key, self.track_secret_key]):
            raise Exception(
                "The track_api_key and track_secret_key are required for Track API requests."
            )

        cache_key = f"{self.carrier_name}|{self.track_api_key}|{self.track_secret_key}"
        now = datetime.datetime.now() + datetime.timedelta(minutes=30)

        auth = self.connection_cache.get(cache_key) or {}
        token = auth.get("access_token")
        expiry = lib.to_date(auth.get("expiry"), current_format="%Y-%m-%d %H:%M:%S")

        if token is not None and expiry is not None and expiry > now:
            return token

        self.connection_cache.set(
            cache_key,
            lambda: login(
                self,
                client_id=self.track_api_key,
                client_secret=self.track_secret_key,
            ),
        )
        new_auth = self.connection_cache.get(cache_key)

        return new_auth["access_token"]


def login(settings: Settings, client_id: str = None, client_secret: str = None):
    import karrio.providers.fedex.error as error

    result = lib.request(
        url=f"{settings.server_url}/oauth/token",
        method="POST",
        headers={
            "content-Type": "application/x-www-form-urlencoded",
        },
        data=urllib.parse.urlencode(
            dict(
                grant_type="client_credentials",
                client_id=client_id,
                client_secret=client_secret,
            )
        ),
    )

    response = lib.to_dict(result)
    messages = error.parse_error_response(response, settings)

    if any(messages):
        raise errors.ShippingSDKError(messages)

    expiry = datetime.datetime.now() + datetime.timedelta(
        seconds=float(response.get("expires_in", 0))
    )

    return {**response, "expiry": lib.fdatetime(expiry)}


def parse_response(binary_string):
    content = lib.failsafe(lambda: gzip.decompress(binary_string)) or binary_string
    return lib.decode(content)


def process_request(
    settings: Settings, data: dict, request_type: str, ctx: dict = None
) -> dict:
    if settings.test_mode is False:
        return data

    if request_type == "rates":
        if (
            data["requestedShipment"]["shipper"]["address"]["countryCode"] != "US"
            or data["requestedShipment"]["recipient"]["address"]["countryCode"] != "US"
        ):

            if len(data["requestedShipment"]["requestedPackageLineItems"]) > 1:
                return INTL_MULTI_PIECE_RATE_QUOTE

            return INTL_RATE_QUOTE

        return US_DOMESTIC_RATE_QUOTE

    if request_type == "tracking":
        return TRACK_BY_NUMBER

    if request_type == "cancel":
        return CANCEL_SHIPMENT

    if request_type == "shipments":
        if "FEDEX_ONE_RATE" in data.get("requestedShipment", {}).get(
            "shipmentSpecialServices", {}
        ).get("specialServiceTypes", []):
            return apply_label_type(ONE_RATE_SHIPMENT, ctx)

        if (
            data["requestedShipment"]["shipper"]["address"]["countryCode"] != "US"
            or data["requestedShipment"]["recipients"][0]["address"]["countryCode"]
            != "US"
        ):
            if len(data["requestedShipment"]["requestedPackageLineItems"]) > 1:
                return apply_label_type(INTL_SINGLE_SHOT_MULTI_PIECE_SHIPMENT, ctx)

            return apply_label_type(MASTER_SHIPMENT, ctx)

        return apply_label_type(MASTER_SHIPMENT, ctx)

    return data


def apply_label_type(data: dict, ctx: dict) -> dict:
    if ctx is None:
        return data

    if "ZPL" in ctx.get("label_type", ""):
        return {
            **data,
            "requestedShipment": {
                **data["requestedShipment"],
                "labelSpecification": {
                    **data["requestedShipment"]["labelSpecification"],
                    "imageType": "ZPL",
                    "labelStockType": "PAPER_4X6",
                },
            },
        }

    return data


INTL_RATE_QUOTE = {
    "accountNumber": {"value": "XXXXX7364"},
    "requestedShipment": {
        "shipper": {"address": {"postalCode": 8099, "countryCode": "CH"}},
        "recipient": {"address": {"postalCode": 2116, "countryCode": "AU"}},
        "shipDateStamp": "2020-07-03",
        "pickupType": "DROPOFF_AT_FEDEX_LOCATION",
        "serviceType": "INTERNATIONAL_PRIORITY",
        "shipmentSpecialServices": {"specialServiceTypes": ["HOLD_AT_LOCATION"]},
        "rateRequestType": ["LIST", "ACCOUNT"],
        "customsClearanceDetail": {
            "dutiesPayment": {
                "paymentType": "SENDER",
                "payor": {"responsibleParty": None},
            },
            "commodities": [
                {
                    "description": "Camera",
                    "quantity": 1,
                    "quantityUnits": "PCS",
                    "weight": {"units": "KG", "value": 11},
                    "customsValue": {"amount": 100, "currency": "SFR"},
                }
            ],
        },
        "requestedPackageLineItems": [
            {
                "weight": {"units": "KG", "value": 11},
                "packageSpecialServices": {
                    "specialServiceTypes": ["SIGNATURE_OPTION"],
                    "signatureOptionType": "ADULT",
                },
            }
        ],
    },
}
US_DOMESTIC_RATE_QUOTE = {
    "accountNumber": {"value": "XXXXX7364"},
    "requestedShipment": {
        "shipper": {"address": {"postalCode": 65247, "countryCode": "US"}},
        "recipient": {"address": {"postalCode": 75063, "countryCode": "US"}},
        "pickupType": "DROPOFF_AT_FEDEX_LOCATION",
        "rateRequestType": ["ACCOUNT", "LIST"],
        "requestedPackageLineItems": [{"weight": {"units": "LB", "value": 10}}],
    },
}
INTL_MULTI_PIECE_RATE_QUOTE = {
    "accountNumber": {"value": "XXXXX7364"},
    "requestedShipment": {
        "shipper": {"address": {"postalCode": 8099, "countryCode": "CH"}},
        "recipient": {"address": {"postalCode": 2116, "countryCode": "AU"}},
        "shipDateStamp": "2020-07-03",
        "pickupType": "DROPOFF_AT_FEDEX_LOCATION",
        "serviceType": "INTERNATIONAL_PRIORITY",
        "rateRequestType": ["LIST", "ACCOUNT"],
        "customsClearanceDetail": {
            "dutiesPayment": {
                "paymentType": "SENDER",
                "payor": {"responsibleParty": None},
            },
            "commodities": [
                {
                    "description": "Camera",
                    "quantity": 1,
                    "quantityUnits": "PCS",
                    "weight": {"units": "KG", "value": 11},
                    "customsValue": {"amount": 100, "currency": "SFR"},
                }
            ],
        },
        "requestedPackageLineItems": [
            {"groupPackageCount": 2, "weight": {"units": "KG", "value": 1}},
            {"groupPackageCount": 3, "weight": {"units": "KG", "value": 10}},
        ],
    },
}
TRACK_BY_NUMBER = {
    "trackingInfo": [{"trackingNumberInfo": {"trackingNumber": "794843185271"}}],
    "includeDetailedScans": True,
}
ONE_RATE_SHIPMENT = {
    "labelResponseOptions": "URL_ONLY",
    "requestedShipment": {
        "shipper": {
            "contact": {
                "personName": "SHIPPER NAME",
                "phoneNumber": 1234567890,
                "companyName": "Shipper Company Name",
            },
            "address": {
                "streetLines": ["SHIPPER STREET LINE 1"],
                "city": "HARRISON",
                "stateOrProvinceCode": "AR",
                "postalCode": 72601,
                "countryCode": "US",
            },
        },
        "recipients": [
            {
                "contact": {
                    "personName": "RECIPIENT NAME",
                    "phoneNumber": 1234567890,
                    "companyName": "Recipient Company Name",
                },
                "address": {
                    "streetLines": [
                        "RECIPIENT STREET LINE 1",
                        "RECIPIENT STREET LINE 2",
                    ],
                    "city": "Collierville",
                    "stateOrProvinceCode": "TN",
                    "postalCode": 38017,
                    "countryCode": "US",
                },
            }
        ],
        "shipDatestamp": "2020-12-30",
        "serviceType": "STANDARD_OVERNIGHT",
        "packagingType": "FEDEX_SMALL_BOX",
        "pickupType": "USE_SCHEDULED_PICKUP",
        "blockInsightVisibility": False,
        "shippingChargesPayment": {"paymentType": "SENDER"},
        "shipmentSpecialServices": {"specialServiceTypes": ["FEDEX_ONE_RATE"]},
        "labelSpecification": {
            "imageType": "PDF",
            "labelStockType": "PAPER_85X11_TOP_HALF_LABEL",
        },
        "requestedPackageLineItems": [{}],
    },
    "accountNumber": {"value": "XXX561073"},
}
MASTER_SHIPMENT = {
    "labelResponseOptions": "URL_ONLY",
    "oneLabelAtATime": True,
    "requestedShipment": {
        "serviceType": "PRIORITY_OVERNIGHT",
        "shipper": {
            "address": {
                "residential": False,
                "city": "TAMPA",
                "countryCode": "US",
                "streetLines": ["10223 HAWK STORM AVE"],
                "postalCode": "336109168",
                "stateOrProvinceCode": "FL",
            },
            "contact": {
                "personName": "L6 FR FSM User L6FRLITER01",
                "emailAddress": "ramanjaneyulu.d.osv@fedex.com",
                "phoneNumber": 4152639685,
                "companyName": "MEMPHIS.",
            },
        },
        "recipients": [
            {
                "contact": {
                    "personName": "RECIPIENT NAME",
                    "phoneNumber": 9018328595,
                    "companyName": "RECIPIENT COMPANY",
                },
                "address": {
                    "city": "New York",
                    "stateOrProvinceCode": "NY",
                    "postalCode": "10001",
                    "countryCode": "US",
                    "residential": False,
                    "streetLines": ["RECIPIENT ADDRESS 1", "RECIPIENT ADDRESS 2"],
                },
            }
        ],
        "rateRequestType": ["LIST"],
        "labelSpecification": {
            "imageType": "PDF",
            "labelFormatType": "COMMON2D",
            "labelStockType": "PAPER_LETTER",
            "labelPrintingOrientation": "TOP_EDGE_OF_TEXT_FIRST",
            "autoPrint": False,
        },
        "customsClearanceDetail": {
            "isDocumentOnly": "false",
            "dutiesPayment": {"paymentType": "SENDER"},
            "commodities": [
                {
                    "description": "Glass Tubes",
                    "countryOfManufacture": "US",
                    "numberOfPieces": "1",
                    "weight": {"value": "101", "units": "LB"},
                    "cIMarksAndNumbers": "87123",
                    "exportLicenseDetail": {
                        "number": "26456",
                        "expirationDate": "2020-12-19",
                    },
                    "quantity": "1",
                    "quantityUnits": "USD",
                    "unitPrice": {"amount": "102", "currency": "USD"},
                    "customsValue": {"amount": "100", "currency": "USD"},
                }
            ],
        },
        "blockInsightVisibility": True,
        "shipDatestamp": "2023-05-18",
        "pickupType": "USE_SCHEDULED_PICKUP",
        "edtRequestType": "NONE",
        "shippingChargesPayment": {
            "payor": {
                "responsibleParty": {
                    "address": {
                        "residential": False,
                        "city": "TAMPA",
                        "countryCode": "US",
                        "streetLines": ["10223 HAWK STORM AVE"],
                        "postalCode": "336109168",
                        "stateOrProvinceCode": "FL",
                    },
                    "contact": {
                        "personName": "L6 FR FSM User L6FRLITER01",
                        "emailAddress": "neena_sebastian@syntelinc.com",
                        "phoneNumber": "4152639685",
                        "companyName": "Syntel Ltd.",
                    },
                    "accountNumber": {"value": "XXXXX1073"},
                }
            },
            "paymentType": "SENDER",
        },
        "packagingType": "YOUR_PACKAGING",
        "totalPackageCount": 2,
        "requestedPackageLineItems": [
            {
                "sequenceNumber": 1,
                "weight": {"units": "LB", "value": "10"},
                "subPackagingType": "BASKET",
            }
        ],
    },
    "accountNumber": {"value": "XXXXX1073"},
}
INTL_SINGLE_SHOT_MULTI_PIECE_SHIPMENT = {
    "labelResponseOptions": "URL_ONLY",
    "requestedShipment": {
        "shipper": {
            "contact": {
                "personName": "SHIPPER NAME",
                "phoneNumber": 1234567890,
                "companyName": "Shipper Company Name",
            },
            "address": {
                "streetLines": ["SHIPPER STREET LINE 1"],
                "city": "Memphis",
                "stateOrProvinceCode": "TN",
                "postalCode": 38116,
                "countryCode": "US",
            },
        },
        "recipients": [
            {
                "contact": {
                    "personName": "RECIPIENT NAME",
                    "phoneNumber": 1234567890,
                    "companyName": "Recipient Company Name",
                },
                "address": {
                    "streetLines": [
                        "RECIPIENT STREET LINE 1",
                        "RECIPIENT STREET LINE 2",
                        "RECIPIENT STREET LINE 3",
                    ],
                    "city": "RICHMOND",
                    "stateOrProvinceCode": "BC",
                    "postalCode": "V7C4V7",
                    "countryCode": "CA",
                },
            }
        ],
        "shipDatestamp": "2020-07-03",
        "serviceType": "INTERNATIONAL_PRIORITY",
        "packagingType": "YOUR_PACKAGING",
        "pickupType": "USE_SCHEDULED_PICKUP",
        "blockInsightVisibility": False,
        "shippingChargesPayment": {"paymentType": "SENDER"},
        "labelSpecification": {
            "imageType": "PDF",
            "labelStockType": "PAPER_85X11_TOP_HALF_LABEL",
        },
        "customsClearanceDetail": {
            "dutiesPayment": {"paymentType": "SENDER"},
            "isDocumentOnly": False,
            "commodities": [
                {
                    "description": "Commodity description",
                    "countryOfManufacture": "US",
                    "quantity": 3,
                    "quantityUnits": "PCS",
                    "unitPrice": {"amount": 100, "currency": "USD"},
                    "customsValue": {"amount": 300, "currency": "USD"},
                    "weight": {"units": "LB", "value": 20},
                }
            ],
        },
        "shippingDocumentSpecification": {
            "shippingDocumentTypes": ["COMMERCIAL_INVOICE"],
            "commercialInvoiceDetail": {
                "documentFormat": {"docType": "PDF", "stockType": "PAPER_LETTER"}
            },
        },
        "requestedPackageLineItems": [
            {
                "groupPackageCount": 1,
                "weight": {"value": 10, "units": "LB"},
                "declaredValue": {"amount": 100, "currency": "USD"},
            },
            {
                "groupPackageCount": 2,
                "weight": {"value": 5, "units": "LB"},
                "declaredValue": {"amount": 100, "currency": "USD"},
            },
        ],
    },
    "accountNumber": {"value": "XXX561073"},
}
CANCEL_SHIPMENT = {
    "accountNumber": {"value": "XXX561073"},
    "trackingNumber": "794842623031",
}
