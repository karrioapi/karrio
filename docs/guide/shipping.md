## `Create`

Once you fetch shipping rates and select your preferred service, your can submit your shipment to the carrier
using the create function.

```python
import purplship
from purplship.core.models import ShipmentRequest

request = ShipmentRequest(...)

response = purplship.Shipment.create(request).from_(gateway).parse()
```


!!! info
    Checkout the reference for more details on the `ShipmentRequest` and 
    the returned `ShipmentDetails` and potential `Message` in case of 
    failure or notice 
    
    [REFERENCES](/references)

## `Cancel`

Shipment previously submitted to the carrier server can be cancelled to void the attached label and let 
the carrier know that you do not intend to ship using the method selected anymore.

!!! warning ""
    It is recommended to cancel shipment (void the label printed) when you decide not to ship because some carriers
    will still bill you after a certain days for shipment submitted unless they are voided.


```python
import purplship
from purplship.core.models import ShipmentCancelRequest

request = ShipmentCancelRequest(...)

response = purplship.Shipment.cancel(request).from_(gateway).parse()
```


!!! info
    Checkout the reference for more details on the `ShipmentCancelRequest` and 
    the returned `ConfirmationDetails` and potential `Message` in case of 
    failure or notice 
    
    [REFERENCES](/references)
