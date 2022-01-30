import purplship

gateway = purplship.gateway["generic"].create(
    {
        "carrier_id": "custom-carrier",
        "custom_carrier_name": "custom_carrier",
        "verbose_name": "Custom Carrier",
        "services": [
            dict(
                service_name="Standard Service",
                service_code="standard_service",
                cost=100.00,
                currency="USD",
            )
        ],
        "metadata": {"APP_ID": "00", "SERIAL": "00099999000"},
    }
)
