## `Schedule`

=== "Plain"
    ```python
    import purplship
    
    response = purplship.Pickup.schedule({
        ...
    })
    ```

=== "Typed"
    ```python
    import purplship
    from purplship.core.models import PickupRequest
    
    response = purplship.Pickup.schedule(PickupRequest(...))
    ```

## `Update`

=== "Plain"
    ```python
    import purplship
    
    response = purplship.Pickup.update({
        ...
    })
    ```

=== "Typed"
    ```python
    import purplship
    from purplship.core.models import PickupUpdateRequest
    
    response = purplship.Pickup.update(PickupRequest(...))
    ```

## `Cancel`

=== "Plain"
    ```python
    import purplship
    
    response = purplship.Pickup.cancel({
        ...
    })
    ```

=== "Typed"
    ```python
    import purplship
    from purplship.core.models import PickupCancelRequest
    
    response = purplship.Pickup.cancel(PickupCancelRequest(...))
    ```
