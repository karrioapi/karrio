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


!!! info
    Check the [Address validation request reference](/references/#addressvalidationrequest) 
    to see the parameters

