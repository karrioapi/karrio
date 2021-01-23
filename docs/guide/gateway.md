## `Create`

The Gateway encapsulate the access to the carrier's API. A carrier gateway instance
can be using the `purplship.gateway` Gateway's initializer.

```python
import purplship
carrier_gateway = purplship.gateway["carrier"].create(...)
```

e.g:

=== "Plain"
    ```python
    import purplship
    
    canadapost = purplship.gateway["canadapost"].create(
        {
            "username": "username",
            "password": "password",
            "customer_number": "123456789",
            "test": True
        }
    )
    ```

=== "Typed"
    ```python
    import purplship
    # from purplship.mappers.[carrier].settings import Settings
    from purplship.mappers.canadapost.settings import Settings
    
    canadapost = purplship.gateway["canadapost"].create(
        Settings(
            username="username",
            password="password",
            customer_number="123456789",
            test=True
        )
    )
    ```
