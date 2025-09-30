# DocumentUploadRecord


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **string** | A unique identifier | [optional] [default to undefined]
**carrier_name** | **string** | The shipment carrier | [optional] [default to undefined]
**carrier_id** | **string** | The shipment carrier configured identifier | [optional] [default to undefined]
**documents** | [**Array&lt;DocumentDetails&gt;**](DocumentDetails.md) | the carrier shipping document ids | [optional] [default to undefined]
**meta** | **{ [key: string]: any; }** | provider specific metadata | [optional] [default to undefined]
**reference** | **string** | Shipping document file reference | [optional] [default to undefined]
**messages** | [**Array&lt;Message&gt;**](Message.md) | The list of note or warning messages | [optional] [default to undefined]

## Example

```typescript
import { DocumentUploadRecord } from './api';

const instance: DocumentUploadRecord = {
    id,
    carrier_name,
    carrier_id,
    documents,
    meta,
    reference,
    messages,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
