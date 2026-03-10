# Documents


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**label** | **string** | A shipping label in base64 string | [optional] [default to undefined]
**invoice** | **string** | A shipping invoice in base64 string | [optional] [default to undefined]
**extra_documents** | [**Array&lt;ShippingDocument&gt;**](ShippingDocument.md) | Additional shipping documents (return labels, COD documents, etc.) | [optional] [default to undefined]

## Example

```typescript
import { Documents } from './api';

const instance: Documents = {
    label,
    invoice,
    extra_documents,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
