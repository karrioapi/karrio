## `Fetch`

Using the fluent API with a gateway previously initialized, you can fetch live shipment rates

=== "Plain"
    ```python
    import purplship
    
    response = purplship.Rating.fetch({...})
    ```

=== "Typed"
    ```python
    import purplship
    from purplship.core.models import RateRequest
    
    response = purplship.Rating.fetch(RateRequest(...))
    ```

### Example

```python
import purplship
from purplship.core.models import Address, Parcel, RateRequest

shipper = Address(
    postal_code="V6M2V9",
    city="Vancouver",
    country_code="CA",
    state_code="BC",
    address_line1="5840 Oak St"
)

recipient = Address(
    postal_code="E1C4Z8",
    city="Moncton",
    country_code="CA",
    state_code="NB",
    residential=False,
    address_line1="125 Church St"
)

parcel = Parcel(
    height=3.0,
    length=6.0,
    width=3.0,
    weight=0.5,
    weight_unit='KG',
    dimension_unit='CM'
)

request = purplship.Rating.fetch(
    RateRequest(
        shipper=shipper,
        recipient=recipient,
        parcels=[parcel],
        services=["canadapost_xpresspost"]
    )
)

response = request.from_(canadapost).parse()
```

???+ check "Rating output"
    ```python
    from purplship.core.utils import DP
    print(DP.jsonify(response))
    ```
    
    ```json
    [
        [],
        [
            {
                "base_charge": 12.26,
                "carrier_id": "canadapost",
                "carrier_name": "canadapost",
                "currency": "CAD",
                "discount": 1.38,
                "duties_and_taxes": 0.0,
                "extra_charges": [
                    {
                        "amount": -0.37,
                        "currency": "CAD",
                        "name": "Automation discount"
                    },
                    {
                        "amount": 1.75,
                        "currency": "CAD",
                        "name": "Fuel surcharge"
                    }
                ],
                "service": "canadapost_xpresspost",
                "total_charge": 13.64,
                "transit_days": 2
            }
        ]
    ]
    ```
