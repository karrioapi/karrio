# ShipmentCancelRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**shipment_identifier** | **string** | The shipment identifier returned during creation. | [default to undefined]
**service** | **string** | The selected shipment service | [optional] [default to undefined]
**carrier_id** | **string** | The shipment carrier_id for specific connection selection. | [optional] [default to undefined]
**_options** | **{ [key: string]: any; }** | Advanced carrier specific cancellation options. | [optional] [default to undefined]

## Example

```typescript
import { ShipmentCancelRequest } from './api';

const instance: ShipmentCancelRequest = {
    shipment_identifier,
    service,
    carrier_id,
    _options,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
