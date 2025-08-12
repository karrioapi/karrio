# PickupCancelRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**confirmation_number** | **string** | The pickup confirmation identifier | [default to undefined]
**address** | [**AddressData**](AddressData.md) | The pickup address | [optional] [default to undefined]
**pickup_date** | **string** | The pickup date.&lt;br/&gt;         Date Format: &#x60;YYYY-MM-DD&#x60;          | [optional] [default to undefined]
**reason** | **string** | The reason of the pickup cancellation | [optional] [default to undefined]

## Example

```typescript
import { PickupCancelRequest } from './api';

const instance: PickupCancelRequest = {
    confirmation_number,
    address,
    pickup_date,
    reason,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
