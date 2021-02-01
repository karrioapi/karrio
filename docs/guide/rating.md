## `Fetch`

Using the fluent API with a gateway previously initialized, you can fetch live shipping rates


```python
import purplship
from purplship.core.models import RateRequest

request = RateRequest(...)

rates, messages = purplship.Rating.fetch(request).from_(gateway).parse()
```


!!! info
    Checkout the reference for more details on the `RateRequest` and the returned `RateDetails` and 
    potential `Message` in case of error
    
    [REFERENCES](/references)


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

response = request.from_(gateway).parse()
```

???+ check "Rating output"

    ```python
    print(rates)
    # [
    #     RateDetails(
    #         carrier_name="canadapost",
    #         carrier_id="canadapost",
    #         currency="CAD",
    #         transit_days=2,
    #         service="canadapost_xpresspost",
    #         discount=1.38,
    #         base_charge=12.26,
    #         total_charge=13.64,
    #         duties_and_taxes=0.0,
    #         extra_charges=[
    #             ChargeDetails(name="Automation discount", amount=-0.37, currency="CAD"),
    #             ChargeDetails(name="Fuel surcharge", amount=1.75, currency="CAD"),
    #         ],
    #         meta=None,
    #         id=None,
    #     )
    # ]
    ```
