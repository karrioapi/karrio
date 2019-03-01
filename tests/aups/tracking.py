import unittest


class TestAustraliaPostTracking(unittest.TestCase):
    pass


TRACKING_RESPONSE = {
    "tracking_results": [
        {
            "tracking_id": "7XX1000",
            "errors": [{"code": "ESB-10001", "name": "Invalid tracking ID"}],
        },
        {
            "tracking_id": "7XX1000634011427",
            "status": "Delivered",
            "consignment": {
                "events": [
                    {
                        "location": "MEL",
                        "description": "Item Delivered",
                        "date": "2017-09-18T14:35:07+10:00",
                    },
                    {
                        "location": "MEL",
                        "description": "On Board for Delivery",
                        "date": "2017-09-18T09:50:05+10:00",
                    },
                ],
                "status": "Delivered in Full",
            },
            "trackable_items": [
                {
                    "article_id": "7XX1000634011427",
                    "product_type": "eParcel",
                    "events": [
                        {
                            "location": "ALEXANDRIA NSW",
                            "description": "Delivered",
                            "date": "2014-05-30T14:43:09+10:00",
                        },
                        {
                            "location": "ALEXANDRIA NSW",
                            "description": "With Australia Post for delivery today",
                            "date": "2014-05-30T06:08:51+10:00",
                        },
                        {
                            "location": "CHULLORA NSW",
                            "description": "Processed through Australia Post facility",
                            "date": "2014-05-29T19:40:19+10:00",
                        },
                        {
                            "location": "SYDNEY (AU)",
                            "description": "Arrived at facility in destination country",
                            "date": "2014-05-29T10:16:00+10:00",
                        },
                        {
                            "location": "JOHN F. KENNEDY APT\/NEW YORK (US)",
                            "description": "Departed facility",
                            "date": "2014-05-26T05:00:00+10:00",
                        },
                        {
                            "location": "JOHN F. KENNEDY APT\/NEW YORK (US)",
                            "description": "Departed facility",
                            "date": "2014-05-26T05:00:00+10:00",
                        },
                        {
                            "description": "Shipping information approved by Australia Post",
                            "date": "2014-05-23T14:27:15+10:00",
                        },
                    ],
                }
            ],
        },
    ]
}

TRACKING_ERROR = {
    "tracking_results": [
        {
            "tracking_id": "7XX1000",
            "errors": [{"code": "ESB-10001", "name": "Invalid tracking ID"}],
        }
    ]
}

ERRORS = {
    "errors": [
        {
            "code": "51101",
            "name": "TOO_MANY_AP_TRACKING_IDS",
            "message": "The request must contain 10 or less AP article ids, consignment ids, or barcode ids.",
        }
    ]
}
