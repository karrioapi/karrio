# ResourceTokenRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**resource_type** | **string** | The type of resource to grant access to. | [default to undefined]
**resource_ids** | **Array&lt;string&gt;** | List of resource IDs to grant access to. | [default to undefined]
**access** | **Array&lt;string&gt;** | List of access permissions to grant. | [default to undefined]
**format** | **string** | Document format (optional). | [optional] [default to undefined]
**expires_in** | **number** | Token expiration time in seconds (60-3600, default: 300). | [optional] [default to 300]

## Example

```typescript
import { ResourceTokenRequest } from './api';

const instance: ResourceTokenRequest = {
    resource_type,
    resource_ids,
    access,
    format,
    expires_in,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
