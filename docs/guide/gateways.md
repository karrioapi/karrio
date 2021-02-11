## `Create`

The Gateway encapsulate the access to the carrier's API. A carrier gateway instance
can created by using the `purplship.gateway` Gateway's initializer.

```python
import purplship
carrier_gateway = purplship.gateway["carrier_name"].create(...)
```

### Code sample
    
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

### Carrier Gateway Settings


#### Yunexpress Settings `[carrier_name = yunexpress]`

| Name | Type | Description 
| --- | --- | --- |
| `customer_number` | `str` | **required**
| `api_secret` | `str` | **required**
| `id` | `str` | 
| `test` | `bool` | 
| `carrier_id` | `str` | 


#### Yanwen Settings `[carrier_name = yanwen]`

| Name | Type | Description 
| --- | --- | --- |
| `customer_number` | `str` | **required**
| `license_key` | `str` | **required**
| `id` | `str` | 
| `test` | `bool` | 
| `carrier_id` | `str` | 


#### USPS Settings `[carrier_name = usps]`

| Name | Type | Description 
| --- | --- | --- |
| `username` | `str` | **required**
| `password` | `str` | **required**
| `id` | `str` | 
| `test` | `bool` | 
| `carrier_id` | `str` | 


#### SF-Express Settings `[carrier_name = sf_express]`

| Name | Type | Description 
| --- | --- | --- |
| `partner_id` | `str` | **required**
| `check_word` | `str` | **required**
| `id` | `str` | 
| `test` | `bool` | 
| `carrier_id` | `str` | 


#### Sendle Settings `[carrier_name = sendle]`

| Name | Type | Description 
| --- | --- | --- |
| `sendle_id` | `str` | **required**
| `api_key` | `str` | **required**
| `id` | `str` | 
| `test` | `bool` | 
| `carrier_id` | `str` | 


#### Royal Mail Settings `[carrier_name = royalmail]`

| Name | Type | Description 
| --- | --- | --- |
| `client_id` | `str` | **required**
| `client_secret` | `str` | **required**
| `id` | `str` | 
| `test` | `bool` | 
| `carrier_id` | `str` | 


#### Dicom Settings `[carrier_name = dicom]`

| Name | Type | Description 
| --- | --- | --- |
| `username` | `str` | **required**
| `password` | `str` | **required**
| `billing_account` | `str` | 
| `id` | `str` | 
| `test` | `bool` | 
| `carrier_id` | `str` | 


#### DHL Universal Tracking Settings `[carrier_name = dhl_universal]`

| Name | Type | Description 
| --- | --- | --- |
| `consumer_key` | `str` | **required**
| `consumer_secret` | `str` | **required**
| `id` | `str` | 
| `test` | `bool` | 
| `carrier_id` | `str` | 


#### Australia Post Settings `[carrier_name = australiapost]`

| Name | Type | Description 
| --- | --- | --- |
| `api_key` | `str` | **required**
| `password` | `str` | **required**
| `account_number` | `str` | **required**
| `id` | `str` | 
| `test` | `bool` | 
| `carrier_id` | `str` | 


#### Aramex Settings `[carrier_name = aramex]`

| Name | Type | Description 
| --- | --- | --- |
| `username` | `str` | **required**
| `password` | `str` | **required**
| `account_pin` | `str` | **required**
| `account_entity` | `str` | **required**
| `account_number` | `str` | **required**
| `account_country_code` | `str` | **required**
| `id` | `str` | 
| `test` | `bool` | 
| `carrier_id` | `str` | 


#### BoxKnight Settings `[carrier_name = boxknight]`

| Name | Type | Description 
| --- | --- | --- |
| `username` | `str` | **required**
| `password` | `str` | **required**
| `id` | `str` | 
| `test` | `bool` | 
| `carrier_id` | `str` | 


#### Canada Post Settings `[carrier_name = canadapost]`

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


#### Canpar Settings `[carrier_name = canpar]`

| Name | Type | Description 
| --- | --- | --- |
| `username` | `str` | **required**
| `password` | `str` | **required**
| `id` | `str` | 
| `test` | `bool` | 
| `carrier_id` | `str` | 


#### DHL Express Settings `[carrier_name = dhl_express]`

| Name | Type | Description 
| --- | --- | --- |
| `site_id` | `str` | **required**
| `password` | `str` | **required**
| `account_number` | `str` | 
| `id` | `str` | 
| `test` | `bool` | 
| `carrier_id` | `str` | 


#### FedEx Express Settings `[carrier_name = fedex_express]`

| Name | Type | Description 
| --- | --- | --- |
| `user_key` | `str` | **required**
| `password` | `str` | **required**
| `meter_number` | `str` | **required**
| `account_number` | `str` | **required**
| `id` | `str` | 
| `test` | `bool` | 
| `carrier_id` | `str` | 


#### Purolator Courier Settings `[carrier_name = purolator_courier]`

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


#### UPS Package Settings `[carrier_name = ups_package]`

| Name | Type | Description 
| --- | --- | --- |
| `username` | `str` | **required**
| `password` | `str` | **required**
| `access_license_number` | `str` | **required**
| `account_number` | `str` | 
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

