# APIError


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**message** | **string** | The error or warning message | [optional] [default to undefined]
**code** | **string** | The message code | [optional] [default to undefined]
**level** | **string** | The message level | [optional] [default to undefined]
**details** | **{ [key: string]: any; }** | any additional details | [optional] [default to undefined]

## Example

```typescript
import { APIError } from './api';

const instance: APIError = {
    message,
    code,
    level,
    details,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
