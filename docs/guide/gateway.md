## `Create`

The Gateway encapsulate the access to the carrier's API. A carrier gateway instance
can created by using the `purplship.gateway` Gateway's initializer.

```python
import purplship
carrier_gateway = purplship.gateway["carrier"].create(...)
```

### Example

=== "Typed"
    ```python
    import purplship
    # from purplship.mappers.[carrier].settings import Settings
    from purplship.mappers.canadapost.settings import Settings
    
    canadapost_gateway = purplship.gateway["canadapost"].create(
        Settings(
            username="username",
            password="password",
            customer_number="123456789",
            test=True
        )
    )
    ```
    
=== "Plain"
    ```python
    import purplship
    
    canadapost_gateway = purplship.gateway["canadapost"].create(
        {
            "username": "username",
            "password": "password",
            "customer_number": "123456789",
            "test": True
        }
    )
    ```


!!! info
    Check the [gateway reference](/references/#gateway) to see the settings required by all supported carriers
