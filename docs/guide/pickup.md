## `Schedule`

```python
import purplship
from purplship.core.models import PickupRequest

request = PickupRequest(...)

pickup, messages = purplship.Pickup.schedule(request).from_(gateway).parse()
```


!!! info
    Checkout the reference for more details on the `PickupRequest` and 
    the returned `PickupDetails` and potential `Message` in case of 
    failure or notice 
    
    [REFERENCES](/references)

## `Update`

```python
import purplship
from purplship.core.models import PickupUpdateRequest

request = PickupUpdateRequest(...)

pickup, messages = purplship.Pickup.update(request).from_(gateway).parse()
```


!!! info
    Checkout the reference for more details on the `PickupUpdateRequest` and 
    the returned `PickupDetails` and potential `Message` in case of 
    failure or notice 
    
    [REFERENCES](/references)

## `Cancel`

```python
import purplship
from purplship.core.models import PickupCancelRequest

request = PickupCancelRequest(...)

confirmation, messages = purplship.Pickup.cancel(request).from_(gateway).parse()
```


!!! info
    Checkout the reference for more details on the `PickupCancelRequest` and 
    the returned `ConfirmationDetails` and potential `Message` in case of 
    failure or notice 
    
    [REFERENCES](/references)
