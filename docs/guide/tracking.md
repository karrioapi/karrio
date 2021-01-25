## `Fetch`

You can retrieve one or many package tracking statuses passing the tracking numbers
to the `Tracking` API 

=== "Plain"
    ```python
    import purplship
    
    response = purplship.Tracking.fetch({
        ...
    })
    ```

=== "Typed"
    ```python
    import purplship
    from purplship.core.models import TrackingRequest
    
    response = purplship.Tracking.fetch(TrackingRequest(...))
    ```
