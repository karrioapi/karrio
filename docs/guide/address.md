## `Validation`

=== "Plain"
    ```python
    import purplship
    
    response = purplship.Address.validate({
        ...
    })
    ```

=== "Typed"
    ```python
    import purplship
    from purplship.core.models import AddressValidationRequest
    
    response = purplship.Address.validate(AddressValidationRequest(...))
    ```
