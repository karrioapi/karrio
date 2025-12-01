# ShipmentPurchaseData


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**selected_rate_id** | **string** | The shipment selected rate. | [optional] [default to undefined]
**service** | **string** | The carrier service to use for the shipment (alternative to selected_rate_id). | [optional] [default to undefined]
**label_type** | **string** | The shipment label file type. | [optional] [default to LabelTypeEnum_Pdf]
**payment** | [**Payment**](Payment.md) | The payment details | [optional] [default to undefined]
**reference** | **string** | The shipment reference | [optional] [default to undefined]
**metadata** | **{ [key: string]: any; }** | User metadata for the shipment | [optional] [default to undefined]

## Example

```typescript
import { ShipmentPurchaseData } from './api';

const instance: ShipmentPurchaseData = {
    selected_rate_id,
    service,
    label_type,
    payment,
    reference,
    metadata,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
