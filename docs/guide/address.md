## `Validation`

```python
import purplship
from purplship.core.models import AddressValidationRequest

request = AddressValidationRequest(...)

validation, messages = purplship.Address.validate(request).from_(carrier_gateway).parse()
```

### Parameters


#### AddressValidationRequest

| Name | Type | Description 
| --- | --- | --- |
| `address` | [Address](#address) | **required**


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


### Response


#### AddressValidationDetails

| Name | Type | Description 
| --- | --- | --- |
| `carrier_name` | `str` | **required**
| `carrier_id` | `str` | **required**
| `success` | `bool` | **required**
| `complete_address` | [Address](#address) | 


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
from purplship.core.models import AddressValidationRequest, Address

address = Address(
    postal_code="V6M2V9",
    city="Vancouver",
    country_code="CA",
    state_code="BC",
    address_line1="5840 Oak St"
)

request = purplship.Address.validate(
    AddressValidationRequest(address=address)
)

tracking_details_list, messages = request.from_(carrier_gateway).parse()
```

???+ check "Tracking output"

    ```python
    print(tracking_details_list)
    # [
    #     TrackingDetails(
    #         carrier_name="canadapost",
    #         carrier_id="canadapost",
    #         tracking_number="7023210039414604",
    #         events=[
    #             TrackingEvent(
    #                 date="2011-04-04",
    #                 description="Order information received by Canada Post",
    #                 location="",
    #                 code="INDUCTION",
    #                 time="13:34",
    #                 signatory="",
    #             )
    #         ],
    #         delivered=None,
    #     )
    # ]
    ```
