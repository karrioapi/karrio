## `Fetch`

You can retrieve one or many package tracking statuses passing the tracking numbers
to the `Tracking` API.


```python
import purplship
from purplship.core.models import TrackingRequest

request = TrackingRequest(...)

tracking_details_list, messages = purplship.Tracking.fetch(request).from_(gateway).parse()
```

!!! info
    Checkout the reference for more details on the `TrackingRequest` and the returned `TrackingDetails` and 
    potential `Message` in case of error
    
    [REFERENCES](/references)

### Example

```python
import purplship
from purplship.core.models import TrackingRequest

request = purplship.Tracking.fetch(
    TrackingRequest(tracking_numbers=["1Z12345E6205277936"])
)

tracking_details_list, messages = request.from_(gateway).parse()
```

???+ check "Tracking output"

    ```python
    print(tracking_details_list)
    # [
    #     TrackingDetails(
    #         carrier_name="canadapost",
    #         carrier_id="canadapost",
    #         tracking_number="7023210039414604",
    #         events=[
    #             TrackingEvent(
    #                 date="2011-04-04",
    #                 description="Order information received by Canada Post",
    #                 location="",
    #                 code="INDUCTION",
    #                 time="13:34",
    #                 signatory="",
    #             )
    #         ],
    #         delivered=None,
    #     )
    # ]
    ```
