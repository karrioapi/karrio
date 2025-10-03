# DocumentUploadData


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**shipment_id** | **string** | The documents related shipment. | [default to undefined]
**document_files** | [**Array&lt;DocumentFileData&gt;**](DocumentFileData.md) | Shipping document files | [default to undefined]
**reference** | **string** | Shipping document file reference | [optional] [default to undefined]

## Example

```typescript
import { DocumentUploadData } from './api';

const instance: DocumentUploadData = {
    shipment_id,
    document_files,
    reference,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
