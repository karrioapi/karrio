# ResourceTokenResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**token** | **string** | The JWT access token. | [default to undefined]
**expires_at** | **string** | Token expiration timestamp. | [default to undefined]
**resource_urls** | **{ [key: string]: string; }** | Map of resource IDs to their access URLs with token. | [default to undefined]

## Example

```typescript
import { ResourceTokenResponse } from './api';

const instance: ResourceTokenResponse = {
    token,
    expires_at,
    resource_urls,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
