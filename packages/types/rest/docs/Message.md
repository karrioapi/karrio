# Message


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**message** | **string** | The error or warning message | [optional] [default to undefined]
**code** | **string** | The message code | [optional] [default to undefined]
**level** | **string** | The message level | [optional] [default to undefined]
**details** | **{ [key: string]: any; }** | any additional details | [optional] [default to undefined]
**carrier_name** | **string** | The targeted carrier | [optional] [default to undefined]
**carrier_id** | **string** | The targeted carrier name (unique identifier) | [optional] [default to undefined]

## Example

```typescript
import { Message } from './api';

const instance: Message = {
    message,
    code,
    level,
    details,
    carrier_name,
    carrier_id,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
