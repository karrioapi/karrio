## `Create`

The Gateway encapsulate the access to the carrier's API. A carrier gateway instance
can created by using the `purplship.gateway` Gateway's initializer.

```python
import purplship
carrier_gateway = purplship.gateway["carrier_name"].create(...)
```

### Carrier Gateways
    
=== "Plain"
    ```python
    import purplship
    
    # canadapost_gateway = purplship.gateway["carrier_name"].create(
    canadapost_gateway = purplship.gateway["canadapost"].create(
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
    
    # canadapost_gateway = purplship.gateway["carrier_name"].create(
    canadapost_gateway = purplship.gateway["canadapost"].create(
        Settings(
            username="username",
            password="password",
            customer_number="123456789",
            test=True
        )
    )
    ```



#### USPS Settings

| Name | Type | Description 
| --- | --- | --- |
| `username` | `str` | **required**
| `password` | `str` | **required**
| `id` | `str` | 
| `test` | `bool` | 
| `carrier_id` | `str` | 


#### UPS Package Settings

| Name | Type | Description 
| --- | --- | --- |
| `username` | `str` | **required**
| `password` | `str` | **required**
| `access_license_number` | `str` | **required**
| `account_number` | `str` | 
| `id` | `str` | 
| `test` | `bool` | 
| `carrier_id` | `str` | 


#### Purolator Courier Settings

| Name | Type | Description 
| --- | --- | --- |
| `username` | `str` | **required**
| `password` | `str` | **required**
| `account_number` | `str` | **required**
| `user_token` | `str` | 
| `language` | `str` | 
| `id` | `str` | 
| `test` | `bool` | 
| `carrier_id` | `str` | 


#### FedEx Express Settings

| Name | Type | Description 
| --- | --- | --- |
| `user_key` | `str` | **required**
| `password` | `str` | **required**
| `meter_number` | `str` | **required**
| `account_number` | `str` | **required**
| `id` | `str` | 
| `test` | `bool` | 
| `carrier_id` | `str` | 


#### Dicom Settings

| Name | Type | Description 
| --- | --- | --- |
| `username` | `str` | **required**
| `password` | `str` | **required**
| `billing_account` | `str` | 
| `id` | `str` | 
| `test` | `bool` | 
| `carrier_id` | `str` | 


#### Canada Post Settings

| Name | Type | Description 
| --- | --- | --- |
| `username` | `str` | **required**
| `password` | `str` | **required**
| `customer_number` | `str` | **required**
| `contract_id` | `str` | 
| `language` | `str` | 
| `id` | `str` | 
| `test` | `bool` | 
| `carrier_id` | `str` | 


#### Canpar Settings

| Name | Type | Description 
| --- | --- | --- |
| `username` | `str` | **required**
| `password` | `str` | **required**
| `id` | `str` | 
| `test` | `bool` | 
| `carrier_id` | `str` | 


#### BoxKnight Settings

| Name | Type | Description 
| --- | --- | --- |
| `username` | `str` | **required**
| `password` | `str` | **required**
| `id` | `str` | 
| `test` | `bool` | 
| `carrier_id` | `str` | 


!!! note ""
    *Note that all carrier gateway defined bellow have these additional parameters*
    
    | Name | Type | Description
    | --- | --- | --- |
    | `carrier_name` | `str` | default: carrier name (eg: canadapost, purolator...)
    | `id` | `str` | 
    | `test` | `boolean` |

