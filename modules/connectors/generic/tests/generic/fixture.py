import karrio

gateway = karrio.gateway["generic"].create(
    {
        "carrier_id": "custom-carrier",
        "custom_carrier_name": "custom_carrier",
        "display_name": "Custom Carrier",
        "services": [
            dict(
                service_name="Standard Service",
                service_code="standard_service",
                currency="USD",
                zones=[dict(rate=100.00)],
            )
        ],
        "metadata": {
            "APP_ID": "00",
            "EXTENSION_DIGIT": "0",
            "GS1_PREFIX": "0099999000",
            "CHECK_DIGIT": "5",
        },
    }
)
