# PickupUpdateData


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**pickup_date** | **string** | The expected pickup date.&lt;br/&gt;         Date Format: YYYY-MM-DD          | [optional] [default to undefined]
**address** | [**AddressData**](AddressData.md) | The pickup address | [optional] [default to undefined]
**ready_time** | **string** | The ready time for pickup. | [optional] [default to undefined]
**closing_time** | **string** | The closing or late time of the pickup | [optional] [default to undefined]
**instruction** | **string** | The pickup instruction.&lt;br/&gt;         eg: Handle with care.          | [optional] [default to undefined]
**package_location** | **string** | The package(s) location.&lt;br/&gt;         eg: Behind the entrance door.          | [optional] [default to undefined]
**_options** | **{ [key: string]: any; }** | Advanced carrier specific pickup options | [optional] [default to undefined]
**tracking_numbers** | **Array&lt;string&gt;** | The list of shipments to be picked up | [optional] [default to undefined]
**metadata** | **{ [key: string]: any; }** | User metadata for the pickup | [optional] [default to undefined]
**confirmation_number** | **string** | pickup identification number | [default to undefined]

## Example

```typescript
import { PickupUpdateData } from './api';

const instance: PickupUpdateData = {
    pickup_date,
    address,
    ready_time,
    closing_time,
    instruction,
    package_location,
    _options,
    tracking_numbers,
    metadata,
    confirmation_number,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
