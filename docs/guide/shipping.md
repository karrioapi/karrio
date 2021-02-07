## `Create`

Once you fetch shipping rates and select your preferred service, your can submit your shipment to the carrier
using the create function.

```python
import purplship
from purplship.core.models import ShipmentRequest

request = ShipmentRequest(...)

shipment, messages = purplship.Shipment.create(request).from_(gateway).parse()
```

### Parameters


#### ShipmentRequest

| Name | Type | Description 
| --- | --- | --- |
| `service` | `str` | **required**
| `shipper` | [Address](#address) | **required**
| `recipient` | [Address](#address) | **required**
| `parcels` | List[[Parcel](#parcel)] | **required**
| `payment` | [Payment](#payment) | 
| `customs` | [Customs](#customs) | 
| `options` | `dict` | 
| `reference` | `str` | 
| `label_type` | `str` | 


#### Address

| Name | Type | Description 
| --- | --- | --- |
| `id` | `str` | 
| `postal_code` | `str` | 
| `city` | `str` | 
| `person_name` | `str` | 
| `company_name` | `str` | 
| `country_code` | `str` | 
| `email` | `str` | 
| `phone_number` | `str` | 
| `state_code` | `str` | 
| `suburb` | `str` | 
| `residential` | `bool` | 
| `address_line1` | `str` | 
| `address_line2` | `str` | 
| `federal_tax_id` | `str` | 
| `state_tax_id` | `str` | 


#### Parcel

| Name | Type | Description 
| --- | --- | --- |
| `id` | `str` | 
| `weight` | `float` | 
| `width` | `float` | 
| `height` | `float` | 
| `length` | `float` | 
| `packaging_type` | `str` | 
| `package_preset` | `str` | 
| `description` | `str` | 
| `content` | `str` | 
| `is_document` | `bool` | 
| `weight_unit` | `str` | 
| `dimension_unit` | `str` | 


#### Payment

| Name | Type | Description 
| --- | --- | --- |
| `paid_by` | `str` | 
| `amount` | `float` | 
| `currency` | `str` | 
| `account_number` | `str` | 
| `contact` | [Address](#address) | 
| `id` | `str` | 


#### Customs

| Name | Type | Description 
| --- | --- | --- |
| `aes` | `str` | 
| `eel_pfc` | `str` | 
| `certify` | `bool` | 
| `signer` | `str` | 
| `content_type` | `str` | 
| `content_description` | `str` | 
| `incoterm` | `str` | 
| `invoice` | `str` | 
| `certificate_number` | `str` | 
| `commodities` | List[[Commodity](#commodity)] | 
| `duty` | [Payment](#payment) | 
| `commercial_invoice` | `bool` | 
| `options` | `dict` | 
| `id` | `str` | 


#### Commodity

| Name | Type | Description 
| --- | --- | --- |
| `id` | `str` | 
| `weight` | `float` | 
| `weight_unit` | `str` | 
| `description` | `str` | 
| `quantity` | `int` | 
| `sku` | `str` | 
| `value_amount` | `float` | 
| `value_currency` | `str` | 
| `origin_country` | `str` | 



### Response


#### ShipmentDetails

| Name | Type | Description 
| --- | --- | --- |
| `carrier_name` | `str` | **required**
| `carrier_id` | `str` | **required**
| `label` | `str` | **required**
| `tracking_number` | `str` | **required**
| `shipment_identifier` | `str` | **required**
| `selected_rate` | [RateDetails](#ratedetails) | 
| `meta` | `dict` | 
| `id` | `str` | 


#### RateDetails

| Name | Type | Description 
| --- | --- | --- |
| `carrier_name` | `str` | **required**
| `carrier_id` | `str` | **required**
| `currency` | `str` | **required**
| `transit_days` | `int` | 
| `service` | `str` | 
| `discount` | `float` | 
| `base_charge` | `float` | 
| `total_charge` | `float` | 
| `duties_and_taxes` | `float` | 
| `extra_charges` | List[[ChargeDetails](#chargedetails)] | 
| `meta` | `dict` | 
| `id` | `str` | 


#### ChargeDetails

| Name | Type | Description 
| --- | --- | --- |
| `name` | `str` | 
| `amount` | `float` | 
| `currency` | `str` | 


#### Message

| Name | Type | Description 
| --- | --- | --- |
| `carrier_name` | `str` | **required**
| `carrier_id` | `str` | **required**
| `message` | Union[str, Any] | 
| `code` | `str` | 
| `details` | `dict` | 


---


### Code sample

```python
import purplship
from purplship.core.models import Address, Parcel, ShipmentRequest, Payment

shipper = Address(
    postal_code="V6M2V9",
    city="Vancouver",
    country_code="CA",
    state_code="BC",
    address_line1="5840 Oak St"
)

recipient = Address(
    postal_code="E1C4Z8",
    city="Moncton",
    country_code="CA",
    state_code="NB",
    residential=False,
    address_line1="125 Church St"
)

parcel = Parcel(
    height=3.0,
    length=6.0,
    width=3.0,
    weight=0.5,
    weight_unit='KG',
    dimension_unit='CM'
)

payment = Payment(paid_by="sender")

request = purplship.Shipment.create(
    ShipmentRequest(
        service="canadapost_xpresspost",
        shipper=shipper,
        recipient=recipient,
        parcels=[parcel],
        payment=payment
    )
)

shipment, messages = request.from_(carrier_gateway).parse()
```

???+ check "On success"

    ```python
    print(shipment)
    # ShipmentDetails(
    #     carrier_name="canadapost",
    #     carrier_id="canadapost",
    #     label="JVBERi0xLjQKJfbk/N8KMSAwIG9iago8PAovVHlwZSAvQ2F0YWxvZwovVmVyc2lvbiAvMS40CijEzMTA4MwolJUVPRgo=\n",
    #     tracking_number="123456789012",
    #     shipment_identifier="123456789012",
    #     selected_rate=None,
    #     meta=None,
    #     id=None,
    # )
    ```

---


## `Cancel`

Shipment previously submitted to the carrier server can be cancelled to void the attached label and let 
the carrier know that you do not intend to ship using the method selected anymore.

!!! warning ""
    It is recommended to cancel shipment (void the label printed) when you decide not to ship because some carriers
    will still bill you after a certain days for shipment submitted unless they are voided.


```python
import purplship
from purplship.core.models import ShipmentCancelRequest

request = ShipmentCancelRequest(...)

confirmation, messages = purplship.Shipment.cancel(request).from_(carrier_gateway).parse()
```

### Parameters


#### ShipmentCancelRequest

| Name | Type | Description 
| --- | --- | --- |
| `shipment_identifier` | `str` | **required**
| `service` | `str` | 
| `options` | `dict` | 


### Response


#### ConfirmationDetails

| Name | Type | Description 
| --- | --- | --- |
| `carrier_name` | `str` | **required**
| `carrier_id` | `str` | **required**
| `success` | `bool` | **required**
| `operation` | `str` | **required**


#### Message

| Name | Type | Description 
| --- | --- | --- |
| `carrier_name` | `str` | **required**
| `carrier_id` | `str` | **required**
| `message` | Union[str, Any] | 
| `code` | `str` | 
| `details` | `dict` | 


---


### Code sample

```python
import purplship
from purplship.core.models import ShipmentCancelRequest

request = purplship.Shipment.cancel(
    ShipmentCancelRequest(
        shipment_identifier='123456789012'
    )
)

confirmation, messages = request.from_(carrier_gateway).parse()
```

???+ check "On success"

    ```python
    print(confirmation)
    # ConfirmationDetails(
    #     carrier_name="canadapost",
    #     carrier_id="canadapost",
    #     success=True,
    #     operation="Cancel Shipment",
    # )
    ```
