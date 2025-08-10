# PickupUpdateRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**pickup_date** | **string** | The expected pickup date.&lt;br/&gt;         Date Format: &#x60;YYYY-MM-DD&#x60;          | [default to undefined]
**address** | [**Address**](Address.md) | The pickup address | [default to undefined]
**parcels** | [**Array&lt;Parcel&gt;**](Parcel.md) | The shipment parcels to pickup. | [default to undefined]
**confirmation_number** | **string** | pickup identification number | [default to undefined]
**ready_time** | **string** | The ready time for pickup.         Time Format: &#x60;HH:MM&#x60;          | [default to undefined]
**closing_time** | **string** | The closing or late time of the pickup.&lt;br/&gt;         Time Format: &#x60;HH:MM&#x60;          | [default to undefined]
**instruction** | **string** | The pickup instruction.&lt;br/&gt;         eg: Handle with care.          | [optional] [default to undefined]
**package_location** | **string** | The package(s) location.&lt;br/&gt;         eg: Behind the entrance door.          | [optional] [default to undefined]
**_options** | **{ [key: string]: any; }** | Advanced carrier specific pickup options | [optional] [default to undefined]

## Example

```typescript
import { PickupUpdateRequest } from './api';

const instance: PickupUpdateRequest = {
    pickup_date,
    address,
    parcels,
    confirmation_number,
    ready_time,
    closing_time,
    instruction,
    package_location,
    _options,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
