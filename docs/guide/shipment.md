## `Create`

Once you fetch shipment rates and select your preferred service, your can submit your shipment to the carrier
using the create function.

=== "Plain"
    ```python
    import purplship
    
    response = purplship.Shipment.create({
        ...
    })
    ```

=== "Typed"
    ```python
    import purplship
    from purplship.core.models import ShipmentRequest
    
    response = purplship.Shipment.create(ShipmentRequest(...))
    ```

## `Cancel`

Shipment previously submitted to the carrier server can be cancelled to void the attached label and let 
the carrier know that you do not intend to ship using the method selected anymore.

!!! warning ""
    It is recommended to cancel shipment (void the label printed) when you decide not to ship because some carriers
    will still bill you after a certain days for shipment submitted unless they are voided.

=== "Plain"
    ```python
    import purplship
    
    response = purplship.Shipment.cancel({
        ...
    })
    ```

=== "Typed"
    ```python
    import purplship
    from purplship.core.models import ShipmentCancelRequest
    
    response = purplship.Shipment.cancel(ShipmentRequest(...))
    ```

