# ShippingDocument

Serializer for shipping document download response.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**category** | **string** | The document category (e.g., \&#39;label\&#39;, \&#39;invoice\&#39;, \&#39;manifest\&#39;) | [default to undefined]
**format** | **string** | The document format (e.g., \&#39;PDF\&#39;, \&#39;ZPL\&#39;) | [default to undefined]
**print_format** | **string** | The document print format (e.g., \&#39;A4\&#39;, \&#39;6x4\&#39;, \&#39;8.5x11\&#39;) | [optional] [default to undefined]
**url** | **string** | The document URL | [optional] [default to undefined]
**base64** | **string** | The document content encoded in base64 | [optional] [default to undefined]

## Example

```typescript
import { ShippingDocument } from './api';

const instance: ShippingDocument = {
    category,
    format,
    print_format,
    url,
    base64,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
