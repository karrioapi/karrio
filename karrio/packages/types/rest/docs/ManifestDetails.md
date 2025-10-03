# ManifestDetails


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **string** | A unique manifest identifier | [optional] [default to undefined]
**object_type** | **string** | Specifies the object type | [optional] [default to 'manifest']
**carrier_name** | **string** | The manifest carrier | [default to undefined]
**carrier_id** | **string** | The manifest carrier configured name | [default to undefined]
**doc** | [**ManifestDocument**](ManifestDocument.md) | The manifest documents | [optional] [default to undefined]
**meta** | **{ [key: string]: any; }** | provider specific metadata | [optional] [default to undefined]
**test_mode** | **boolean** | Specified whether it was created with a carrier in test mode | [default to undefined]

## Example

```typescript
import { ManifestDetails } from './api';

const instance: ManifestDetails = {
    id,
    object_type,
    carrier_name,
    carrier_id,
    doc,
    meta,
    test_mode,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
