# TrackingData


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**tracking_number** | **string** | The package tracking number | [default to undefined]
**carrier_name** | **string** | The tracking carrier | [default to undefined]
**account_number** | **string** | The shipper account number | [optional] [default to undefined]
**reference** | **string** | The shipment reference | [optional] [default to undefined]
**info** | [**TrackingInfo**](TrackingInfo.md) | The package and shipment tracking details | [optional] [default to undefined]
**metadata** | **{ [key: string]: any; }** | The carrier user metadata. | [optional] [default to undefined]

## Example

```typescript
import { TrackingData } from './api';

const instance: TrackingData = {
    tracking_number,
    carrier_name,
    account_number,
    reference,
    info,
    metadata,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
