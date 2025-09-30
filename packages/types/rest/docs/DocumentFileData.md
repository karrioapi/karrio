# DocumentFileData


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**doc_file** | **string** | A base64 file to upload | [default to undefined]
**doc_name** | **string** | The file name | [default to undefined]
**doc_format** | **string** | The file format | [optional] [default to undefined]
**doc_type** | **string** |          Shipment document type          values: &lt;br/&gt;         &#x60;certificate_of_origin&#x60; &#x60;commercial_invoice&#x60; &#x60;pro_forma_invoice&#x60; &#x60;packing_list&#x60; &#x60;other&#x60;          For carrier specific packaging types, please consult the reference.          | [optional] [default to 'other']

## Example

```typescript
import { DocumentFileData } from './api';

const instance: DocumentFileData = {
    doc_file,
    doc_name,
    doc_format,
    doc_type,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
