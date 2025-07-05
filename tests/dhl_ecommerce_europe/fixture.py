import karrio.sdk as karrio
import karrio.core.models as models

gateway = karrio.gateway["dhl_ecommerce_europe"].create(
    dict(
        username="test_username",
        password="test_password", 
        account_number="123456789",
        test=True,
    )
)

# Test payload for rate requests
RatePayload = {
    "shipper": {
        "company_name": "Test Company",
        "person_name": "John Doe",
        "phone_number": "+49123456789",
        "email": "shipper@test.com",
        "address_line1": "Test Street 1",
        "city": "Berlin",
        "postal_code": "10115",
        "country_code": "DE",
    },
    "recipient": {
        "company_name": "Recipient Company", 
        "person_name": "Jane Smith",
        "phone_number": "+33123456789",
        "email": "recipient@test.com",
        "address_line1": "Test Street 2",
        "city": "Paris",
        "postal_code": "75001",
        "country_code": "FR",
    },
    "parcels": [
        {
            "weight": 2.5,
            "length": 20,
            "width": 15, 
            "height": 10,
            "weight_unit": "KG",
            "dimension_unit": "CM",
        }
    ],
    "services": ["V01PAK"],
}

# Test payload for shipment requests
ShipmentPayload = {
    "service": "V01PAK",
    "shipper": RatePayload["shipper"],
    "recipient": RatePayload["recipient"],
    "parcels": RatePayload["parcels"],
}

# Test payload for tracking requests
TrackingPayload = {
    "tracking_numbers": ["00340434292135100186"],
}

# Expected rate request
RateRequest = {
    "plannedShippingDateAndTime": "2025-01-20T09:00:00",
    "pickup": {
        "typeCode": "business",
        "accounts": [
            {
                "typeCode": "shipper",
                "number": "123456789",
            }
        ],
        "address": {
            "postalCode": "10115",
            "cityName": "Berlin",
            "countryCode": "DE",
        },
    },
    "productCode": "V01PAK",
    "accounts": [
        {
            "typeCode": "shipper",
            "number": "123456789",
        }
    ],
    "customerDetails": {
        "shipperDetails": {
            "postalAddress": {
                "postalCode": "10115",
                "cityName": "Berlin",
                "countryCode": "DE",
            }
        },
        "receiverDetails": {
            "postalAddress": {
                "postalCode": "75001",
                "cityName": "Paris",
                "countryCode": "FR",
            }
        },
    },
    "packages": [
        {
            "weight": 2.5,
            "dimensions": {
                "length": 20,
                "width": 15,
                "height": 10,
            },
        }
    ],
}

# Expected rate response
RateResponse = """{
  "products": [
    {
      "name": "DHL Parcel",
      "productCode": "V01PAK",
      "localProductCode": "V01PAK",
      "productType": "ETIME",
      "localProductCountryCode": "DE",
      "deliveryCapabilities": {
        "deliveryTypeCode": "QDDC",
        "estimatedDeliveryDateAndTime": "2025-01-22T17:00:00",
        "destinationServiceAreaCode": "BER",
        "destinationFacilityAreaCode": "BER",
        "deliveryAdditionalDays": 0,
        "deliveryDayOfWeek": 4,
        "totalTransitDays": 2
      },
      "totalPrice": [
        {
          "price": 25.50,
          "priceCurrency": "EUR",
          "priceType": "TOTAL",
          "breakdown": [
            {
              "name": "Base Price",
              "price": 20.00,
              "priceCurrency": "EUR",
              "priceType": "BASE"
            },
            {
              "name": "Fuel Surcharge",
              "price": 5.50,
              "priceCurrency": "EUR",
              "priceType": "TAX"
            }
          ]
        }
      ],
      "pickupCapabilities": {
        "nextBusinessDay": false,
        "requestedPickupTimeEarliest": "09:00",
        "requestedPickupTimeLatest": "17:00",
        "originServiceAreaCode": "BER",
        "originFacilityAreaCode": "BER",
        "pickupEarliest": "2025-01-20T09:00:00",
        "pickupLatest": "2025-01-20T17:00:00"
      }
    }
  ]
}"""

# Expected tracking response
TrackingResponse = """{
  "shipments": [
    {
      "shipmentTrackingNumber": "00340434292135100186",
      "status": {
        "timestamp": "2025-01-22T14:30:00",
        "location": {
          "address": {
            "addressLocality": "Berlin",
            "postalCode": "10115",
            "countryCode": "DE"
          }
        },
        "statusCode": "delivered",
        "status": "delivered",
        "description": "Delivered"
      },
      "estimatedTimeOfDelivery": "2025-01-22T15:00:00",
      "events": [
        {
          "date": "2025-01-20",
          "time": "09:15:00",
          "timestamp": "2025-01-20T09:15:00",
          "typeCode": "PU",
          "description": "Shipment picked up",
          "location": {
            "address": {
              "addressLocality": "Hamburg",
              "postalCode": "20095", 
              "countryCode": "DE"
            }
          },
          "serviceArea": [
            {
              "code": "HAM",
              "description": "Hamburg"
            }
          ]
        },
        {
          "date": "2025-01-22",
          "time": "14:30:00",
          "timestamp": "2025-01-22T14:30:00",
          "typeCode": "OK",
          "description": "Delivered",
          "location": {
            "address": {
              "addressLocality": "Berlin",
              "postalCode": "10115",
              "countryCode": "DE"
            }
          },
          "serviceArea": [
            {
              "code": "BER",
              "description": "Berlin"
            }
          ]
        }
      ]
    }
  ]
}""" 